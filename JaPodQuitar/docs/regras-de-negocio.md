# Regras de negócio e onde elas vivem no código

| Regra | Implementação prevista | Teste |
|---|---|---|
| RN01 Um programa ativo por vez | `servicos/servico_programa.py` | `testes/unidade/test_regras_negocio.py` |
| RN02 Fila FIFO; dia 1 é o mapeamento de gatilhos | `dominio/estruturas/fila_missoes.py` | `testes/unidade/test_fila_missoes.py` |
| RN03 Só uma missão em andamento | `servicos/servico_missoes.py` | `testes/unidade/test_regras_negocio.py` |
| RN04 Pilha LIFO no diário | `dominio/estruturas/diario_progresso.py` | `testes/unidade/test_diario_progresso.py` |
| RN05 Registro não é apagado individualmente | `servicos/servico_privacidade.py` | `testes/unidade/test_regras_negocio.py` |
| RN06 Recaída zera o contador, preserva o recorde | `servicos/servico_metricas.py` | `testes/unidade/test_regras_negocio.py` |
| RN07 Três recaídas em sete dias destacam o apoio | `servicos/servico_metricas.py` | `testes/unidade/test_regras_negocio.py` |
| RN08 Economia = (dias ÷ 7) × custo semanal | `dominio/pessoa.py`, `servicos/servico_metricas.py` | `testes/unidade/test_regras_negocio.py` |
| RN09 Intensidade de 1 a 5 | `utils/validadores.py` | `testes/unidade/test_regras_negocio.py` |
| RN10 Publicação só com fonte e perfil moderador | `servicos/servico_conteudo.py` | `testes/unidade/test_regras_negocio.py` |
| RN11 Sem diagnóstico nem prescrição | `templates/componentes/_rodape.html` | revisão manual |
