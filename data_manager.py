"""Persistencia do PixelPet na Firebase Realtime Database."""

import os

import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

from pet import Pet
from ovo import Ovo

class GestorDados:
    """Guarda e recupera o estado do jogador na Firebase."""

    _app = None # Instância da aplicação Firebase, inicializada apenas uma vez.
    

    @classmethod
    def _referencia(cls, colecao: str):
        if cls._app is None:
            load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)
            url = os.environ.get("FIREBASE_DATABASE_URL")
            caminho_credenciais = os.environ.get("FIREBASE_CREDENTIALS_PATH")
            if not url or not caminho_credenciais:
                raise RuntimeError(
                    "Configura FIREBASE_DATABASE_URL e FIREBASE_CREDENTIALS_PATH antes de iniciar o jogo."
                )
            # Permite caminhos relativos, resolvidos a partir da pasta do projeto,
            # para o .env funcionar em qualquer computador.
            if not os.path.isabs(caminho_credenciais):
                caminho_credenciais = os.path.join(os.path.dirname(__file__), caminho_credenciais)
            if not os.path.isfile(caminho_credenciais):
                raise RuntimeError("O ficheiro de credenciais Firebase nao foi encontrado.")
            cls._app = firebase_admin.initialize_app(
                credentials.Certificate(caminho_credenciais),
                {"databaseURL": url},
            )

        utilizador = os.environ.get("FIREBASE_USER_ID", "jogador_local")
        return db.reference(f"pixelpet/{utilizador}/{colecao}", app=cls._app)

    @classmethod
    def guardar(cls, pet: Pet):
        cls._referencia("pet").set(pet.para_dicionario())  # cls é a classe GestorDados

    @classmethod
    def existe_save(cls) -> bool:
        return cls._referencia("pet").get() is not None

    @classmethod
    def carregar(cls) -> Pet:
        dados = cls._referencia("pet").get()
        if dados is None:
            raise FileNotFoundError("Nao existe nenhum pet guardado na Firebase.")
        return Pet.a_partir_de_dicionario(dados)

    @classmethod
    def apagar_save(cls):
        cls._referencia("pet").delete()

    @classmethod
    def guardar_ovo(cls, ovo: Ovo):
        cls._referencia("ovo").set(ovo.para_dicionario())

    @classmethod
    def existe_ovo(cls) -> bool:
        return cls._referencia("ovo").get() is not None

    @classmethod
    def carregar_ovo(cls) -> Ovo:
        dados = cls._referencia("ovo").get()
        if dados is None:
            raise FileNotFoundError("Nao existe nenhum ovo guardado na Firebase.")
        return Ovo.a_partir_de_dicionario(dados)

    @classmethod
    def apagar_ovo(cls):
        cls._referencia("ovo").delete()