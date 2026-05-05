import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Monster Tracker Pro", page_icon="🔋")

st.markdown("""
    <style>
    .stApp {background-color: #000; color: #30ff00;}
    .stButton>button {background-color: #30ff00; color: black; font-weight: bold; width: 100%; border-radius: 10px;}
    .offer-card {background-color: #111; padding: 15px; border-radius: 10px; border: 1px solid #30ff00; margin-bottom: 10px;}
    .store-tag {font-size: 12px; color: #888; text-transform: uppercase;}
    </style>
    """, unsafe_allow_html=True)

st.title("🔋 Monster Tracker Multi-Market")
st.write("Buscando o melhor preço em tempo real...")

def buscar_ofertas(loja):
    resultados = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9"
    }
    
    try:
        if loja == "Mercado Livre":
            url = "https://lista.mercadolivre.com.br/monster-energy-pack"
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            itens = soup.select(".ui-search-result__content-wrapper", limit=5)
            for item in itens:
                nome = item.find('h2').text
                preco = item.find('span', class_='andes-money-amount__fraction').text
                link = item.find('a')['href']
                resultados.append({"loja": "Mercado Livre", "nome": nome, "preco": float(preco.replace('.','')), "link": link})
        
        elif loja == "Amazon":
            url = "https://www.amazon.com.br/s?k=monster+energy+pack"
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            itens = soup.select(".s-result-item[data-component-type='s-search-result']", limit=5)
            for item in itens:
                try:
                    nome = item.h2.text.strip()
                    preco_int = item.select_one(".a-price-whole").text.replace('.','').replace(',','')
                    link = "https://www.amazon.com.br" + item.select_one("h2 a")['href']
                    resultados.append({"loja": "Amazon", "nome": nome, "preco": float(preco_int), "link": link})
                except: continue
    except:
        pass
    return resultados

if st.button('🔥 COMPARAR TODOS OS MARKETPLACES'):
    with st.spinner('Rastreando Amazon e Mercado Livre...'):
        todas_ofertas = []
        todas_ofertas.extend(buscar_ofertas("Amazon"))
        todas_ofertas.extend(buscar_ofertas("Mercado Livre"))
        
        if todas_ofertas:
            # Ordena pelo mais barato
            df = pd.DataFrame(todas_ofertas).sort_values(by="preco")
            
            for index, row in df.iterrows():
                st.markdown(f"""
                <div class="offer-card">
                    <span class="store-tag">{row['loja']}</span>
                    <h2 style="margin: 5px 0;">R$ {row['preco']:.2f}</h2>
                    <p style="color: white; font-size: 14px;">{row['nome']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"IR PARA {row['loja'].upper()}", row['link'])
        else:
            st.error("Os sites estão bloqueando o acesso agora. Tente clicar novamente ou aguarde 30 segundos.")

st.info("Dica: Se não carregar de primeira, clique novamente. Esses sites bloqueiam acessos repetidos muito rápidos.")
