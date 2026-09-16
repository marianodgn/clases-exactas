import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. Configuración de la página
# ==========================================
st.set_page_config(page_title="Clases Exactas | Contacto", page_icon="📐", layout="centered")

# ==========================================
# 2. Estilos Visuales (CSS Integrado)
# ==========================================
st.markdown("""
    <style>
    .titulo { text-align: center; color: #45a29e; font-size: 3em; font-weight: bold; margin-bottom: 0px; }
    .subtitulo { text-align: center; color: #c5c6c7; font-size: 1.2em; margin-top: 0px; margin-bottom: 30px; }
    .experiencia { text-align: center; background-color: #1f2833; padding: 15px; border-radius: 10px; border-left: 5px solid #66fcf1; color: #fff; font-size: 1.1em; }
    div[data-testid="stForm"] { background-color: rgba(31, 40, 51, 0.4); border: 1px solid #45a29e; border-radius: 10px; padding: 20px;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Encabezado de la página
# ==========================================
st.markdown('<p class="titulo">Ciencias Exactas</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Acompañamiento Académico de Excelencia</p>', unsafe_allow_html=True)
st.markdown('<div class="experiencia">Más de <b>20 años de experiencia</b> formando estudiantes de nivel secundario y universitario.</div><br>', unsafe_allow_html=True)

# ==========================================
# 4. Estructura a dos columnas
# ==========================================
col1, col2 = st.columns([1.1, 1])

# --- Columna Izquierda: Autoridad y Servicios ---
with col1:
    st.subheader("👨‍🏫 Sobre las clases")
    st.write("Soy Mariano, docente universitario e investigador especializado en física y ciencias exactas. Mi formación y experiencia activa en instituciones como FIUBA, UNGS y UNLP me permite conocer exactamente los niveles de exigencia y las metodologías de evaluación actuales.")
    
    st.markdown("### Niveles que preparamos:")
    st.markdown("✅ **Nivel Secundario:** Apoyo escolar, preparación para previas y nivelación para el ingreso a la facultad.")
    st.markdown("✅ **Nivel Universitario:** Ingresos, CBC, Análisis Matemático, Álgebra, Física General, Mecánica Clásica y Electromagnetismo.")
    
    st.info("💡 La metodología de estudio se adapta estrictamente al programa oficial de tu institución.")

# --- Columna Derecha: Formulario de Contacto ---
with col2:
    st.subheader("📬 Formulario de Contacto")
    st.write("Dejame tu consulta. Tus datos son confidenciales y te responderé a la brevedad con disponibilidad y aranceles.")
    
    # st.form agrupa todos los campos y no recarga la página hasta presionar el botón
    with st.form("contacto_form"):
        nombre = st.text_input("Tu Nombre y Apellido *")
        email = st.text_input("Tu Correo Electrónico *")
        nivel = st.selectbox("Nivel Educativo", ["Seleccionar...", "Secundario", "Ingreso Universitario / CBC", "Universitario de Grado"])
        materia = st.text_input("Materia a preparar")
        mensaje = st.text_area("Contame brevemente qué temas necesitas preparar (Opcional)")
        
        # El botón de envío
        enviado = st.form_submit_button("Enviar Consulta 🚀")
        
        # Lógica de validación
        if enviado:
            if not nombre or not email or nivel == "Seleccionar...":
                st.error("⚠️ Por favor, completá tu nombre, email y nivel para poder contactarte.")
            elif "@" not in email:
                st.error("⚠️ Por favor, ingresá una dirección de correo válida.")
            else:
                # -------------------------------------------------------------
                # AQUÍ CONECTARÍAS CON TU GOOGLE SHEETS PARA GUARDAR LOS DATOS
                # usando la misma lógica de "guardar_cartera" de tu terminal.
                # -------------------------------------------------------------
                
                st.success(f"¡Gracias por tu mensaje, {nombre.split()[0]}! Me pondré en contacto a tu email muy pronto.")
                st.balloons()
