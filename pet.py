"""
pet.py
Contém a classe Pet: o "cérebro" do PixelPet.
Guarda os atributos (fome, energia, higiene, carma) e a lógica
de como eles reagem às ações do jogador e à passagem do tempo.
"""

from datetime import datetime
import random


class Pet:
    """Representa o animal de estimação virtual."""

    # Limites usados em vários sítios (evita "números mágicos" espalhados)
    MIN_VALOR = 0
    MAX_VALOR = 100

    def __init__(self, nome: str):
        self.nome = nome
        self.fome = 70          # 100 = totalmente saciado, 0 = esfomeado
        self.energia = 70       # 100 = cheio de energia, 0 = exausto
        self.higiene = 70       # 100 = impecável, 0 = imundo
        self.carma = 50         # 0 = odeia-te, 100 = adora-te
        self.vivo = True
        self.a_dormir = False
        self.criado_em = datetime.now().isoformat(timespec="seconds")

        # Histórico do carma: lista de tuplos (timestamp, valor)
        # Uma estrutura de dados simples que alimenta o gráfico mais tarde.
        self.historico_carma = [(self.criado_em, self.carma)]

    # ------------------------------------------------------------------
    # Utilitário interno
    # ------------------------------------------------------------------
    def _limitar(self, valor: float) -> int:
        """Garante que um atributo fica sempre entre MIN_VALOR e MAX_VALOR."""
        return max(self.MIN_VALOR, min(self.MAX_VALOR, int(valor)))

    def _registar_carma(self):
        agora = datetime.now().isoformat(timespec="seconds")
        self.historico_carma.append((agora, self.carma))

    def _ajustar_carma(self, delta: int):
        self.carma = self._limitar(self.carma + delta)
        self._registar_carma()

    # ------------------------------------------------------------------
    # Ações do jogador
    # ------------------------------------------------------------------
    def alimentar(self):
        if not self.vivo or self.a_dormir:
            return "O pet não pode comer agora."

        if self.fome >= 90:
            # Alimentar em excesso é mau para o carma (fartura!)
            self._ajustar_carma(-5)
            return f"{self.nome} já está cheio e não gostou de ser forçado a comer."

        self.fome = self._limitar(self.fome + 25)
        self._ajustar_carma(+4)
        return f"{self.nome} comeu e ficou contente!"

    def brincar(self):
        if not self.vivo or self.a_dormir:
            return "O pet não pode brincar agora."

        if self.energia < 15:
            self._ajustar_carma(-3)
            return f"{self.nome} está exausto demais para brincar."

        self.energia = self._limitar(self.energia - 15)
        self.fome = self._limitar(self.fome - 5)
        self._ajustar_carma(+6)
        return f"{self.nome} brincou muito e adorou!"

    def limpar(self):
        if not self.vivo:
            return "Já não há nada a fazer."

        self.higiene = self.MAX_VALOR
        self._ajustar_carma(+3)
        return f"{self.nome} está limpinho outra vez!"

    def dormir(self):
        if not self.vivo:
            return "Já não há nada a fazer."

        self.a_dormir = not self.a_dormir
        if self.a_dormir:
            return f"{self.nome} foi dormir."
        self.energia = self._limitar(self.energia + 30)
        self._ajustar_carma(+2)
        return f"{self.nome} acordou revigorado!"

    def repreender(self):
        """Ação negativa: reduz bastante o carma."""
        if not self.vivo:
            return "Já não há nada a fazer."

        self._ajustar_carma(-10)
        return f"{self.nome} ficou triste e assustado."

    def evento_aleatorio(self, evento: str | None = None) -> str:
        """Aplica um pequeno acontecimento inesperado ao pet."""
        if not self.vivo:
            return "Já não há nada a fazer."

        evento = evento or random.choice(("presente", "brisa", "pesadelo"))
        if evento == "presente":
            self._ajustar_carma(+8)
            return f"{self.nome} encontrou um presente e ficou radiante!"
        if evento == "brisa":
            self.higiene = self._limitar(self.higiene + 15)
            self._ajustar_carma(+2)
            return f"Uma brisa fresca deixou {self.nome} mais confortável."
        if evento == "pesadelo":
            self._ajustar_carma(-3)
            return f"{self.nome} teve um pesadelo e precisa de atenção."
        raise ValueError(f"Evento desconhecido: {evento}")

    # ------------------------------------------------------------------
    # Passagem do tempo (chamado periodicamente pelo ciclo do jogo)
    # ------------------------------------------------------------------
    def atualizar_estado(self):
        """Degrada os atributos com o tempo, como num Tamagochi real."""
        if not self.vivo:
            return

        if self.a_dormir:
            self.energia = self._limitar(self.energia + 1)
            self.fome = self._limitar(self.fome - 1)
        else:
            self.fome = self._limitar(self.fome - 2)
            self.energia = self._limitar(self.energia - 1)
            self.higiene = self._limitar(self.higiene - 1)

        # Negligência prolongada penaliza o carma
        if self.fome <= 10 or self.higiene <= 10 or self.energia <= 5:
            self._ajustar_carma(-2)

        # Morte por negligência extrema
        if self.fome <= 0 and self.energia <= 0:
            self.vivo = False
            self._ajustar_carma(-20)

    # ------------------------------------------------------------------
    # Estado atual (usado pelo módulo de sprites para escolher a imagem)
    # ------------------------------------------------------------------
    def estado_atual(self) -> str:
        """Devolve uma string simples que descreve o estado visual do pet."""
        if not self.vivo:
            return "morto"
        if self.a_dormir:
            return "a_dormir"
        if self.fome <= 20:
            return "esfomeado"
        if self.higiene <= 20:
            return "sujo"
        if self.carma >= 80:
            return "muito_feliz"
        if self.carma <= 20:
            return "triste"
        return "normal"

    def nivel_carma_texto(self) -> str:
        if self.carma >= 80:
            return "Ama-te"
        if self.carma >= 50:
            return "Gosta de ti"
        if self.carma >= 20:
            return "Desconfiado"
        return "Ressentido"

    # ------------------------------------------------------------------
    # Serialização (para gravar/carregar em ficheiro)
    # ------------------------------------------------------------------
    def para_dicionario(self) -> dict:
        return {
            "nome": self.nome,
            "fome": self.fome,
            "energia": self.energia,
            "higiene": self.higiene,
            "carma": self.carma,
            "vivo": self.vivo,
            "a_dormir": self.a_dormir,
            "criado_em": self.criado_em,
            "historico_carma": self.historico_carma,
        }

    @classmethod
    def a_partir_de_dicionario(cls, dados: dict) -> "Pet":
        pet = cls(dados["nome"])
        pet.fome = dados.get("fome", 70)
        pet.energia = dados.get("energia", 70)
        pet.higiene = dados.get("higiene", 70)
        pet.carma = dados.get("carma", 50)
        pet.vivo = dados.get("vivo", True)
        pet.a_dormir = dados.get("a_dormir", False)
        pet.criado_em = dados.get("criado_em", pet.criado_em)
        pet.historico_carma = dados.get("historico_carma", pet.historico_carma)
        return pet
