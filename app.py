import streamlit as st
import requests

st.set_page_config(page_title="Monster Tracker - Supermercados", page_icon="🛒")

# Recomendo usar a SerpApi para evitar bloqueios (Pegue sua chave em serpapi.com)
API_KEY = "SUA_CHAVE_AQUI"

st.markdown("""
    <style>
    .stApp {background-color: #000; color: #30ff00;}
    .market-card {
        background-color: #111; 
        padding: 15px; 
        border-radius: 12px; 
        border-left: 5px solid #30ff00; 
        margin-bottom: 15px;
    }
    .price-text { font-size: 24px; font-weight: bold; color: #30ff00; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛒 Monster no Supermercado")
st.write("Buscando ofertas em redes de varejo e mercados.")

if st.button('🔎 BUSCAR EM SUPERMERCADOS'):
    if API_KEY == "SUA_CHAVE_AQUI":
        st.warning("Insira sua chave API no código para buscar.")
    else:
        with st.spinner('Consultando redes de supermercados...'):
            # A busca agora foca em 'supermercado' e 'delivery'
            query = "monster energy pack supermercado"
            url = f"https://serpapi.com/search.json?engine=google_shopping&q={query}&google_domain=google.com.br&gl=br&hl=pt&api_key={API_KEY}"
            
            try:
                response = requests.get(url)
                dados = response.json()
                
                if "shopping_results" in dados:
                    # Filtramos para evitar Amazon/Mercado Livre e focar em mercados
                    excluir = ["amazon", "mercado livre", "shopee"]
                    resultados = [item for item in dados["shopping_results"] 
                                 if not any(x in item.get('source', '').lower() for x in excluir)]
                    
                    if resultados:
                        for item in resultados[:10]:
                            with st.container():
                                st.markdown(f"""
                                <div class="market-card">
                                    <p style="color:#888; margin:0;">{item.get('source')}</p>
                                    <h2 class="price-text">{item.get('price')}</h2>
                                    <p style="color:white; font-size:14px;">{item.get('title')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                st.link_button(f"IR PARA {item.get('source').upper()}", item.get('link'))
                    else:
                        st.info("Nenhuma oferta de supermercado encontrada agora. Tente em alguns minutos.")
                else:
                    st.error("Erro ao processar dados da busca.")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

st.caption("Foco: Carrefour, Pão de Açúcar, Extra, Mambo, Sonda, etc.")
