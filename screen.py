import streamlit as st
import pandas as pd
from sqlalchemy import text
from core.database import engine 


# Função para executar a consulta SQL e retornar um DataFrame
def fetch_data_from_sql_query(sql_query):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            data = result.fetchall()
            columns = result.keys()
            df = pd.DataFrame(data, columns=columns)
            return df
    except Exception as e:
        st.error(f"Erro ao executar consulta SQL: {e}")
        return None

# Consulta SQL
sql_query = """
    -- Subconsulta para cada depósito
WITH deposito_saldos AS (
    SELECT
        i.codigo as sku,
        i.descricao as produto,
        c.descricao as Categoria,
        pd.marca as Marca,
        pd.situacao as "Esta Ativo ou Inativo?",
        pd.preco as "Preço 1",
        p.data as data_pedido,
        p.numero as pedido,
        f."precoCusto" as "Preço de Custo",
        f.codigo as "Última compra",
        f.padrao as padrao,
        p."notaFiscal_id" as idNotaFiscal,
        CASE 
            WHEN pc."formaPagamento_id" ='3311712' OR pc."formaPagamento_id" = '4212038' THEN 'CRÉDITO 1X'
            WHEN pc."formaPagamento_id" ='3311727' OR pc."formaPagamento_id" = '4212029' THEN 'PIX'
            WHEN pc."formaPagamento_id" ='3311721' OR pc."formaPagamento_id" = '4212163' THEN 'DÉBITO'
            WHEN pc."formaPagamento_id" ='3744106' OR pc."formaPagamento_id" ='3477100' OR pc."formaPagamento_id" ='3477104' OR pc."formaPagamento_id" ='3477105' OR pc."formaPagamento_id" ='3477106' OR pc."formaPagamento_id" = '4212045' OR pc."formaPagamento_id"= '4212054' OR pc."formaPagamento_id" = '4212065' OR pc."formaPagamento_id" ='4212094' THEN 'CRÉDITO PARCELADO'
            WHEN pc."formaPagamento_id" ='3082877' OR pc."formaPagamento_id" = '4188404' OR pc."formaPagamento_id" = 0 THEN 'DINHEIRO'
            WHEN pc."formaPagamento_id" ='3477127' OR pc."formaPagamento_id" = '4212182' THEN 'CHEQUE'
            WHEN pc."formaPagamento_id" ='3477114' OR pc."formaPagamento_id" = '4212247' THEN 'CONVENIO'
            WHEN pc."formaPagamento_id" ='3082878' THEN 'CONTAS A RECEBER/PAGAR'
            WHEN pc."formaPagamento_id" IS NULL THEN 'PEDIDO EM ABERTO'
            ELSE 'NEW_FORMA-PAGAMENTO'
        END as forma_de_pagamento,
        CASE
            WHEN p.situacao_id = 9 OR p.situacao_id = 24 THEN 'ATENDIDO'
            WHEN p.situacao_id = 89088 THEN 'EMISSAO NOTA'
            WHEN p.situacao_id = 12 THEN 'CANCELADO'
            WHEN p.situacao_id = 138377 THEN 'ABASTECIMENTO SALAO'
            WHEN p.situacao_id = 76791 THEN 'PAGO'
	        WHEN p.situacao_id = 6 THEN 'EM ABERTO'
			WHEN p.situacao_id = 15 THEN 'EM ANDAMENTO'   
            WHEN p.situacao_id = 329644 THEN 'CONSIGNADO'
            ELSE 'New'
        END as Situacao,
        i.valor as valor,
        i.quantidade as quantidade,
        (i.valor * i.quantidade) as totalvenda,
        e.deposito_id,
        e.saldo_virtual_deposito,
        p."intermediador_nomeUsuario",
        p."taxas_taxaComissao" as TaxaComissao,
        p."taxas_custoFrete" as TaxaFrete,
        p."taxas_valorBase" as ValorBase,
        (p."taxas_valorBase" - p."taxas_taxaComissao" - p."taxas_custoFrete") as ValorReceber
    FROM
        itens i
        LEFT JOIN pedidos p ON p.id = i.pedido_id
        LEFT JOIN parcelas pc ON pc.pedido_id = i.pedido_id
        LEFT JOIN estoque e ON e.produto_id = i.produto_id
        LEFT JOIN produto pd ON pd.id = e.produto_id
        LEFT JOIN fornecedores f ON f.produto_id = pd.id
        LEFT JOIN categorias c ON c.id = pd.categoria_id
    WHERE
        /*p.data >= '2024-01-01'*/
        pd.situacao = 'A'
        /*AND i.codigo = '0000000028721'*/
)
-- Agregação final
SELECT
    sku,
    produto,
    Categoria,
    Marca,
    "Esta Ativo ou Inativo?",
    "Preço 1",
    data_pedido,
    pedido,
    "Preço de Custo",
    "Última compra",
    padrao,
    idNotaFiscal,
    forma_de_pagamento,
    MAX(CASE WHEN deposito_id = 14886987121 THEN saldo_virtual_deposito ELSE 0 END) as "LOJA RETIRO",
    MAX(CASE WHEN deposito_id = 14886987122 THEN saldo_virtual_deposito ELSE 0 END) as "CHARMY CENTRAL",
    MAX(CASE WHEN deposito_id = 14886855600 THEN saldo_virtual_deposito ELSE 0 END) as "GERAL",
    MAX(CASE WHEN deposito_id = 14887235779 THEN saldo_virtual_deposito ELSE 0 END) as "LOJA ROSARIO",
    MAX(CASE WHEN deposito_id = 14887235780 THEN saldo_virtual_deposito ELSE 0 END) as "CHARMY CENTRO",
    Situacao,
    valor,
    quantidade,
    totalvenda,
    "intermediador_nomeUsuario",
    TaxaComissao,
    TaxaFrete,
    ValorBase,
    ValorReceber
FROM
    deposito_saldos
GROUP BY
    sku,
    produto,
    Categoria,
    Marca,
    "Esta Ativo ou Inativo?",
    "Preço 1",
    data_pedido,
    pedido,
    "Preço de Custo",
    "Última compra",
    padrao,
    idNotaFiscal,
    forma_de_pagamento,
    Situacao,
    valor,
    quantidade,
    totalvenda,
    "intermediador_nomeUsuario",
    TaxaComissao,
    TaxaFrete,
    ValorBase,
    ValorReceber
ORDER BY
    sku DESC;


"""


st.set_page_config(layout="wide")
# Interface do Streamlit
st.title("Pedidos de Vendas :shopping_trolley:")

# Carregar dados da consulta SQL em um DataFrame
df = fetch_data_from_sql_query(sql_query)

df['data_pedido'] = pd.to_datetime(df['data_pedido'], format='%d/%m/%Y')
