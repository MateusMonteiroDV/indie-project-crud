import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("estoque.db")
c = conn.cursor()

# Produtos com nomes SEM ACENTO
produtos = [
    ("macarrao", 85, 4.90),
    ("farinha", 120, 5.30),
    ("miojo", 320, 2.40)
]

for nome, qtd, preco in produtos:
    c.execute("""
        INSERT OR IGNORE INTO produtos (nome, quantidade, preco) 
        VALUES (?, ?, ?)
    """, (nome, qtd, preco))

conn.commit()

c.execute("SELECT id, nome FROM produtos WHERE nome IN ('macarrao', 'farinha', 'miojo')")
produtos_ids = {row[1]: row[0] for row in c.fetchall()}

if len(produtos_ids) != 3:
    print("Aviso: Nem todos os produtos foram encontrados no banco!")
    print("Produtos encontrados:", produtos_ids.keys())

def gerar_movimentacoes(produto_id, dias_atras, quantidade_media_diaria, variacao):
    data_atual = datetime.now()
    movimentacoes = []
    
    for i in range(dias_atras):
        data = data_atual - timedelta(days=i)
        qtd = round(random.gauss(quantidade_media_diaria, variacao))
        qtd = max(1, qtd)  
        movimentacoes.append((produto_id, qtd, data))
    
    return movimentacoes

todas_mov = []

todas_mov.extend(gerar_movimentacoes(produtos_ids["macarrao"], 180, 3.1, 1.2))
todas_mov.extend(gerar_movimentacoes(produtos_ids["macarrao"], 90, 3.4, 1.3))
todas_mov.extend(gerar_movimentacoes(produtos_ids["macarrao"], 30, 3.8, 1.4))

todas_mov.extend(gerar_movimentacoes(produtos_ids["farinha"], 90, 2.5, 1.0))
todas_mov.extend(gerar_movimentacoes(produtos_ids["farinha"], 30, 2.9, 1.1))

todas_mov.extend(gerar_movimentacoes(produtos_ids["miojo"], 90, 14.0, 5.0))
todas_mov.extend(gerar_movimentacoes(produtos_ids["miojo"], 30, 16.5, 5.5))

c.executemany(
    "INSERT INTO movimentacoes (produto_id, quantidade, data) VALUES (?, ?, ?)",
    todas_mov
)

conn.commit()
conn.close()

print("Produtos e movimentações adicionados com sucesso.")
print("Nomes usados no banco:", [p[0] for p in produtos])
