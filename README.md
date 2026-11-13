# Já Pod Quitar

Plataforma web de informação e acompanhamento para quem quer reduzir ou parar de usar cigarro eletrônico (pod).

Projeto da turma ADSIS4SM, Unicesumar, 2026.

- Matheus Bueno Sossai (RA 25127039-2)
- Bruno Guerino Mendes (RA 25057244-2)
- Vinicius Felipe Amstalden de Castro (RA 25178392-2)

Esta é a **2ª entrega (segundo bimestre)**: o código-fonte completo da aplicação, seguindo o que foi definido no documento de concepção da 1ª entrega (requisitos, regras de negócio, diagrama de classes e DER).

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Servidor | Python 3 + Flask |
| Banco de dados | SQLite, acessado pelo SQLAlchemy (Flask-SQLAlchemy) |
| Autenticação | Flask-Login + hash de senha do Werkzeug |
| Proteção dos formulários | Flask-WTF (só o CSRF) |
| Interface | HTML, CSS, JavaScript, Jinja2, Bootstrap 5 e Bootstrap Icons via CDN, fontes Nunito e Lora (Google Fonts) |
| Testes | pytest |

## Como rodar

Precisa ter o Python 3.10 ou mais novo instalado.

No Windows (PowerShell ou CMD), dentro da pasta do projeto:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

No Linux/Mac é igual, só troca a ativação por `source venv/bin/activate`.

Depois é só abrir http://127.0.0.1:5000 no navegador.

Na primeira execução o sistema cria o banco em `instance/japodquitar.db` e já cadastra o moderador, as 20 matérias informativas e o catálogo com 21 missões.

Se o banco foi criado antes de novas matérias serem escritas, rodar `python seed.py` adiciona só as que ainda não existem (a comparação é pelo título).

Para ter um usuário com histórico pronto (bom para a apresentação), rode uma vez:

```
python seed.py --demo
```

### Contas de teste

| Perfil | E-mail | Senha |
|---|---|---|
| Moderador | moderador@japodquitar.com | Moderador@123 |
| Usuário demo (depois do `seed.py --demo`) | demo@japodquitar.com | Demo@1234 |

O usuário demo começou o programa há 12 dias, concluiu 6 missões, teve uma recaída no 5º dia e tem registros de sintomas e conquistas no diário.

Para zerar tudo, é só apagar a pasta `instance/` e rodar de novo.

## Testes

```
pytest
```

São 61 testes, divididos em:

- `tests/test_estruturas.py`: fila e pilha
- `tests/test_modelos.py`: classes abstratas, herança, polimorfismo, hash de senha, cálculo da economia
- `tests/test_regras_programa.py`: RN01, RN02, RN03, adiamento e encerramento do programa
- `tests/test_regras_diario.py`: RN04 a RN07, RN09, RF08 e RF09
- `tests/test_rotas.py`: telas, permissões de acesso, CRUD do moderador, exportação e exclusão de conta
- `tests/test_conteudos.py`: formatação das matérias (inclusive bloqueio de HTML), fontes obrigatórias e carga de matérias novas

Os testes usam um banco SQLite em memória, então não mexem no banco de verdade.

## Estrutura de pastas

```
app/
  __init__.py          cria a aplicação (create_app), filtros e páginas de erro
  config.py            configurações (banco, chave secreta, testes)
  extensoes.py         db, login_manager e csrf
  validacao.py         funções de validação reaproveitadas
  opcoes.py            listas fixas (sintomas, gatilhos, categorias, canais de apoio)
  dados_iniciais.py    moderador, conteúdos e missões iniciais + usuário demo
  estruturas/          FilaMissoes (fila) e DiarioProgresso (pilha)
  modelos/             classes do domínio mapeadas no banco (camada de domínio + persistência)
  servicos/            regras de negócio (camada de serviço)
  rotas/               blueprints do Flask (camada de controle)
  templates/           páginas Jinja2 (camada de apresentação)
  static/              estilo.css e app.js
tests/                 testes com pytest
run.py                 inicia o servidor
seed.py                popula o banco
```

A separação segue o MVC em camadas descrito na seção 3.1 do documento: as rotas só recebem a requisição e chamam os serviços, e as regras ficam nos serviços e nos modelos, sem depender da tela.

## Onde está cada requisito técnico da entrega

### Pilares da orientação a objetos

| Conceito | Onde está no código |
|---|---|
| Herança | `Pessoa` → `Usuario` e `Moderador` (`app/modelos/pessoa.py`); `Missao` → `MissaoReflexiva`, `MissaoPratica` e `MissaoEducativa` (`app/modelos/missao.py`); `RegistroDiario` → `RegistroSintoma`, `RegistroRecaida` e `RegistroConquista` (`app/modelos/registro.py`) |
| Classes abstratas | As três classes base usam `@abstractmethod` do módulo `abc`. Tentar instanciar `Pessoa`, `Missao` ou `RegistroDiario` gera `TypeError`. Como o SQLAlchemy já tem uma metaclasse, foi preciso juntar ela com a `ABCMeta` em `app/modelos/base.py` |
| Polimorfismo | `exibir_painel()` e `perfil_acesso()` em Pessoa; `executar()`, `orientacao()`, `rotulo()`, `exige_resposta()`, `pode_ser_dia_um()` e `preencher()` nas missões; `resumo()`, `impacto()`, `rotulo()`, `criar_de_dados()`, `mensagem_confirmacao()` e `para_dict()` nos registros. Exemplo prático: `diario_servico.registrar_ocorrencia` usa `registro.impacto() < 0` para saber se foi recaída, sem testar o tipo da classe |
| Sobrescrita com `super()` | `preencher()` das missões e `para_dict()` dos registros chamam o método da classe mãe e completam com os campos próprios |
| Encapsulamento | `FilaMissoes` e `DiarioProgresso` escondem o `deque` e a `list` (atributos `_itens` e `_registros`); a senha só é mexida por `definir_senha()` e `autenticar()` |
| Composição 1:N | `Usuario` tem vários `ProgramaCessacao` e cada `ProgramaCessacao` tem vários `RegistroDiario`, com `cascade="all, delete-orphan"`: excluindo a conta, tudo vai junto (RF12) |
| Composição 1:1 | `ProgramaCessacao` monta a sua própria `FilaMissoes` (`montar_fila()`) e o seu próprio `DiarioProgresso` (`montar_diario()`) |
| Agregação | `ProgramaMissao` → `Missao`: as missões são um catálogo que existe sem o programa e é reaproveitado por todos |
| Associação simples | `Moderador` → `ConteudoInformativo` (publica) e `MissaoEducativa` → `ConteudoInformativo` (usa) |

### Estruturas de dados

- **Fila (FIFO)**: `app/estruturas/fila_missoes.py`, com `deque`. Enfileirar, desenfileirar e consultar são O(1). A ordem fica salva na coluna `posicao_fila` da tabela `programa_missao`.
- **Pilha (LIFO)**: `app/estruturas/diario_progresso.py`, com `list` operada pelo final. A ordem fica salva em `posicao_pilha` da tabela `registro_diario`, com `data_hora` de desempate.

As duas são remontadas a partir do banco a cada acesso, como descrito na seção 3.4 do documento.

### CRUDs

| Entidade | Create | Read | Update | Delete |
|---|---|---|---|---|
| Conteúdo informativo (moderador) | Novo conteúdo | Lista pública e página do texto | Editar | Excluir (bloqueado se uma missão usa o conteúdo) |
| Missão do catálogo (moderador) | Nova missão | Lista do catálogo | Editar | Excluir (bloqueado se a missão já está em algum programa) |
| Conta do usuário | Cadastro | Minha conta e exportação em JSON | Nome, senha e perfil de consumo | Excluir conta, apagando tudo em cascata |
| Programa de cessação | Novo programa | Painel, página do programa e histórico | Concluir e adiar missão, encerrar programa | Não tem exclusão avulsa: o programa encerrado fica no histórico (RN01) |
| Registro do diário | Novo registro | Diário e página de padrões | Complementar | Só junto com a conta (RN05) |

### Banco de dados

SQLite com SQLAlchemy, seguindo o DER da seção 5.2:

- Herança por tabelas separadas (joined) em `pessoa` → `usuario` / `moderador` e em `registro_diario` → `registro_sintoma` / `registro_recaida` / `registro_conquista`.
- Herança em tabela única na `missao`, com o discriminador `tipo_missao`.
- Chaves estrangeiras ligadas no SQLite (`PRAGMA foreign_keys = ON`, em `app/extensoes.py`).
- Datas gravadas no formato ISO-8601.
- `CHECK` no banco para a intensidade do sintoma ficar entre 1 e 5 (RN09).

Durante a implementação foram feitos alguns ajustes pequenos no DER:

| Tabela | Campo novo | Motivo |
|---|---|---|
| usuario | `tempo_uso_meses` | O RF03 pede "tempo de uso" e o DER não tinha o campo |
| usuario | `data_consentimento` | Guardar quando a pessoa aceitou o termo (RNF04 / LGPD) |
| missao | `duracao_min` | Estava no diagrama de classes (MissaoPratica) mas faltou no DER; é o tempo do cronômetro |
| programa_cessacao | `data_fim` | Saber quando o programa foi encerrado, usado no histórico e nos indicadores de dia 7 e dia 30 |
| programa_missao | `resposta` | Guardar a resposta das missões reflexivas, como o mapeamento de gatilhos do dia 1 |
| contador_acesso (nova) | `chave`, `total` | Contar acessos anônimos ao módulo informativo e cliques nos canais de apoio (indicadores da seção 2.3) sem guardar quem acessou |

### Regras de negócio

| Regra | Onde está | Teste |
|---|---|---|
| RN01 um programa ativo por vez | `programa_servico.criar_programa` | `test_rn01_*` |
| RN02 fila FIFO, dia 1 é o mapeamento de gatilhos | `programa_servico.criar_programa`, `missao_servico.salvar_missao` | `test_rn02_*` |
| RN03 só uma missão em andamento | `programa_servico.liberar_proxima` | `test_rn03_*` |
| RN04 registro mais recente no topo | `ProgramaCessacao.registrar` e `DiarioProgresso` | `test_rn04_*` |
| RN05 registro não é apagado, só complementado | `RegistroDiario.complementar` (não existe rota de exclusão) | `test_rn05_*` |
| RN06 recaída zera o contador mas guarda recorde e total | `diario_servico.registrar_ocorrencia`, `ProgramaCessacao.recorde_dias` | `test_rn06_*` |
| RN07 3 recaídas em 7 dias destacam os canais de apoio | `diario_servico.precisa_alerta_apoio` | `test_rn07_*` |
| RN08 economia = (dias sem nicotina / 7) x custo semanal | `Usuario.calcular_economia` | `test_rn08_*` |
| RN09 intensidade inteira de 1 a 5 | `RegistroSintoma._validar_intensidade` e CHECK no banco | `test_rn09_*` |
| RN10 só moderador publica e a fonte é obrigatória | `Moderador.publicar`, `conteudo_servico.salvar_conteudo` | `test_rn10_*`, `test_moderador_crud_de_conteudo` |
| RN11 sem diagnóstico ou prescrição | Aviso fixo no rodapé e em cada conteúdo | - |

Sobre o RF09: quando a pessoa registra uma recaída, a missão que estava em andamento volta para o fim da fila (para ser tentada de novo depois) e a próxima é liberada. As missões já concluídas continuam concluídas, então o progresso não é zerado.

### Matérias informativas

São 20 matérias em 11 categorias. As 12 mais recentes falam dos malefícios do cigarro eletrônico, e cada uma é baseada em um estudo publicado. A referência completa aparece no fim da matéria, e o texto explica também os limites de cada estudo.

| Matéria | Estudo usado |
|---|---|
| Pulmão de pipoca: o diacetil escondido nos sabores | Allen et al., Environmental Health Perspectives, 2016 |
| Chumbo, níquel e cromo: os metais que saem da resistência | Olmedo et al., Environmental Health Perspectives, 2018 |
| Tosse e bronquite em adolescentes que usam pod | McConnell et al., Am. J. Respir. Crit. Care Med., 2017 |
| O que o pod faz com o coração de quem usa todo dia | Moheimani et al., JAMA Cardiology, 2017 |
| Cáries: o pod também deixa marca na boca | Irusa et al., Journal of the American Dental Association, 2022 |
| Pod causa câncer? O que já se sabe e o que ainda não | Tang et al., PNAS, 2019 |
| Quem começa no pod tem mais chance de fumar cigarro depois | Soneji et al., JAMA Pediatrics, 2017 |
| Sabor de fruta e de bala: a isca para atrair jovens | CDC, MMWR, National Youth Tobacco Survey 2024 |
| Uso de pod entre adolescentes quase dobrou no Brasil | IBGE, PeNSE 2019 e 2024; Covitel 2023 |
| Explosões e queimaduras: o risco que vem da bateria | Rossheim et al., Tobacco Control, 2019 |
| Refil perto de criança é perigo: intoxicação por nicotina | Govindarajan et al., Pediatrics, 2018 |
| Mitos e verdades sobre o pod | OMS, INCA e os estudos acima |

O moderador escreve as matérias em texto simples. Uma linha começando com `## ` vira subtítulo, linhas começando com `- ` viram lista, e uma linha em branco separa os parágrafos. A conversão fica em `app/formatacao.py` e passa tudo pelo escape, então não dá para colocar HTML ou script no conteúdo.

### Segurança e privacidade

- Senha só em hash (Werkzeug).
- Diário visível apenas para o dono: tentar abrir o registro de outra pessoa retorna 404.
- Rotas separadas por perfil (`perfil_requerido` em `app/rotas/acesso.py`); usuário comum tentando entrar na moderação recebe 403.
- Token CSRF em todos os formulários.
- Coleta mínima: só apelido e e-mail, com consentimento explícito no cadastro.
- Exportação dos dados em JSON e exclusão total da conta (RF12).

Em produção a `SECRET_KEY` deve ser definida por variável de ambiente.

## Divisão do trabalho

| Sprint | Épico | Responsável |
|---|---|---|
| Sprint 1 (15/09 a 28/09) | Domínio e autenticação (RF01, RF03) | Matheus |
| Sprint 2 (29/09 a 12/10) | Motor de missões / fila (RF05) | Bruno |
| Sprint 3 (13/10 a 26/10) | Diário de progresso / pilha (RF06) | Vinicius |
| Sprint 4 (27/10 a 09/11) | Cálculos, alertas e persistência (RF07, RF08) | Matheus, Bruno e Vinicius |
