import streamlit as st 
import plotly.express as px 
from screen import df
from controller.utils import format_number
from app.graficos import grafico_coluna_forma_pagamento, grafico_rec_mensal, grafico_rec_produto, grafico_rec_categoria

#st.title("Dashboard de vendas :shopping_trolley:")

aba1, aba2, aba3 = st.tabs(['Screen', 'Receita', 'Produtos'])
with aba1:
    # Exibir DataFrame no Streamlit
    if df is not None:
        st.write(df)
        
with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita total', format_number(df['totalvenda'].sum(), 'R$'))
        st.plotly_chart(grafico_coluna_forma_pagamento, use_container_width=True)
        st.plotly_chart(grafico_rec_produto, use_container_width=True)
    with coluna2:
        st.metric('Quantidade de Vendas', format_number(df.shape[0]))
        st.plotly_chart(grafico_rec_mensal, use_container_width=True)
        st.plotly_chart(grafico_rec_categoria, use_container_width=True)
    

