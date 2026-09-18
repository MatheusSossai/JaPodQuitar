"""Conteudo do modulo informativo aberto (RF02, RF11)."""


class ConteudoInformativo:
    """Texto publicado por um moderador; o campo fonte e obrigatorio (RNF05)."""

    def __init__(
        self,
        id: int | None,
        titulo: str,
        corpo: str,
        fonte: str,
        categoria: str = "geral",
    ) -> None:
        self.id = id
        self.titulo = titulo
        self.corpo = corpo
        self.fonte = fonte
        self.categoria = categoria

    def resumir(self, limite: int = 180) -> str:
        """Trecho usado nas listagens.

        TODO (Sprint 2): cortar por palavra inteira, nao por caractere.
        """
        raise NotImplementedError
