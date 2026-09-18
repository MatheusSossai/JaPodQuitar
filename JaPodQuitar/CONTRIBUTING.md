# Como contribuir

## Ramos

| Ramo | Para que serve |
|---|---|
| `main` | Apenas versões estáveis. Ninguém escreve direto aqui. |
| `develop` | Integração do time. Recebe os pull requests. |
| `feature/nome-da-funcionalidade` | Uma funcionalidade por ramo, criada a partir de `develop`. |

```bash
git checkout develop
git pull
git checkout -b feature/motor-de-missoes
```

## Commits semânticos

| Prefixo | Uso |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção |
| `docs` | Documentação |
| `refactor` | Reestruturação sem mudança de comportamento |
| `test` | Testes |

Exemplo: `feat: entrega das missoes uma a uma pela fila (RF05)`

## Pull request

Abra o PR de `feature/...` para `develop`. É obrigatória a revisão de ao menos
um integrante que não seja o autor. O PR só entra com a suíte de testes passando.

## Onde escrever cada coisa

Regra de negócio vai para `app/servicos`. Consulta ao banco vai para
`app/repositorios`. Rota não decide nada: recebe, chama o serviço e devolve o
template. Quem quebra essa separação quebra o RNF06.
