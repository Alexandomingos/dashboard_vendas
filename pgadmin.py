from shutil import which
import streamlit as st 
import psycopg2
import pandas as pd 


def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()


def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
rows = run_query("SELECT * FROM pedidos")

data = pd.DataFrame(rows)
print(data)