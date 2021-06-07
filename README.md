# Desafio Python  

### Aplicação para consulta e arquivamento de registros da previsão do tempo de determinada cidade.


### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
[Git](https://git-scm.com), [Python 3.8.10](https://www.python.org/downloads/), [Docker](https://www.docker.com/products/docker-desktop). 
Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)

### 🎲 Rodando o Projeto

```bash
# Clone este repositório
$ git clone <https://github.com/esferrari/desafio_python.git>

# Acesse a pasta do projeto no terminal/cmd
$ cd desafio_python

# Instale as dependências
$ pip install -r requirements.txt

# Com docker iniciado executar comando para inicio do banco de dados
$ docker-compose up

# Execute a aplicação em modo de desenvolvimento
$ uvicorn main:app --reload

# O servidor inciará na porta:8000 - acesse <http://127.0.0.1:8000>

# Após o inicio do servidor acesse a documentação - <http://127.0.0.1:8000/docs>
```

### 🛠 Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [PosgreSQL](https://www.postgresql.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Insomnia](https://insomnia.rest/)
- [Beekeeper Studio](https://www.beekeeperstudio.io/)

### ‼️ Explicação dependências usadas

<ul>
  <li>FastAPI - Escolhida devido a simplicidade e facilidade de implementação. Também pelo fato de vir com documentação embutida através do /docs.</li>
  <li>Docker - Escolhido para evitar a instalação do banco de dados postgreSQL localmente, utilizando container da imagem oficial postgres e tornando o manuseio do o banco de      dados mais simples e rapido. </li>
</ul>


