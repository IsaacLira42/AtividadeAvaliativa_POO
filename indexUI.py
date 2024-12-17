from datetime import datetime
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
from templates.abrircontaUI import AbrirContaUI
from templates.loginUi import LoginUI
from templates.admin.manterclienteUI import ManterClienteUI
from templates.admin.manterprodutosUI import ManterProdutoUI
from templates.admin.mantercategoriaUI import ManterCategoriaUI
from templates.admin.visualizarpedidosUI import VizualizarPedidosUI
from templates.admin.reajustarprecosUI import ReajustarPrecosUI
from templates.client.clienteUI import ClienteUI

from view import View

class IndexUI:
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema", "Abrir Conta"])
        if op == "Entrar no Sistema": LoginUI.main()
        if op == "Abrir Conta": AbrirContaUI.main()
               
    def menu_admin():            
        op = st.sidebar.selectbox("Menu", ["Cadastro de Clientes", "Cadastro de Produtos", "Cadastro de Categorias", "Visualizar Pedidos", "Reajustar Preços"])
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Produtos": ManterProdutoUI.main()
        if op == "Cadastro de Categorias": ManterCategoriaUI.main()
        if op == "Visualizar Pedidos" : VizualizarPedidosUI.main()
        if op == "Reajustar Preços" : ReajustarPrecosUI.main()
        
    def menu_cliente():
        # filtra as vendas do cliente
        cliente_id = st.session_state.get("cliente_id")
        vendas_cliente = View.vendas_cliente(cliente_id)

        if len(vendas_cliente) == 0 or vendas_cliente[-1].carrinho == False:
            if cliente_id:
                View.venda_inserir(datetime.now(), True, 0, cliente_id)
        
        ClienteUI.main()

    def sair_do_sistema():
        if st.sidebar.button("Sair"):
            del st.session_state["cliente_id"]
            del st.session_state["cliente_nome"]
            st.rerun()
    
    def sidebar():
        if "cliente_id" not in st.session_state:
            # usuário não está logado
            IndexUI.menu_visitante()   
        else:
            # usuário está logado, verifica se é o admin
            admin = st.session_state["cliente_nome"] == "admin"
            # mensagen de bem-vindo
            st.sidebar.write("Bem-vindo(a), " + st.session_state["cliente_nome"])
            # menu do usuário
            if admin: IndexUI.menu_admin()
            else: IndexUI.menu_cliente()
            # controle de sair do sistema
            IndexUI.sair_do_sistema()
    
    def main():
        # verifica a existe o usuário admin
        View.cliente_admin()
        # monta o sidebar
        IndexUI.sidebar()
       
IndexUI.main()