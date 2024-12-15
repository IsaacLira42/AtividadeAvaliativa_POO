import streamlit as st
import pandas as pd
from view import View
import time

from models.categoria import Categoria
from models.categorias import Categorias

class ManterProdutoUI:
    def main():
        st.header("Cadastro de Produtos")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterProdutoUI.listar()
        with tab2: ManterProdutoUI.inserir()
        with tab3: ManterProdutoUI.atualizar()
        with tab4: ManterProdutoUI.excluir()

    def listar():
        produto = View.produto_listar()
        if len(produto) == 0: 
            st.write("Nenhum produto cadastrado")
        else:    
            dic = []
            for obj in produto: dic.append(obj.__dict__)
            df = pd.DataFrame(dic)
            st.dataframe(df)

    def inserir():
        nome = st.text_input("Informe o nome do produto")
        preco = st.number_input("Preço")
        estoque = st.number_input("Estoque")

        categorias = Categorias.listar()
        if len(categorias) > 0:
            # Selecionar a categoria e obter o ID correspondente
            categoria_selecionada = st.selectbox("Selecione a categoria", [categoria.descricao for categoria in categorias])
            idCategoria = next(categoria.id for categoria in categorias if categoria.descricao == categoria_selecionada)

        # Botão para inserir o produto
        if st.button("Inserir"):
            if idCategoria is None:
                st.error("Selecione uma categoria")
            else:
                View.produto_inserir(0, nome, preco, estoque, idCategoria)
                st.success("Produto inserido com sucesso")
                time.sleep(2)
                st.rerun()

    def atualizar():
        produtos = View.produto_listar()
        if not produtos:
            st.write("Nenhum produto cadastrado")
        else:
            produto_selecionado = st.selectbox("Selecione o produto para atualizar", [produto.descricao for produto in produtos])
            produto = next(produto for produto in produtos if produto.descricao == produto_selecionado)

            descricao = st.text_input("Informe o novo nome do produto", produto.descricao)
            preco = st.number_input("Atualizar Preço")
            estoque = st.number_input("Atualizar Estoque")

            categorias = Categorias.listar()
            if categorias:
                categoria_selecionada = st.selectbox("Selecione a categoria", [categoria.descricao for categoria in categorias])
                idCategoria = next(categoria.id for categoria in categorias if categoria.descricao == categoria_selecionada)
            else:
                st.warning("Sem categorias")
                idCategoria = None

            if st.button("Atualizar"):
                if not idCategoria:
                    st.error("Selecione uma categoria.")
                else:
                    View.produto_atualizar(produto.id, descricao, preco, estoque, idCategoria)
                    st.success("Produto atualizado com sucesso")
                    time.sleep(2)
                    st.rerun()

    def excluir():
        produtos = View.produto_listar()
        if not produtos:
            st.write("Nenhum produto cadastrado")
        else:
            produto_selecionado = st.selectbox("Selecione o produto para excluir", [produto.descricao for produto in produtos])
            idProduto = next(produto.id for produto in produtos if produto.descricao == produto_selecionado)

            if st.button("Excluir"):
                View.produto_excluir(idProduto)
                st.success("Produto excluído com sucesso!")
                time.sleep(2)
                st.rerun()