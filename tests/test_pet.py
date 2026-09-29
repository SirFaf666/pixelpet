"""
tests/test_pet.py
Testes unitários às principais funcionalidades da classe Pet.
Correr com:  python3 -m unittest discover -s tests -v   (a partir da pasta do projeto)
"""

import unittest
import sys
import os

# Garante que conseguimos importar o pet.py que está na pasta principal do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pet import Pet


class TestPet(unittest.TestCase):

    def setUp(self):
        """Corre antes de cada teste: cria um pet "limpo" para testar."""
        self.pet = Pet(nome="TesteBot")

    def test_criacao_pet_tem_valores_iniciais_corretos(self):
        self.assertEqual(self.pet.nome, "TesteBot")
        self.assertEqual(self.pet.fome, 70)
        self.assertEqual(self.pet.energia, 70)
        self.assertEqual(self.pet.higiene, 70)
        self.assertEqual(self.pet.carma, 50)
        self.assertTrue(self.pet.vivo)

    def test_alimentar_aumenta_fome_e_carma(self):
        fome_antes = self.pet.fome
        carma_antes = self.pet.carma
        self.pet.alimentar()
        self.assertGreater(self.pet.fome, fome_antes)
        self.assertGreater(self.pet.carma, carma_antes)

    def test_alimentar_com_fome_cheia_penaliza_carma(self):
        self.pet.fome = 95
        carma_antes = self.pet.carma
        self.pet.alimentar()
        self.assertLess(self.pet.carma, carma_antes)

    def test_brincar_reduz_energia_e_aumenta_carma(self):
        energia_antes = self.pet.energia
        carma_antes = self.pet.carma
        self.pet.brincar()
        self.assertLess(self.pet.energia, energia_antes)
        self.assertGreater(self.pet.carma, carma_antes)

    def test_limpar_repoe_higiene_ao_maximo(self):
        self.pet.higiene = 10
        self.pet.limpar()
        self.assertEqual(self.pet.higiene, Pet.MAX_VALOR)

    def test_repreender_reduz_carma_significativamente(self):
        carma_antes = self.pet.carma
        self.pet.repreender()
        self.assertEqual(self.pet.carma, carma_antes - 10)

    def test_evento_presente_aumenta_o_carma(self):
        carma_antes = self.pet.carma
        mensagem = self.pet.evento_aleatorio("presente")
        self.assertEqual(self.pet.carma, carma_antes + 8)
        self.assertIn("presente", mensagem)

    def test_evento_desconhecido_da_erro(self):
        with self.assertRaises(ValueError):
            self.pet.evento_aleatorio("invalido")

    def test_valores_nunca_ultrapassam_limites(self):
        self.pet.fome = 100
        for _ in range(10):
            self.pet.alimentar()
        self.assertLessEqual(self.pet.fome, Pet.MAX_VALOR)
        self.assertGreaterEqual(self.pet.fome, Pet.MIN_VALOR)

    def test_atualizar_estado_degrada_atributos_quando_acordado(self):
        fome_antes = self.pet.fome
        self.pet.atualizar_estado()
        self.assertLess(self.pet.fome, fome_antes)

    def test_pet_morre_por_negligencia_extrema(self):
        self.pet.fome = 0
        self.pet.energia = 0
        self.pet.atualizar_estado()
        self.assertFalse(self.pet.vivo)

    def test_estado_atual_reflete_condicao_do_pet(self):
        self.pet.fome = 5
        self.assertEqual(self.pet.estado_atual(), "esfomeado")

    def test_serializacao_e_reconstrucao_mantêm_dados(self):
        self.pet.carma = 77
        dados = self.pet.para_dicionario()
        pet_novo = Pet.a_partir_de_dicionario(dados)
        self.assertEqual(pet_novo.carma, 77)
        self.assertEqual(pet_novo.nome, "TesteBot")


if __name__ == "__main__":
    unittest.main()
