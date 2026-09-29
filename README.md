# PixelPet Desktop

Um Desktop Pet/Tamagotchi em pixel art para Windows, feito em Python com
Pygame. Fica numa janela compacta e sempre visível, guarda o progresso
automaticamente e reage aos teus cuidados com um sistema de carma.

## Estrutura do projeto

```
pixelpet/
├── main.py             # ponto de entrada do Desktop Pet
├── desktop_pet.py      # janela compacta, sempre visível, e ações do pet
├── game.py             # versão original, em janela de jogo maior
├── pet.py               # classe Pet — atributos, ações e sistema de carma
├── sprites.py           # pixel art (sprites como matrizes) + desenho no ecrã
├── data_manager.py      # guardar/carregar o progresso em JSON
├── stats.py              # gráfico da evolução do carma (matplotlib)
├── requirements.txt
├── tests/
│   └── test_pet.py      # testes unitários à classe Pet
└── dados/                # criado automaticamente: save + gráfico gerado
```

## Como instalar e correr

```powershell
pip install -r requirements.txt
python main.py
```

### Configurar Firebase

1. Cria um projeto em [Firebase Console](https://console.firebase.google.com/) e ativa **Realtime Database**.
2. Em **Project settings > Service accounts**, gera e descarrega uma chave privada JSON.
3. Copia `.env.example` para `.env` e preenche a URL e o caminho do JSON.
4. Em **Realtime Database > Data**, copia a URL apresentada no topo e coloca-a
   em `FIREBASE_DATABASE_URL`. Nao uses o email `firebase-adminsdk-...`.
5. Inicia o jogo:

```powershell
python main.py
```

O pet e o ovo sao guardados na Firebase ao receber cuidados, a cada atualizacao
e ao fechar a aplicacao. Nunca publiques o ficheiro JSON de credenciais.

No Windows, a janela mantém-se no topo e pode ser deslocada com a barra de
título.

## Como jogar

| Botão | Efeito |
|---|---|
| Comer | Aumenta a saciedade e o carma |
| Brincar | Aumenta o carma, mas consome energia e saciedade |
| Limpar | Repõe a higiene ao máximo |
| Dormir | Alterna entre acordado/a dormir; recupera energia |

De tempos a tempos, o pet recebe um pequeno evento aleatório: pode encontrar
um presente, sentir uma brisa fresca ou precisar de atenção depois de um
pesadelo.

Se ignorares o pet durante muito tempo (fome e energia a zero), ele
"foge" por negligência — fim de jogo.

## Correr os testes

```powershell
python -m unittest discover -s tests -v
```

## Conceitos usados (para o relatório)

- **POO**: classes `Pet`, `Jogo`, `Botao`, `GestorAnimacao`, `GestorDados`
- **Estruturas de dados**: dicionários (atributos, paleta de cores), listas
  de listas (sprites), lista de tuplos (histórico de carma)
- **Condicionais**: lógica de estados do pet, regras de ganho/perda de carma
- **Ciclos**: `for` a desenhar cada sprite, `while` no loop principal do jogo
- **Ficheiros**: leitura/escrita em JSON (`data_manager.py`)
- **Bibliotecas**: `pygame`, `matplotlib`, `json`, `datetime`, `random` (eventos futuros), `unittest`
- **Gráfico**: evolução do carma ao longo do tempo (`stats.py`)
