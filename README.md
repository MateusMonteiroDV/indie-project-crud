# Teste Técnico - Projeto

Projeto em Python com Streamlit e SQLite, com opção de rodar via Docker.

## Pré-requisitos

- Python 3.x
- pip
- Docker (opcional)

## Setup Local

1. Criar e ativar ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Criar banco de dados:
```bash
python model/db.py
```

4. (Opcional) Inserir dados fictícios:
```bash
python model/seed.py
```

5. Rodar aplicação:
```bash
streamlit run main.py
```

> Todos os comandos devem ser executados dentro da pasta `src`.

## Setup via Docker (Opcional)

Subir container com dados fictícios:
```bash
docker compose up
```

## Estrutura do Projeto

```
.
.
├── docker-compose.yml
├── src/
│   ├── main.py
│   ├── model/
│   │   ├── db.py
|   |   ├── db_functions.py
│   │   └── seed.py
│   ├── Dockerfile
│   └── requirements.txt

