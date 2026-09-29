"""Modelo de um ovo que pode ser incubado antes de nascer um PixelPet."""

from pet import Pet


class Ovo:
    """Representa o primeiro ciclo de vida de um pet."""

    CUIDADOS_NECESSARIOS = 3

    def __init__(self, nome_pet: str):
        self.nome_pet = nome_pet
        self.cuidados = 0

    @property
    def pronto_a_chocar(self) -> bool:
        return self.cuidados >= self.CUIDADOS_NECESSARIOS

    def incubar(self) -> str:
        if self.pronto_a_chocar:
            return "O ovo esta pronto para chocar!"
        self.cuidados += 1
        if self.pronto_a_chocar:
            return "O ovo esta a abanar. Ja pode chocar!"
        return f"O ovo recebeu calor ({self.cuidados}/{self.CUIDADOS_NECESSARIOS})."

    def chocar(self) -> Pet:
        if not self.pronto_a_chocar:
            raise ValueError("O ovo ainda precisa de mais cuidados.")
        return Pet(self.nome_pet)

    def para_dicionario(self) -> dict:
        return {"nome_pet": self.nome_pet, "cuidados": self.cuidados}

    @classmethod
    def a_partir_de_dicionario(cls, dados: dict) -> "Ovo":
        ovo = cls(dados["nome_pet"])
        ovo.cuidados = dados.get("cuidados", 0)
        return ovo