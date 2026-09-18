# Arquitetura

Resumo operacional da seção 3 do documento de concepção. O documento completo
está em `docs/entrega-1/`.

## Estilo

Cliente-servidor, monólito modular em camadas, padrão MVC.

| Camada | Pasta | Responsabilidade |
|---|---|---|
| Apresentação | `app/templates`, `app/static` | Renderização Jinja2 e estilos |
| Controle | `app/controladores` | Rotas (blueprints); sem regra de negócio |
| Serviço | `app/servicos` | Regras RN01 a RN11 |
| Repositório | `app/repositorios` | Único ponto de acesso ao banco |
| Domínio | `app/dominio` | Classes de negócio, fila e pilha |
| Persistência | `app/modelos` | Mapeamento ORM das tabelas do DER |

## Regra de dependência

O fluxo de chamadas é sempre `controlador -> serviço -> repositório -> modelo`.
A camada de domínio não importa Flask nem SQLAlchemy, o que permite testá-la
isoladamente (RNF06).

## Estruturas de dados

- `FilaMissoes` (`collections.deque`) governa a ordem de entrega das missões
  (RN02, RN03). Persistida em `programa_missao.posicao_fila`.
- `DiarioProgresso` (`list`) governa a leitura do histórico (RN04). Persistida
  em `registro_diario.posicao_pilha`, com `data_hora` como desempate.
