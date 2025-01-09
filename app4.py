import streamlit as st
import openai
import PyPDF2


# Configurar la clave de API de OpenAI
#openai.api_key ="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" # Configurar la página de Streamlit

st.set_page_config(page_title="Asistente", layout="centered")
st.title("📄🤖 Asistente Formación docente")
#st.markdown("Sube un archivo PDF y haz preguntas relacionadas con su contenido.")
#openai.api_key = st.text_input("Ingresa la clave:", key="input_usuario",type="password")
openai.api_key = st.text_input("Ingresa la clave:", type="password")
print("Respuesta de api:\n", openai.api_key)


# Función para extraer texto del PDF
def extraer_texto_pdf(archivo_pdf):
    texto = ""
    lector = PyPDF2.PdfReader(archivo_pdf)
    for pagina in lector.pages:
        texto += pagina.extract_text()
    return texto

# Subir y procesar el archivo PDF
#contenido_pdf = ""
#archivo_subido = st.file_uploader("Sube un archivo PDF", type=["pdf"])
#if archivo_subido:
    #with st.spinner("Extrayendo texto del PDF..."):
contenido_pdf = extraer_texto_pdf("DDAW_ES_Guía didáctica_Docentes Digitales_ ABP web.docx.pdf")
#st.success("Texto extraído con éxito.")
#st.text_area("Contenido del PDF", contenido_pdf, height=200)

# Inicializar el historial de la conversación
if "historial" not in st.session_state:
    st.session_state.historial = [
        {"role": "system", "content": "Eres un asistente que responde preguntas basadas en el contenido proporcionado."}
    ]

# Función para obtener respuesta de ChatGPT

def obtener_respuesta(mensaje_usuario, contexto):
    st.session_state.historial.append({"role": "user", "content": mensaje_usuario})
    st.session_state.historial.append({"role": "system", "content": f"Contexto: {contexto}"})
    
    respuesta = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Modelo para ChatGPT Plus
        messages=st.session_state.historial,
        temperature=0.5,
        max_tokens=300
    )
    mensaje_chatbot = respuesta['choices'][0]['message']['content']
    st.session_state.historial.append({"role": "assistant", "content": mensaje_chatbot})
    return mensaje_chatbot

# Entrada del usuario
if contenido_pdf and openai.api_key:
    pregunta_usuario = st.text_input("Haz una pregunta sobre el contenido de tu formación:", key="input_usuario")

    # Mostrar respuesta basada en el PDF
    if pregunta_usuario:
        with st.spinner("Escribiendo..."):
            respuesta_chatbot = obtener_respuesta(pregunta_usuario, contenido_pdf)
        st.markdown(f"**Tú:** {pregunta_usuario}")
        st.markdown(f"**Asistente:** {respuesta_chatbot}")
