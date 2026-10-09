import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
import os

# ==========================================
# 0. CONFIGURACIÓN DE CREDENCIALES
# ==========================================
TU_CORREO = st.secrets["TU_CORREO"]
TU_CONTRASENA_APP = st.secrets["TU_CONTRASENA_APP"]
TU_CELULAR = st.secrets["TU_CELULAR"]

def enviar_correo(nombre, email_alumno, nivel, materia, mensaje):
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(TU_CORREO, TU_CONTRASEÑA_APP)

        msg = MIMEMultipart()
        msg['From'] = TU_CORREO
        msg['To'] = TU_CORREO 
        msg['Subject'] = f"Nueva Consulta Académica: {nombre} - {materia}"

        cuerpo = f"""
        NUEVA CONSULTA DE CLASES
        
        Datos del Alumno:
        - Nombre: {nombre}
        - Email: {email_alumno}
        - Nivel: {nivel}
        - Materia: {materia}
        
        Mensaje / Temas a preparar:
        {mensaje}
        
        -----------------------------------------
        Para responder directamente, haz clic en responder a: {email_alumno}
        """
        msg.attach(MIMEText(cuerpo, 'plain'))
        servidor.send_message(msg)
        servidor.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

# ==========================================
# 1. CONFIGURACIÓN GENERAL Y ESTILOS
# ==========================================
# Se cambió el título de la pestaña para que no tenga nombre personal
st.set_page_config(page_title="Clases Exactas | Acompañamiento Académico", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    /* Estilos Generales y Tipografía */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Contenedores principales */
    .hero-section {
        background: linear-gradient(135deg, #0a192f 0%, #172a45 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .hero-title { font-size: 3.5em; font-weight: 700; margin-bottom: 10px; color: #64ffda; }
    .hero-subtitle { font-size: 1.5em; font-weight: 300; opacity: 0.9; }
    
    /* Tarjetas de servicios */
    .service-card {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        border-top: 4px solid #64ffda;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 100%;
        color: #333;
    }
    
    /* Formulario y botones */
    div[data-testid="stForm"] { 
        background-color: #f8f9fa; 
        border: 1px solid #e9ecef; 
        border-radius: 15px; 
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    .whatsapp-btn { 
        display: block; 
        background-color: #25D366; 
        color: white !important; 
        padding: 15px 20px; 
        text-align: center; 
        text-decoration: none; 
        font-size: 1.1em; 
        border-radius: 8px; 
        font-weight: 600; 
        margin-top: 20px; 
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(37,211,102,0.3);
    }
    .whatsapp-btn:hover { background-color: #128C7E; transform: translateY(-2px); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SECCIÓN HERO (Encabezado Moderno)
# ==========================================
banner_path = "banner_ciencias.jpg"
if os.path.exists(banner_path):
    st.image(Image.open(banner_path), use_column_width=True)

st.markdown("""
<div class="hero-section">
    <div class="hero-title">Acompañamiento Académico Universitario</div>
    <div class="hero-subtitle">Excelencia en Ciencias Exactas, Física y Matemáticas</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. MÉTRICAS Y EXPERIENCIA
# ==========================================
st.write("---")
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="Años de Experiencia", value="+20", delta="Docencia")
m2.metric(label="Universidad", value="UBA", delta="Investigación")
m3.metric(label="Alumnos Aprobados", value="+500", delta="Tasa de Éxito Alta")
m4.metric(label="Modalidad", value="Presencial / Online", delta="Adaptable")
st.write("---")

# ==========================================
# 4. CUERPO PRINCIPAL (2 Columnas)
# ==========================================
col_info, col_form = st.columns([1.2, 1])

with col_info:
    perfil_path = "foto_perfil.jpg"
    texto_docente = "Soy docente universitario e investigador. Mi formación en ciencias exactas y mi experiencia diaria en las aulas me permiten brindarte herramientas concretas para superar los exámenes más exigentes."
    
    if os.path.exists(perfil_path):
        col_foto, col_texto = st.columns([1, 2])
        with col_foto:
            st.image(Image.open(perfil_path), use_column_width=True)
        with col_texto:
            st.markdown("### El Docente")
            st.write(texto_docente)
    else:
        st.markdown("### 👨‍🏫 Sobre las clases")
        st.write(texto_docente)
    
    st.write("")
    
    # Tarjetas de Niveles
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="service-card">
            <h4>📚 Nivel Universitario</h4>
            <p>Preparación rigurosa para parciales y finales. Análisis Matemático, Introducción a Matemática, Álgebra, Física General y Mecánica.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="service-card">
            <h4>🎓 Ingreso y Secundario</h4>
            <p>Nivelación para el CBC, ingreso a ingenierías, y apoyo para exámenes previos o regulares del secundario.</p>
        </div>
        """, unsafe_allow_html=True)

    # Botón WhatsApp
    url_whatsapp = f"https://wa.me/{TU_CELULAR}?text=Hola,%20te%20escribo%20desde%20tu%20página%20web%20para%20consultar%20por%20clases."
    st.markdown(f'<a href="{url_whatsapp}" target="_blank" class="whatsapp-btn">💬 Contactar por WhatsApp</a>', unsafe_allow_html=True)

with col_form:
    st.markdown("### 📬 Solicitar Presupuesto y Horarios")
    st.write("Tus datos son confidenciales. Detallá tu necesidad y te responderé a la brevedad.")
    
    with st.form("contacto_form"):
        nombre = st.text_input("Tu Nombre Completo *", placeholder="Ej: Juan Pérez")
        email = st.text_input("Correo Electrónico *", placeholder="ejemplo@gmail.com")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nivel = st.selectbox("Nivel Educativo *", ["Seleccionar...", "Secundario", "Ingreso / CBC", "Universitario de Grado"])
        with col_f2:
            materia = st.text_input("Materia específica *")
            
        mensaje = st.text_area("Temario a preparar (Opcional)", height=100, placeholder="Escribí los temas principales, si tenés fecha de examen, etc.")
        
        st.markdown("---")
        enviado = st.form_submit_button("Enviar Consulta Oficial 🚀", use_container_width=True)
        
        if enviado:
            if not nombre or not email or not materia or nivel == "Seleccionar...":
                st.error("⚠️ Por favor, completá los campos obligatorios (*).")
            elif "@" not in email:
                st.error("⚠️ El formato del correo no es válido.")
            else:
                with st.spinner('Enviando consulta segura...'):
                    exito = enviar_correo(nombre, email, nivel, materia, mensaje)
                
                if exito:
                    st.success(f"✅ ¡Excelente, {nombre.split()[0]}! Tu solicitud fue registrada con éxito.")
                    st.balloons()
                else:
                    st.error("Hubo un error de conexión. Por favor, utilizá el botón de WhatsApp a la izquierda.")

# Footer
st.markdown("<br><br><hr><center><small>© 2026. Buenos Aires, Argentina. Todos los derechos reservados.</small></center>", unsafe_allow_html=True)
