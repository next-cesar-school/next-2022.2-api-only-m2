<h1 align=”center”>
<img src="https://user-images.githubusercontent.com/114358060/204836563-4e83015b-e414-44ba-b595-5d091d273ce4.png" width="100px">
</h1>


## Descrição do Projeto 
<p align=”center”>O programa permite realizar o armazenamento e a comparação de imagens, identificando a de maior similaridade.</p>


> Status do Projeto: Concluido :heavy_check_mark:

## Linguagens e libs utilizadas :books:

- Python: versão 3.11.0 

### Features

- [x] Adição de Imagem
- [x] Comparação de Imagens
- [x] Imagem mais similar
- [x] Remoção de Imagem

### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
[Git](https://git-scm.com) e [Python](https://www.python.org/downloads/). 

Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/) ou [Pycharm](https://www.jetbrains.com/pt-br/pycharm/)

### 🎲 Rodando o Back End (servidor)

```bash
# Clone este repositório
$ git clone <https://github.com/next-cesar-school/next-2022.2-api-only-m2.git>

# Acesse a pasta do projeto no terminal/cmd
$ cd next-2022.2-api-only-m2

# Crie um ambiente virtual
$ python -m venv .venv

# Ative o ambiente virtual
$ source venv/Scripts/activate

# Instale as dependências
$ pip install -r requirements.txt

# Inicie a aplicação
$ uvicorn main:app --reload

# O servidor inciará na porta:8000 - acesse <http://localhost:8000/docs>


