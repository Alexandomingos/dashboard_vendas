
from sqlalchemy import   Column, String, Float, Date, Boolean, BigInteger, ForeignKey, DECIMAL
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from core.database import engine 

Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produto'
    id = Column(BigInteger, primary_key=True)
    id_produto_pai = Column(BigInteger, ForeignKey('produto.id'))
    nome = Column(String(180))
    codigo = Column(String(30))
    preco = Column(DECIMAL(8,2))
    tipo = Column(String(15))
    situacao = Column(String(5))
    formato = Column(String(18))
    descricao_curta = Column(String(5000))
    imagem_url = Column(String)
    data_validade = Column(Date)
    unidade = Column(String(15))
    peso_liquido = Column(Float)
    peso_bruto = Column(Float)
    volumes = Column(BigInteger)
    itens_por_caixa = Column(BigInteger)
    gtin = Column(String)
    gtin_embalagem = Column(String(18))
    tipo_producao = Column(String(18))
    condicao = Column(BigInteger)
    frete_gratis = Column(Boolean)
    marca = Column(String(50))
    observacoes = Column(String(900))
    categoria_id = Column(BigInteger, ForeignKey('categoria.id'))
    categoria = relationship('Categoria', back_populates='produtos')
    estoque_id = Column(BigInteger, ForeignKey('estoque.id'))
    estoque = relationship("Estoque", foreign_keys="[Estoque.produto_id]", back_populates="produto")


class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(BigInteger, primary_key=True)
    descricao = Column(String)
    produtos = relationship('Produto', back_populates='categoria')
    #variacoes = relationship('Variacao', back_populates='categoria')
    
class Deposito(Base):
        __tablename__ = 'depositos'

        id = Column(BigInteger, primary_key=True)
        produto_id = Column(BigInteger, ForeignKey('produto.id'))
        saldoFisicoTotal = Column(BigInteger)
        saldoVirtualTotal = Column(BigInteger)
    
        produto = relationship("Produto", back_populates="depositos")
        depositos_itens = relationship("DepositoItem", back_populates="deposito")   


class GrupoProduto(Base):
    __tablename__ = 'grupo_produto'
    id = Column(BigInteger, primary_key=True)

class Estoque(Base):
    __tablename__ = 'estoque'

    id = Column(BigInteger, primary_key=True)
    produto_id = Column(BigInteger, ForeignKey('produto.id'))
    saldo_fisico_total = Column(BigInteger)
    saldo_virtual_total = Column(BigInteger)
    deposito_id = Column(BigInteger)
    saldo_fisico_deposito = Column(BigInteger)
    saldo_virtual_deposito = Column(BigInteger)

    # Adicione um relacionamento com a tabela de Produto se necessário
    produto = relationship("Produto", foreign_keys="[Estoque.produto_id]", back_populates="estoque")



class DepositoItem(Base):
    __tablename__ = 'deposito_itens'

    id = Column(BigInteger, primary_key=True)
    deposito_id = Column(BigInteger, ForeignKey('depositos.id'))
    saldoFisico = Column(BigInteger)
    saldoVirtual = Column(BigInteger)

    deposito = relationship("Deposito", back_populates="depositos_itens")

class Fornecedor(Base):
    __tablename__ = 'fornecedores'

    id = Column(BigInteger, primary_key=True)
    descricao = Column(String(255))
    codigo = Column(String(50))
    precoCusto = Column(DECIMAL(8,2))
    precoCompra = Column(DECIMAL(8,2))
    padrao = Column(Boolean)
    produto_id = Column(BigInteger, ForeignKey('produto.id'))

    produto = relationship("Produto")

Produto.depositos = relationship("Deposito", order_by=Deposito.id, back_populates="produto")

# Cria as tabelas
Base.metadata.create_all(engine)


