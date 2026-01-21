import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect("estoque.db")

def add_product(nome, quantidade, preco):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
    produto_id = c.lastrowid
    c.execute("INSERT INTO movimentacoes (produto_id, quantidade) VALUES (?, ?)", (produto_id, quantidade))
    conn.commit()
    conn.close()

def get_products():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM produtos", conn)
    conn.close()
    return df

def add_stock(product_id, quantidade):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, product_id))
    c.execute("INSERT INTO movimentacoes (produto_id, quantidade) VALUES (?, ?)", (product_id, quantidade))
    conn.commit()
    conn.close()

def get_stock_history():
    conn = get_connection()
    
    query = """
    WITH todas_datas AS (
        -- Todas as datas únicas de movimentações + data atual
        SELECT data FROM movimentacoes
        UNION
        SELECT DATE('now', 'localtime') AS data
    ),
    produtos_datas AS (
        -- Combinação de todos produtos × todas datas relevantes
        SELECT p.id, p.nome, d.data
        FROM produtos p
        CROSS JOIN (SELECT DISTINCT data FROM todas_datas) d
    ),
    movimentacoes_acumuladas AS (
        SELECT 
            pd.nome,
            pd.data,
            COALESCE(
                SUM(m.quantidade) OVER (
                    PARTITION BY pd.id 
                    ORDER BY pd.data 
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ),
                0
            ) AS estoque
        FROM produtos_datas pd
        LEFT JOIN movimentacoes m 
            ON m.produto_id = pd.id 
            AND m.data = pd.data
    )
    SELECT 
        nome,
        data,
        estoque
    FROM movimentacoes_acumuladas
    ORDER BY nome, data
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df
