import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from model.db_functions import add_product, get_products, add_stock, get_stock_history
from datetime import datetime, timedelta

st.title("Dashboard de Estoque")
tab1, tab2 = st.tabs(["Cadastrar Produto", "Gráfico de Estoque"])

with tab1:
    st.subheader("Cadastrar Produto")
    with st.form(key="form_produto"):
        nome = st.text_input("Nome do produto")
        quantidade = st.number_input("Quantidade inicial", min_value=0, step=1)
        preco = st.number_input("Preço", min_value=0.0, step=0.01)
        submit = st.form_submit_button("Adicionar")
        if submit:
            add_product(nome, quantidade, preco)
            st.success(f"Produto '{nome}' adicionado!")
    st.subheader("Atualizar Estoque")
    products = get_products()
    if not products.empty:
        prod_dict = dict(zip(products["id"], products["nome"]))
        prod_id = st.selectbox("Produto", list(prod_dict.keys()), format_func=lambda x: prod_dict[x])
        qtd = st.number_input("Quantidade a adicionar ou retirar", step=1)
        if st.button("Atualizar Estoque"):
            add_stock(prod_id, qtd)
            st.success(f"Estoque atualizado para {prod_dict[prod_id]}")

with tab2:
    st.subheader("Histórico de Estoque - Resumo")
    df = get_stock_history()
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], format='mixed', errors='coerce')
        df["data_date"] = df["data"].dt.date
      
        periodo = st.radio(
            "Período a visualizar:",
            options=["Dia específico", "Últimos 30 dias", "Últimos 3 meses", "Últimos 6 meses", "Personalizado"],
            horizontal=True,
            index=0
        )
        datas_disponiveis = sorted(df["data_date"].dropna().unique())
        data_max = datas_disponiveis[-1] if datas_disponiveis else datetime.today().date()
       
        if periodo == "Dia específico":
            data_inicio = st.date_input("Selecione a data:", value=data_max)
            data_fim = data_inicio
        elif periodo == "Últimos 30 dias":
            data_inicio = data_max - timedelta(days=29)
            data_fim = data_max
        elif periodo == "Últimos 3 meses":
            data_inicio = data_max - timedelta(days=89)
            data_fim = data_max
        elif periodo == "Últimos 6 meses":
            data_inicio = data_max - timedelta(days=179)
            data_fim = data_max
        else:
            col1, col2 = st.columns(2)
            with col1:
                data_inicio = st.date_input("Data inicial:", value=data_max - timedelta(days=30))
            with col2:
                data_fim = st.date_input("Data final:", value=data_max)
       
        mask = (df["data_date"] >= data_inicio) & (df["data_date"] <= data_fim)
        df_periodo = df[mask].copy()
       
        if df_periodo.empty:
            st.warning(f"Sem registros no período selecionado.")
        else:
            ultimo_dia = df_periodo["data_date"].max()
            df_resumo = df_periodo[df_periodo["data_date"] == ultimo_dia].groupby("nome")["estoque"].last().reset_index()
            df_resumo = df_resumo.sort_values("estoque", ascending=False)
           
            st.write(f"**Estoque final em {ultimo_dia.strftime('%d/%m/%Y')}** (último dia do período: {data_inicio} → {data_fim})")
          
            st.dataframe(
                df_resumo.style.format({"estoque": "{:,.0f}"}),
                use_container_width=True,
                hide_index=True
            )
           
            st.write("**Estoque final por produto**")
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(df_resumo["nome"], df_resumo["estoque"], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])
          
            ax.set_ylabel("Quantidade em Estoque (final do período)")
            ax.set_title(f"Estoque Final - {ultimo_dia.strftime('%d/%m/%Y')}")
            ax.grid(True, axis='y', linestyle='--', alpha=0.6)
          
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}',
                        ha='center', va='bottom', fontsize=9)
          
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
    else:
        st.info("Nenhum dado registrado ainda.")
