import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Monster Tracker | Amazon", page_icon="🔋")

# Estilo visual
st.markdown("""
    <style>
    .stApp {background-color: #000; color: #30ff00;}
    .stButton>button {background-color: #30ff00; color: black; font-weight: bold; border-radius: 20px;}
    .card {background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🔋 Monster Tracker (Amazon)")
st.write("Buscando ofertas de Monster direto na Amazon Brasil")

def buscar_amazon():
    produtos = []
    # URL de busca da Amazon para Monster Energy
    url = "https://www.amazon.com.br/s?k=monster+energy+pack"
    
    # Headers para parecer um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Seleciona os blocos de produtos da Amazon
        itens = soup.select(".s-result-item[data-component-type='s-search-result']", limit=8)
        
        for item in itens:
            nome = item.h2.text.strip()
            # Busca o preço (parte inteira e decimal)
            preco_inteiro = item.select_one(".a-price-whole")
            preco_decimal = item.select_one(".a-price-fraction")
            link_tag = item.select_one("h2 a")
            
            if preco_inteiro and link_tag:
                preco_final = preco_inteiro.text.replace(",", "").replace(".", "")
                centavos = preco_decimal.text if preco_decimal else "00"
                link = "https://www.amazon.com.br" + link_tag['href']
                
                produtos.append({
                    "nome": nome,
                    "preco": f"{preco_final},{centavos}",
                    "link": link
                })
    except Exception as e:
        st.error(f"Erro ao conectar com a Amazon: {e}")
        
    return produtos

if st.button('🔍 PESQUISAR NA AMAZON'):
    with st.spinner('Consultando prateleiras da Amazon...'):
        resultados = buscar_amazon()
        
        if resultados:
            for i, prod in enumerate(resultados):
                st.markdown(f"""
                <div class="card">
                    <h2 style='color:#30ff00;'>R$ {prod['preco']}</h2>
                    <p style='color:white; font-size:14px;'>{prod['nome']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"VER NA AMAZON", prod['link'])
                st.write("")
        else:
            st.warning("A Amazon bloqueou a consulta automática ou não encontrou itens. Tente clicar novamente.")

st.caption("Nota: Os preços podem variar de acordo com o frete e promoções relâmpago.")
