# Requisitos

Espelho enxuto dos quadros 3 e 4 do documento de concepção, para consulta
durante a implementação. A versão oficial está em `docs/entrega-1/`.

## Funcionais

| Código | Descrição | Sprint |
|---|---|---|
| RF01 | Cadastro e autenticação com e-mail e senha | 1 |
| RF02 | Módulo informativo aberto, com fonte obrigatória | 2 |
| RF03 | Perfil de consumo inicial | 1 |
| RF04 | Programa de cessação com meta de dias | 1 |
| RF05 | Missões diárias entregues uma a uma | 2 |
| RF06 | Diário de sintomas, recaídas e conquistas | 3 |
| RF07 | Dias sem nicotina e economia financeira | 4 |
| RF08 | Resumo de padrões de consumo | 4 |
| RF09 | Recaída sem zerar o progresso registrado | 3 |
| RF10 | Canais oficiais de apoio | 4 |
| RF11 | Publicação de conteúdo pelo moderador | 2 |
| RF12 | Exportar ou excluir dados pessoais | 4 |

## Não funcionais

| Código | Onde é verificado |
|---|---|
| RNF01 Usabilidade | Templates responsivos; no máximo três toques até o diário |
| RNF02 Linguagem | Revisão de texto em `app/templates` |
| RNF03 Segurança | `ServicoAutenticacao`, hash do Werkzeug |
| RNF04 Privacidade | `ServicoPrivacidade`, consentimento no cadastro |
| RNF05 Confiabilidade | Campo `fonte` obrigatório em `conteudo_informativo` |
| RNF06 Manutenibilidade | Separação em camadas + suíte em `testes/` |
| RNF07 Desempenho | Consultas do painel abaixo de dois segundos |
