from operator import index
import time
from core.database import session
from models.product import Produto, Categoria, Deposito
from app.screen import df
import pandas as pd
import streamlit as st 

def find_all_products():
    try:
        produtos = session.query(Produto).all()
        return produtos
    except Exception as e:
        print(f"Erro ao selecionar os dados: {e}")
        return []
    finally:
        session.close()
        
def find_all_category():
    try:
        produtos = session.query(Categoria).all()
        return produtos
    except Exception as e:
        print(f"Erro ao selecionar os dados: {e}")
        return []
    finally:
        session.close()

def find_all_stock():
    try:
        produtos = session.query(Deposito).all()
        return produtos
    except Exception as e:
        print(f"Erro ao selecionar os dados: {e}")
        return []
    finally:
        session.close()


def format_number(value, prefix=''):
    for unit in ['','mil']:
        if value < 1000:
            return f'{prefix} {value:.2f} {unit}'
        value /= 1000
    return f'{prefix} {value:.2f} milhões'

# 1- Dataframe Receita por Forma de pagamento
df_rec_forma_pagamento = df.groupby('forma_de_pagamento')[['valor']].sum()
df_rec_forma_pagamento = df.drop_duplicates(subset='forma_de_pagamento')[['forma_de_pagamento']].merge(df_rec_forma_pagamento, left_on='forma_de_pagamento', right_index=True).sort_values('valor', ascending=False)

# 2 - Dataframe Receita Mensal

df_rec_mensal = df.set_index('data_pedido').groupby(pd.Grouper(freq='ME'))['valor'].sum().reset_index()
df_rec_mensal['Ano'] = df_rec_mensal['data_pedido'].dt.year
df_rec_mensal['Mes'] = df_rec_mensal['data_pedido'].dt.month_name()



# 3- Dataframe Receita por  Produtos
df_rec_produtos = df.groupby('produto')[['valor']].sum().sort_values('valor', ascending=False)
# df_rec_produtos  = df.drop_duplicates(subset='produto')[['produto']].merge(df_rec_produtos , left_on='produto', right_index=True).sort_values('valor', ascending=False)

# 4- Dataframe Receita por  Categoria
df_rec_categoria = df.groupby('categoria')[['valor']].sum().sort_values('valor', ascending=False)


# 5- Dataframe Receita por  Marca
df_rec_marca = df.groupby('marca')[['valor']].sum()
df_rec_marca = df.drop_duplicates(subset='marca')[['marca']].merge(df_rec_marca, left_on='marca', right_index=True).sort_values('valor', ascending=False)

# Função para converter arquivo csv
@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')


def mensagem_sucesso():
    success = st.success(
        'Arquivo baixado com sucesso!',
         icon="✅"
    )
    time.sleep(3)
    success.empty()
    