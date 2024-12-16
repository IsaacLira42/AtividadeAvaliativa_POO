import streamlit as st
import pandas as pd
from view import View
import time

from models.categoria import Categoria
from models.categorias import Categorias

class ManterCategoriaUI:
    def main():
        st.header("Cadastro de Categorias")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterCategoriaUI.listar()
        with tab2: ManterCategoriaUI.inserir()
        with tab3: ManterCategoriaUI.atualizar()
        with tab4: ManterCategoriaUI.excluir()

    def listar():
        categoria = View.categoria_listar()
        if len(categoria) == 0: 
            st.write("Nenhuma categoria cadastrada")
        else:    
            dic = []
            for obj in categoria: dic.append(obj.__dict__)
            df = pd.DataFrame(dic)
            st.dataframe(df)

    def inserir():
        nome = st.text_input("Informe a categoria")

        lista_de_categorias = View.categoria_listar()

        erro = False

        for categoria in lista_de_categorias:
            if categoria.descricao == nome:
                erro = True
                break
    
        # Botão para inserir o produto
        if st.button("Inserir"):
            if not nome.strip():
                st.error("Selecione uma categoria")
            elif erro:
                st.error("Categoria existente")
            else:
                View.categoria_inserir(nome)
                st.success("Categoria inserida com sucesso")
                time.sleep(2)
                st.rerun()
    
    def atualizar():
        categorias = View.categoria_listar()
        if not categorias:
            st.write("Nenhuma categoria cadastrada")
        else:
            categoria_selecionada = st.selectbox("Selecione a categoria para atualizar", [categoria.descricao for categoria in categorias])
            categoria = next(categoria for categoria in categorias if categoria.descricao == categoria_selecionada)

            descricao = st.text_input("Informe o novo nome da categoria", categoria.descricao)


            if st.button("Atualizar"):
                if not categoria_selecionada:
                    st.error("Selecione uma categoria.")
                else:
                    View.categoria_atualizar(categoria.id, descricao)
                    st.success("Categoria atualizada com sucesso")
                    time.sleep(2)
                    st.rerun()


    def excluir():
        categorias = View.categoria_listar()

        if len(categorias) == 0:
            st.write("Nenhuma categoria cadastrada")
        else:
            categoria_selecionada = st.selectbox("Selecione a categoria para excluir", [categoria.descricao for categoria in categorias])
            
            categoria = next((categoria for categoria in categorias if categoria.descricao == categoria_selecionada), None)

            # Botão para excluir a categoria
            if st.button("Excluir"):
                if not categoria:
                    st.error("A categoria não foi encontrada.")
                else:
                    st.success("Categoria excluída com sucesso!")
                    View.categoria_excluir(categoria.id)
                    time.sleep(2)
                    st.rerun()
