import streamlit as st

from models.cliente import Cliente
from models.clientes import Clientes
from models.categoria import Categoria
from models.categorias import Categorias
from models.produto import Produto
from models.produtos import Produtos
from models.venda import Venda
from models.vendas import Vendas
from models.vendaitem import VendaItem
from models.vendaitens import VendaItens
from view import View

class IndexUI:
    