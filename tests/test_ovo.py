"""Testes unitarios do ciclo de incubacao."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ovo import Ovo


class TestOvo(unittest.TestCase):
    def test_ovo_choca_depois_de_tres_cuidados(self):
        ovo = Ovo("Luna")
        for _ in range(3):
            ovo.incubar()

        pet = ovo.chocar()
        self.assertTrue(ovo.pronto_a_chocar)
        self.assertEqual(pet.nome, "Luna")

    def test_ovo_nao_choca_antes_de_estar_pronto(self):
        ovo = Ovo("Luna")
        with self.assertRaises(ValueError):
            ovo.chocar()

    def test_ovo_mantem_progresso_ao_ser_reconstruido(self):
        ovo = Ovo("Luna")
        ovo.incubar()
        ovo_reconstruido = Ovo.a_partir_de_dicionario(ovo.para_dicionario())
        self.assertEqual(ovo_reconstruido.nome_pet, "Luna")
        self.assertEqual(ovo_reconstruido.cuidados, 1)


if __name__ == "__main__":
    unittest.main()