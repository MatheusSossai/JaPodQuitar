from datetime import date, datetime

from app.estruturas import DiarioProgresso, FilaMissoes
from app.excecoes import RegraNegocioErro
from app.extensoes import db
from app.opcoes import STATUS_MISSAO, STATUS_PROGRAMA
from app.validacao import texto_opcional


class ProgramaCessacao(db.Model):
    __tablename__ = "programa_cessacao"

    ATIVO = "ativo"
    CONCLUIDO = "concluido"
    INTERROMPIDO = "interrompido"

    id_programa = db.Column(db.Integer, primary_key=True)
    id_pessoa_usuario = db.Column(
        db.Integer, db.ForeignKey("usuario.id_pessoa", ondelete="CASCADE"), nullable=False
    )
    data_inicio = db.Column(db.Date, nullable=False)
    meta_dias = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, nullable=False, default=ATIVO)
    data_fim = db.Column(db.Date)

    usuario = db.relationship("Usuario", back_populates="programas")
    itens_fila = db.relationship(
        "ProgramaMissao",
        back_populates="programa",
        cascade="all, delete-orphan",
        order_by="ProgramaMissao.posicao_fila",
    )
    registros = db.relationship(
        "RegistroDiario",
        back_populates="programa",
        cascade="all, delete-orphan",
        order_by="RegistroDiario.posicao_pilha",
    )

    # ---- composição com as estruturas de dados ----
    # A fila e a pilha são montadas em memória a partir do banco a cada acesso.
    # A ordem fica salva em posicao_fila e posicao_pilha.

    def montar_fila(self):
        fila = FilaMissoes()
        for item in sorted(self.itens_fila, key=lambda i: i.posicao_fila):
            if item.status == ProgramaMissao.PENDENTE:
                fila.enfileirar(item)
        return fila

    def montar_diario(self):
        diario = DiarioProgresso()
        for registro in sorted(self.registros, key=lambda r: (r.posicao_pilha, r.data_hora)):
            diario.empilhar(registro)
        return diario

    # ---- missões ----

    def missao_atual(self):
        for item in self.itens_fila:
            if item.status == ProgramaMissao.EM_ANDAMENTO:
                return item
        return None

    def proxima_missao(self):
        """A que vem depois da atual (ainda bloqueada)."""
        return self.montar_fila().consultar_proxima()

    def missoes_concluidas(self):
        concluidas = [i for i in self.itens_fila if i.status == ProgramaMissao.CONCLUIDA]
        return sorted(concluidas, key=lambda i: i.data_conclusao or datetime.min)

    def concluir_missao(self, resposta=None, agora=None):
        atual = self.missao_atual()
        if atual is None:
            raise RegraNegocioErro("Não existe missão em andamento agora.")
        atual.concluir(resposta, agora)
        return atual

    def concluiu_missao_dia_um(self):
        return any(i.status == ProgramaMissao.CONCLUIDA and i.missao.ordem_dia == 1 for i in self.itens_fila)

    def pontos(self):
        return sum(item.missao.pontuacao() for item in self.missoes_concluidas())

    # ---- diário ----

    def registrar(self, registro):
        diario = self.montar_diario()
        topo = diario.consultar_topo()
        registro.posicao_pilha = topo.posicao_pilha + 1 if topo else 1
        diario.empilhar(registro)
        self.registros.append(registro)
        return diario

    # ---- números do programa ----

    def dias_de_programa(self, hoje=None):
        fim = self.data_fim or hoje or date.today()
        return max((fim - self.data_inicio).days, 0)

    def percentual_conclusao(self, hoje=None):
        if not self.meta_dias:
            return 0
        return min(100, round(self.dias_de_programa(hoje) / self.meta_dias * 100))

    def recorde_dias(self, hoje=None):
        """RN06: maior sequência sem nicotina dentro do programa.

        As recaídas são achadas pelo impacto negativo (polimorfismo), sem testar o tipo.
        """
        fim = self.data_fim or hoje or date.today()
        marcos = [self.data_inicio]
        for registro in sorted(self.registros, key=lambda r: r.data_hora):
            if registro.impacto() < 0:
                marcos.append(registro.data_hora.date())
        marcos.append(fim)
        return max(max((depois - antes).days, 0) for antes, depois in zip(marcos, marcos[1:]))

    def pode_ser_concluido(self, hoje=None):
        terminou_missoes = self.missao_atual() is None and self.montar_fila().esta_vazia()
        return self.dias_de_programa(hoje) >= self.meta_dias or terminou_missoes

    def status_legivel(self):
        return STATUS_PROGRAMA.get(self.status, self.status)

    def para_dict(self):
        return {
            "data_inicio": self.data_inicio.isoformat(),
            "data_fim": self.data_fim.isoformat() if self.data_fim else None,
            "meta_dias": self.meta_dias,
            "status": self.status,
            "missoes": [item.para_dict() for item in sorted(self.itens_fila, key=lambda i: i.posicao_fila)],
            "diario": [registro.para_dict() for registro in self.montar_diario().listar_recentes()],
        }


class ProgramaMissao(db.Model):
    """Resolve o N:N entre programa e missão e guarda a posição na fila."""

    __tablename__ = "programa_missao"

    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"

    id_programa_missao = db.Column(db.Integer, primary_key=True)
    id_programa = db.Column(
        db.Integer, db.ForeignKey("programa_cessacao.id_programa", ondelete="CASCADE"), nullable=False
    )
    id_missao = db.Column(db.Integer, db.ForeignKey("missao.id_missao"), nullable=False)
    posicao_fila = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, nullable=False, default=PENDENTE)
    data_conclusao = db.Column(db.DateTime)
    resposta = db.Column(db.Text)

    programa = db.relationship("ProgramaCessacao", back_populates="itens_fila")
    # agregação: a missão é do catálogo e continua existindo sem o programa
    missao = db.relationship("Missao", lazy="joined")

    def concluir(self, resposta=None, agora=None):
        resposta = texto_opcional(resposta, "resposta", 2000)
        if self.missao.exige_resposta() and not resposta:
            raise RegraNegocioErro("Essa missão pede uma resposta antes de ser concluída.")
        self.resposta = resposta
        self.status = self.CONCLUIDA
        self.data_conclusao = agora or datetime.now()

    def status_legivel(self):
        return STATUS_MISSAO.get(self.status, self.status)

    def para_dict(self):
        return {
            "posicao_fila": self.posicao_fila,
            "dia": self.missao.ordem_dia,
            "titulo": self.missao.titulo,
            "tipo": self.missao.rotulo(),
            "status": self.status,
            "data_conclusao": self.data_conclusao.isoformat(timespec="minutes") if self.data_conclusao else None,
            "resposta": self.resposta,
        }
