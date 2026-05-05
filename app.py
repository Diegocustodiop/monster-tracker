import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Monster Tracker", page_icon="🔋")

st.markdown("<style>.stApp {background-color: #000; color: #30ff00;}</style>", unsafe_allow_html=True)
st.title("🔋 Monster Tracker")

if st.button('🚀 BUSCAR PREÇOS'):
    with st.spinner('Driblando a segurança e buscando...'):
        # URL de busca geral
        url = "https://www.mercadolivre.com.br/monster-energy/monster_NoIndex_True"
        
        # Este é o "disfarce" (User-Agent)
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "Accept-Language": "pt-BR,pt;q=0.9"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Mudamos o jeito de procurar os itens para um mais simples
            itens = soup.find_all('div', class_='ui-search-result__content-wrapper', limit=5)
            
            if not itens:
                # Se não achar do jeito novo, tenta um jeito reserva
                itens = soup.select(".ui-search-layout__item", limit=5)

            if itens:
                for item in itens:
                    try:
                        nome = item.find('h2').text
                        preco = item.find('span', class_='andes-money-amount__fraction').text
                        link = item.find('a')['href']
                        
                        with st.container():
                            st.write(f"### R$ {preco}")
                            st.write(f"{nome}")
                            st.link_button("VER OFERTA", link)
                            st.divider()
                    except:
                        continue
            else:
                st.error("O Mercado Livre bloqueou o acesso temporariamente. Tente clicar de novo em 1 minuto.")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")


