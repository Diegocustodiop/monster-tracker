import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="Monster Tracker", page_icon="🔋")

# Estilo Dark
st.markdown("""
    <style>
    .main { background-color: #000; color: #30ff00; }
    .stButton>button { background-color: #30ff00; color: black; font-weight: bold; width: 100%; border-radius: 10px; }
    .price-card { background-color: #111; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔋 Monster Tracker")
st.write("Ranking de preços atualizado")

def buscar_ml():
    produtos = []
    # URL de busca direta por packs de Monster
    url = "https://lista.mercadolivre.com.br/monster-energy-pack#D[A:monster%20energy%20pack]"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        itens = soup.find_all('div', class_='ui-search-result__content-wrapper', limit=10)
        
        for item in itens:
            nome = item.find('h2').text
            preco_raw = item.find('span', class_='andes-money-amount__fraction').text
            link = item.find('a')['href']
            produtos.append({
                "nome": nome,
                "preco": float(preco_raw.replace('.', '').replace(',', '.')),
                "link": link
            })
    except Exception as e:
        st.error(f"Erro na busca: {e}")
    
    return sorted(produtos, key=lambda x: x['preco'])

if st.button('🚀 ATUALIZAR RANKING AGORA'):
    with st.spinner('Rastreando ofertas...'):
        time.sleep(1) # Pequena pausa visual
        dados = buscar_ml()
        
        if dados:
            for i, item in enumerate(dados):
                st.markdown(f"""
                <div class="price-card">
                    <h3 style='color:#30ff00;'>{i+1}º Lugar - R$ {item['preco']}</h3>
                    <p style='color:white;'>{item['nome']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"Abrir Oferta {i+1}", item['link'])
        else:
            st.warning("Nenhuma oferta encontrada no momento. Tente novamente.")

