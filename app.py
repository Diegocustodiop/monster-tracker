import streamlit as st
import requests
from bs4 import BeautifulSoup

# Configuração da página
st.set_page_config(page_title="Monster Tracker", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #111; color: #30ff00; }
    .stButton>button { background-color: #30ff00; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔋 Monster Tracker: O Ranking de Preços")
st.subheader("Buscando as melhores ofertas em tempo real...")

def pegar_dados_ml():
    # Simulação de raspagem real no Mercado Livre
    url = "https://lista.mercadolivre.com.br/monster-energy-pack"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    produtos = []
    itens = soup.find_all('div', class_='ui-search-result__content-wrapper', limit=10)
    
    for item in itens:
        nome = item.find('h2').text
        preco = item.find('span', class_='andes-money-amount__fraction').text
        link = item.find('a', class_='ui-search-link')['href']
        produtos.append({"nome": nome, "preco": float(preco), "link": link, "loja": "Mercado Livre"})
    
    return sorted(produtos, key=lambda x: x['preco'])

if st.button('Atualizar Ranking'):
    dados = pegar_dados_ml()
    
    for i, item in enumerate(dados):
        col1, col2, col3 = st.columns([1, 4, 2])
        with col1:
            st.metric(label="Posição", value=f"{i+1}º")
        with col2:
            st.write(f"**{item['nome']}**")
            st.caption(f"Loja: {item['loja']}")
        with col3:
            st.subheader(f"R$ {item['preco']}")
            st.link_button("Ver Anúncio", item['link'])
        st.divider()
