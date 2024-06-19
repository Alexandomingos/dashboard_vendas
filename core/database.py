from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine


'''
Função para configurar a conexão ao banco de dados.
    
''' 
# Definindo a URL do banco de dados PostgreSQL
DATABASE_URL = "postgresql://postgres:Laura1107@localhost:5432/blingapiv3"

# Criando uma sessão
print("Creating session...")
# Criando o engine
print("Creating engine...")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()