# Teste Técnico - Projeto

Projeto em Python usando **Streamlit** e **SQLite**, com opção de rodar via Docker.

---

## Pré-requisitos

- Python 3.x
- pip
- Docker (opcional)

---

## Setup Local

1. **Entre na pasta `src/`**:

```bash
cd src
```

2. **Crie e ative o ambiente virtual dentro de `src/`**:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Crie o banco de dados:**

```bash
python model/db.py
```

5. **(Opcional) Popule com dados fictícios:**

```bash
python model/seed.py
```

6. **Execute a aplicação:**

```bash
streamlit run main.py
```

> A aplicação estará disponível em `http://localhost:8501`.

---

## Setup via Docker (Opcional)

1. **Suba o container (com dados fictícios):**

```bash
docker compose up 
```

2. **Acesse a aplicação em:**

```
http://localhost:8501
```

> O container usa `src/` como diretório de trabalho, então qualquer alteração no código é refletida automaticamente.

---

## Estrutura do Projeto

```
.
├── docker-compose.yml
├── src/
│   ├── main.py
│   ├── model/
│   │   ├── db.py
│   │   ├── db_functions.py
│   │   └── seed.py
│   ├── Dockerfile
│   └── requirements.txt
```

---

## Observações

- **Banco SQLite:** Arquivo `db.sqlite` será criado automaticamente em `src/` ao rodar `db.py`.
- **Streamlit:** A porta padrão é `8501`, mas pode ser alterada no Docker ou diretamente no comando `streamlit run`.

