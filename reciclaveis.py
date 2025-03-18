from together import Together
import streamlit as st
import requests
from PIL import Image
from io import BytesIO


with st.sidebar:
    st.sidebar.header("Reciclaveis")
    st.sidebar.write("""
    Insira os itens para construção de um produto com materiais reciclaveis
                     
    - Caso tenha alguma idéia para publicarmos, envie uma mensagem para: 11-990000425 (Willian)
    - Contribua com qualquer valor para mantermos a pagina no ar. PIX (wpyagami@gmail.com)
    """)


def generate_image(prompt, api_key):
    """Gera uma imagem baseada no prompt utilizando a API do Together"""
    try:
        client = Together(api_key=api_key)
        
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            steps=4,
            width=1024,
            height=768,
            n=1
        )
        
        # Obtém a URL da imagem gerada
        imurl = response.data[0].url
        
        # Faz o download da imagem gerada
        my_res = requests.get(imurl)
        my_img = Image.open(BytesIO(my_res.content))
        return my_img

    except Exception as e:
        raise RuntimeError(f"Erro ao gerar imagem: {e}")

st.title("Gerador de Imagens de Materiais Recicláveis")
st.write("Informe uma lista de materiais recicláveis para gerar uma imagem.")

api_key = st.secrets["together"]

# Entrada dos materiais recicláveis
items = st.text_area("Digite os itens separados por vírgula", value="garrafa, papel, vidro")

if st.button("Gerar Imagem"):
    if not api_key:
        st.error("Por favor, insira sua API Key.")
    else:
        items_list = [item.strip() for item in items.split(",") if item.strip()]
        prompt = f"Crie um objeto utilizando os seguintes materiais recicláveis: {', '.join(items_list)}"
        
        try:
            image = generate_image(prompt, api_key)
            st.image(image, caption="Imagem Gerada", use_column_width=True)
        except Exception as e:
            st.error(str(e))

