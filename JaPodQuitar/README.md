# Já Pod Quitar

Plataforma web de informação e acompanhamento para redução e cessação do uso de
cigarros eletrônicos (PODs).

Projeto da disciplina ADSIS4SM — Unicesumar, alinhado ao ODS 3 (Saúde e Bem-estar).

| | |
|---|---|
| **Equipe** | Matheus Bueno Sossai (RA 25127039-2) · Bruno Guerino Mendes (RA 25057244-2) · Vinicius Felipe Amstalden de Castro (RA 25178392-2) |
| **Arquitetura** | Cliente-servidor, monólito modular em camadas (MVC) |
| **Servidor** | Python 3 + Flask |
| **Persistência** | SQLite + SQLAlchemy (Flask-SQLAlchemy) |
| **Interface** | Jinja2 + Bootstrap 5 (CDN), sem etapa de build |
| **Testes** | pytest |

> A plataforma é uma ferramenta de informação e autoacompanhamento. Não emite
> diagnóstico nem prescreve tratamento (RN11).

## Como rodar

```bash
git clone https://github.com/MatheusSossai/JaPodQuitar.git
cd JaPodQuitar

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # Windows: copy .env.example .env
python scripts/criar_banco.py
python run.py
```

A aplicação sobe em `http://127.0.0.1:5000`. O banco fica em
`dados/japodquitar.db`, fora do controle de versão — para começar do zero,
apague o arquivo e rode `scripts/criar_banco.py` de novo.

Testes:

```bash
pytest
```

## Estrutura do repositório

```
JaPodQuitar/
├── .github/                      Templates de issue/PR e integração contínua
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── workflows/
│   │   └── ci.yml                Roda pytest a cada push e pull request
│   └── pull_request_template.md
├── app/                          Aplicação (camadas do MVC)
│   ├── __init__.py               Fábrica da aplicação e registro de blueprints
│   ├── config.py                 Configuração por ambiente
│   ├── extensions.py             Instâncias de SQLAlchemy e Flask-Login
│   ├── controladores/            CONTROLE — rotas, sem regra de negócio
│   │   ├── rotas_publicas.py         Página inicial, sobre, canais de apoio
│   │   ├── rotas_autenticacao.py     Cadastro, login, logout (RF01)
│   │   ├── rotas_painel.py           Painel, perfil de consumo, meus dados
│   │   ├── rotas_missoes.py          Missão atual e histórico (RF05)
│   │   ├── rotas_diario.py           Diário de progresso (RF06)
│   │   ├── rotas_conteudo.py         Módulo informativo aberto (RF02)
│   │   └── rotas_moderacao.py        Publicação de conteúdo (RF11)
│   ├── dominio/                  DOMÍNIO — classes de negócio puras
│   │   ├── pessoa.py                 Pessoa (abstrata) → Usuario, Moderador
│   │   ├── missao.py                 Missao (abstrata) → Reflexiva, Pratica, Educativa
│   │   ├── registro_diario.py        RegistroDiario (abstrata) → Sintoma, Recaida, Conquista
│   │   ├── programa_cessacao.py      Compõe a fila e a pilha do programa
│   │   ├── conteudo_informativo.py
│   │   └── estruturas/
│   │       ├── fila_missoes.py       FILA (FIFO) sobre deque — RN02, RN03
│   │       └── diario_progresso.py   PILHA (LIFO) sobre list — RN04
│   ├── servicos/                 SERVIÇO — regras RN01 a RN11
│   │   ├── servico_autenticacao.py
│   │   ├── servico_programa.py
│   │   ├── servico_missoes.py
│   │   ├── servico_diario.py
│   │   ├── servico_metricas.py       Dias sem nicotina e economia (RN06, RN08)
│   │   ├── servico_conteudo.py
│   │   └── servico_privacidade.py    Exportar e excluir dados (RF12, LGPD)
│   ├── repositorios/             REPOSITÓRIO — único ponto de acesso ao banco
│   │   ├── repositorio_base.py
│   │   ├── repositorio_usuario.py
│   │   ├── repositorio_programa.py
│   │   ├── repositorio_missao.py     Reconstrói a fila a partir de posicao_fila
│   │   ├── repositorio_registro.py   Reconstrói a pilha a partir de posicao_pilha
│   │   └── repositorio_conteudo.py
│   ├── modelos/                  PERSISTÊNCIA — tabelas do DER (seção 5.2)
│   │   ├── pessoa_modelo.py          PESSOA → USUARIO / MODERADOR (joined)
│   │   ├── programa_modelo.py        PROGRAMA_CESSACAO
│   │   ├── missao_modelo.py          MISSAO (tabela única) e PROGRAMA_MISSAO
│   │   ├── registro_modelo.py        REGISTRO_DIARIO → SINTOMA / RECAIDA / CONQUISTA
│   │   └── conteudo_modelo.py        CONTEUDO_INFORMATIVO
│   ├── templates/                APRESENTAÇÃO — páginas Jinja2
│   │   ├── base.html
│   │   ├── componentes/              Navbar, mensagens, rodapé, cartões
│   │   ├── publico/                  index, sobre, apoio
│   │   ├── autenticacao/             login, cadastro
│   │   ├── painel/                   painel, perfil_consumo, meus_dados
│   │   ├── missoes/                  missao_atual, historico
│   │   ├── diario/                   diario, novo_registro
│   │   ├── conteudo/                 lista, detalhe
│   │   ├── moderacao/                painel_moderador, formulario_conteudo
│   │   └── erros/                    404, 500
│   ├── static/                   CSS próprio, JavaScript e imagens
│   └── utils/                    Datas em ISO-8601 e validadores
├── dados/                        Banco SQLite (ignorado) e carga inicial
│   └── seeds/
│       ├── missoes_iniciais.json
│       └── conteudos_iniciais.json
├── docs/                         Documentação do projeto
│   ├── arquitetura.md
│   ├── requisitos.md
│   ├── regras-de-negocio.md
│   ├── diagramas/                Fontes do draw.io (classes e DER)
│   └── entrega-1/                PDF da 1.ª entrega
├── scripts/
│   ├── criar_banco.py            Cria as tabelas do DER
│   ├── popular_dados.py          Carrega os seeds
│   └── executar_testes.sh        pytest com relatório de cobertura
├── testes/
│   ├── conftest.py               Fixtures de aplicação e cliente de teste
│   ├── unidade/                  Fila, pilha, polimorfismo, regras de negócio
│   ├── integracao/               Rotas e fluxo ponta a ponta
│   └── fixtures/
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── pytest.ini
├── requirements.txt
└── run.py                        Ponto de entrada
```

## Por que essa organização

Cada pasta de `app/` corresponde a uma camada da seção 3.1 do documento de
concepção, e o fluxo de chamadas é sempre o mesmo:

```
controlador → serviço → repositório → modelo → SQLite
                 ↓
              domínio (fila, pilha, hierarquias de classes)
```

O domínio não importa Flask nem SQLAlchemy. É isso que permite testar as regras
RN01 a RN11 sem subir a aplicação nem o banco, como pede o RNF06. A fila e a
pilha ficam encapsuladas em `app/dominio/estruturas`: as demais camadas só
enxergam `enfileirar`, `desenfileirar`, `empilhar` e `consultar_topo`, nunca a
coleção interna.

Detalhes em [`docs/arquitetura.md`](docs/arquitetura.md),
[`docs/requisitos.md`](docs/requisitos.md) e
[`docs/regras-de-negocio.md`](docs/regras-de-negocio.md).

## Fluxo de trabalho

`main` guarda versões estáveis, `develop` integra o time e cada funcionalidade
nasce em `feature/nome-da-funcionalidade`. A entrada em `develop` é por pull
request, com revisão de um integrante que não seja o autor. Commits seguem o
padrão semântico (`feat`, `fix`, `docs`, `refactor`, `test`). Ver
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Planejamento

| Sprint | Período | Épico | Responsável |
|---|---|---|---|
| 1 | 15/09 – 28/09 | Domínio e autenticação (RF01, RF03) | Matheus |
| 2 | 29/09 – 12/10 | Motor de missões — fila (RF05) | Bruno |
| 3 | 13/10 – 26/10 | Diário de progresso — pilha (RF06) | Vinicius |
| 4 | 27/10 – 09/11 | Cálculos, alertas e persistência (RF07, RF08) | Equipe |

## Privacidade

Dados de saúde são tratados como dados pessoais sensíveis (Lei n.º 13.709/2018).
Senhas são armazenadas apenas como hash, o diário é visível somente ao próprio
titular e o usuário pode exportar ou excluir tudo (RF12). Os indicadores de
sucesso são apurados apenas sobre dados agregados e anonimizados.
