import streamlit as st
from app.screen import df
from controller.utils import convert_csv, mensagem_sucesso

st.title('Dataset de Vendas')

# Verifique se df está carregado corretamente
if df is not None:
    with st.expander('Colunas'):
        colunas = st.multiselect(
            'Selecione as Colunas',
            list(df.columns),
            list(df.columns)
        )
    st.sidebar.title('Filtros')
    with st.sidebar.expander('categoria'):
        categorias = st.multiselect(
            'Selecione as categorias',
            df['categoria'].unique(), 
            df['categoria'].unique()
            
        
        )
               
    with st.sidebar.expander('marca'):
        marcas = st.multiselect(
            'Selecione as marcas',
            df['marca'].unique(), 
            df['marca'].unique()
        )
        
    with st.sidebar.expander('situacao'):
        situacoes = st.multiselect(
            'Selecione as situações',
            df['situacao'].unique(), 
            df['situacao'].unique()
        )
    with st.sidebar.expander('forma_de_pagamento'):
        forma_pagamentos = st.multiselect(
            'Selecione as Formas de Pagamentos',
            df['forma_de_pagamento'].unique(), 
            df['forma_de_pagamento'].unique()
        )

        
    with st.sidebar.expander('data_pedido'):
        data_pedido = st.date_input(
            'Selecione a data',
            (df['data_pedido'].min(),
            df['data_pedido'].max())         
        )
 
    query = '''
        `categoria` in @categorias and \
        `marca` in @marcas and \
        `forma_de_pagamento` in @forma_pagamentos and \
        `situacao` in @situacoes and \
         @data_pedido[0] <= `data_pedido` <= @data_pedido[1]
    
    '''
    filtro_dados = df.query(query)
    filtro_dados = filtro_dados[colunas]
                
    st.dataframe(filtro_dados)
    st.markdown(f'A tabela possui :blue[{filtro_dados.shape[0]}] linhas e :blue[{filtro_dados.shape[1]}] colunas')
    st.markdown('Escreva um nome do arquivo')
    
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        nome_arquivo = st.text_input(
            '',
            label_visibility='collapsed'
        )
    nome_arquivo += '.csv'
    with coluna2:
        st.download_button(
            'Baixar arquivo',
            data=convert_csv(filtro_dados),
            file_name=nome_arquivo,
            mime='text/csv',
            on_click= mensagem_sucesso
        )
        
else:
    st.error("Erro: O DataFrame 'df' não foi carregado corretamente.")
    
