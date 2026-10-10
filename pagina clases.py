import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 0. CONFIGURACIÓN DE CREDENCIALES
# ==========================================
TU_CORREO = st.secrets["TU_CORREO"]
TU_CONTRASEÑA_APP = st.secrets.get("TU_CONTRASENA_APP", st.secrets.get("TU_CONTRASEÑA_APP"))
TU_CELULAR = st.secrets["TU_CELULAR"]

def enviar_correo(nombre, email_alumno, nivel, materia, mensaje):
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(TU_CORREO, TU_CONTRASEÑA_APP)

        msg = MIMEMultipart()
        msg['From'] = TU_CORREO
        msg['To'] = TU_CORREO 
        msg['Subject'] = f"Nueva Consulta de Clases: {nombre} - {materia}"

        cuerpo = f"""
        NUEVA SOLICITUD DE CLASES (Vía Web)
        
        Datos del Alumno:
        - Nombre: {nombre}
        - Email: {email_alumno}
        - Nivel: {nivel}
        - Materia: {materia}
        
        Mensaje / Temas a preparar:
        {mensaje}
        
        -----------------------------------------
        Para responder, haz clic en "Responder" a: {email_alumno}
        """
        msg.attach(MIMEText(cuerpo, 'plain'))
        servidor.send_message(msg)
        servidor.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

# ==========================================
# 1. CONFIGURACIÓN GENERAL Y CSS 
# ==========================================
st.set_page_config(page_title="Clases Exactas | Acompañamiento Académico", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    /* Tipografía limpia */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* IMAGEN DE FONDO CON VELO BLANCO */
    [data-testid="stAppViewContainer"] {
        /* Capa 1: Velo blanco al 90% | Capa 2: Imagen universitaria/exactas */
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.90), rgba(255, 255, 255, 0.90)), 
            url("https://images.unsplash.com/photo-1543269865-cbf427effbad?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Hacemos transparente el encabezado superior de Streamlit para que no tape el fondo */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Sección Hero (Encabezado principal con efecto translúcido) */
    .hero { 
        text-align: center; 
        padding: 3rem 1rem; 
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px); /* Efecto vidrio esmerilado */
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px; 
        margin-bottom: 2rem; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .hero h1 { font-weight: 900; font-size: 3.2rem; color: #1a1a1a; line-height: 1.2; margin-bottom: 1rem; }
    .hero p { font-size: 1.25rem; color: #4a4a4a; max-width: 700px; margin: 0 auto 2rem auto; }
    
    /* Etiquetas de Materias (Pills) */
    .pills-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-bottom: 2rem; }
    .pill { 
        background-color: rgba(255, 255, 255, 0.9); border: 1px solid #e0e0e0; 
        padding: 10px 20px; border-radius: 50px; font-weight: 600; 
        color: #2c3e50; font-size: 0.95rem; box-shadow: 0 2px 5px rgba(0,0,0,0.02); 
    }
    
    /* Tarjeta del Docente */
    .teacher-card {
        background-color: rgba(255, 255, 255, 0.85); padding: 25px; border-radius: 15px; 
        border-left: 5px solid #0056b3; margin-bottom: 2rem;
        backdrop-filter: blur(5px);
    }
    
    /* Pasos "Cómo funciona" */
    .step-container { display: flex; align-items: flex-start; margin-bottom: 1.5rem; }
    .step-icon { 
        background-color: #0056b3; color: white; width: 35px; height: 35px; 
        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
        font-weight: bold; font-size: 1.1rem; margin-right: 15px; flex-shrink: 0; 
    }
    .step-text h4 { margin: 0 0 5px 0; font-weight: 700; color: #1a1a1a; font-size: 1.1rem;}
    .step-text p { margin: 0; color: #555; font-size: 1rem; line-height: 1.5; }
    
    /* Formulario de Contacto (Destacado) */
    div[data-testid="stForm"] { 
        background-color: rgba(255, 255, 255, 0.95); 
        border: 1px solid #eaeaea; 
        border-radius: 20px; 
        padding: 35px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        backdrop-filter: blur(5px);
    }
    
    /* Botón WhatsApp */
    .whatsapp-btn { 
        display: flex; align-items: center; justify-content: center; gap: 10px;
        background-color: #25D366; color: white !important; padding: 15px 20px; 
        text-decoration: none; border-radius: 12px; font-weight: 700; 
        font-size: 1.1rem; transition: transform 0.2s, background-color 0.2s; 
        box-shadow: 0 4px 15px rgba(37,211,102,0.3); margin-top: 1rem; 
    }
    .whatsapp-btn:hover { background-color: #1ebc59; transform: translateY(-3px); }
    
    /* Aviso de disponibilidad */
    .disclaimer-box {
        background-color: rgba(252, 252, 252, 0.9);
        border: 1px dashed #cccccc;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        font-size: 0.85rem;
        color: #666666;
        line-height: 1.4;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SECCIÓN HERO (Encabezado)
# ==========================================
st.markdown("""
<div class="hero">
    <h1>Clases Particulares de Ciencias Exactas a Medida</h1>
    <p>Acompañamiento académico personalizado para Universidad (UBA), CBC y Nivel Secundario.</p>
    <div class="pills-container">
        <span class="pill">Análisis Matemático</span>
        <span class="pill">Introducción a la Matemática</span>
        <span class="pill">Álgebra</span>
        <span class="pill">Física General</span>
        <span class="pill">Mecánica</span>
        <span class="pill">Biofísica</span>
        <span class="pill">Electricidad y Magnetismo</span>
        <span class="pill">Óptica y Ondas</span>
        <span class="pill">Química Inorgánica</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. MÉTRICAS
# ==========================================
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="Experiencia Docente", value="+20 Años")
m2.metric(label="Alumnos Aprobados", value="+500")
m3.metric(label="Universidades", value="UBA")
m4.metric(label="Modalidad", value="Online / Presencial")
st.write("---")

# ==========================================
# 4. ESTRUCTURA PRINCIPAL (2 Columnas)
# ==========================================
col_info, col_form = st.columns([1.1, 1], gap="large")

with col_info:
    # Perfil del docente
    st.markdown("""
    <div class="teacher-card">
        <h3 style="margin-top:0;">👨‍🏫 Sobre el Docente</h3>
        <p style="margin-bottom:0; font-size: 1.05rem; color: #333;">
        Soy docente universitario e investigador. Mi formación en ciencias exactas y mi experiencia diaria en las aulas me permiten brindarte herramientas concretas, métodos claros y el enfoque exacto para superar los exámenes más exigentes.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ¿Cómo funciona el proceso?")
    st.write("Te acompaño paso a paso para que recuperes la confianza y apruebes.")
    
    st.markdown("""
    <div class="step-container">
        <div class="step-icon">1</div>
        <div class="step-text">
            <h4>Analizamos lo que necesitás</h4>
            <p>Evaluamos tu nivel actual, los temas específicos que te cuestan y las fechas de tus próximos exámenes.</p>
        </div>
    </div>
    <div class="step-container">
        <div class="step-icon">2</div>
        <div class="step-text">
            <h4>Enfoque a medida</h4>
            <p>Trabajamos directamente sobre los conceptos y ejercicios que requieren mayor refuerzo, adaptándonos al enfoque de tu cátedra.</p>
        </div>
    </div>
    <div class="step-container">
        <div class="step-icon">3</div>
        <div class="step-text">
            <h4>Empezamos las clases</h4>
            <p>Clases dinámicas, con resolución de ejercicios de parciales y finales reales para que vayas 100% seguro a rendir.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Botón WhatsApp
    url_whatsapp = f"https://wa.me/{TU_CELULAR}?text=Hola,%20te%20escribo%20desde%20tu%20página%20web%20para%20consultar%20por%20clases."
    st.markdown(f'<a href="{url_whatsapp}" target="_blank" class="whatsapp-btn">💬 Consultar disponibilidad por WhatsApp</a>', unsafe_allow_html=True)

with col_form:
    st.markdown("<h3 style='margin-bottom: 0px;'>📬 Solicitar información</h3>", unsafe_allow_html=True)
    st.write("Tus datos son confidenciales. Te responderé a la brevedad con aranceles y horarios disponibles.")
    
    with st.form("contacto_form"):
        nombre = st.text_input("Tu Nombre Completo *", placeholder="Ej: Juan Pérez")
        email = st.text_input("Correo Electrónico *", placeholder="ejemplo@gmail.com")
        
        nivel = st.selectbox("Nivel Educativo *", ["Seleccionar...", "Secundario", "Ingreso / CBC", "Universitario de Grado"])
        materia = st.text_input("Materia específica a preparar *")
            
        mensaje = st.text_area("Comentarios (Opcional)", height=120, placeholder="Contame qué temas necesitás reforzar o si tenés una fecha de examen próxima...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        enviado = st.form_submit_button("Solicitar mis clases 🚀", use_container_width=True)
        
        if enviado:
            if not nombre or not email or not materia or nivel == "Seleccionar...":
                st.error("⚠️ Por favor, completá los campos obligatorios (*).")
            elif "@" not in email:
                st.error("⚠️ El formato del correo no es válido.")
            else:
                with st.spinner('Enviando tu consulta...'):
                    exito = enviar_correo(nombre, email, nivel, materia, mensaje)
                
                if exito:
                    st.success(f"✅ ¡Excelente, {nombre.split()[0]}! Recibí tu solicitud. Te voy a estar contactando por correo a la brevedad.")
                    st.balloons()
                else:
                    st.error("Hubo un error temporal. Por favor, utilizá el botón de WhatsApp de la izquierda.")

    # Aviso de disponibilidad limitado y urgencias (Aclaración profesional)
    st.markdown("""
    <div class="disclaimer-box">
        <strong>Aviso importante sobre disponibilidad:</strong><br>
        Debido a mis compromisos de docencia e investigación universitaria, mi agenda suele estar completa. Si no recibís una respuesta a tu consulta a la brevedad, te ruego desestimarla, ya que significará que lamentablemente no cuento con cupos disponibles en este momento. Por este motivo, <strong>no es posible atender urgencias a pocos días de un examen</strong>. Gracias por comprender.
    </div>
    """, unsafe_allow_html=True)
# ==========================================
# 5. SECCIÓN DE OPINIONES / RESEÑAS (Google Maps)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #1a1a1a; margin-bottom: 30px;'>⭐ Lo que dicen los alumnos</h2>", unsafe_allow_html=True)

# Creamos 3 columnas para mostrar las opiniones tipo tarjeta
col_res1, col_res2, col_res3 = st.columns(3, gap="medium")

with col_res1:
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; height: 100%;">
        <p style="color: #f39c12; font-size: 1.2rem; margin: 0;">★★★★★</p>
        <p style="font-style: italic; color: #333; margin: 10px 0;">"Eternamente agradecida un excelente profesor que sabe transmitir sus conocimientos con toda la paciencia del mundo. Preparo a mí nene para rendir matemáticas y aprobó sin ningún error. Feliz de haber encontrado un profesor como vos que le dio a mí nene las herramientas que necesitaba para ser  resolutivo y lo más importante le diste la confianza que le faltaba para sentirse seguro.
Todos los laureles para vos y vamos por más para que lo prepares para el curso de ingreso a la universidad."</p>
        <p style="font-weight: bold; color: #555; margin: 0; font-size: 0.9rem;">— Karina</p>
    </div>
    """, unsafe_allow_html=True)

with col_res2:
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; height: 100%;">
        <p style="color: #f39c12; font-size: 1.2rem; margin: 0;">★★★★★</p>
        <p style="font-style: italic; color: #333; margin: 10px 0;">"Excelente profesor! Es súper didáctico, explica los temas de forma clara, rápida y sencilla. Se preocupa que entiendas y hace las clases entretenidas. Me ayudó a preparar mis parciales y finales de la universidad. 100% recomendado"</p>
        <p style="font-weight: bold; color: #555; margin: 0; font-size: 0.9rem;">— Ayelen</p>
    </div>
    """, unsafe_allow_html=True)

with col_res3:
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; height: 100%;">
        <p style="color: #f39c12; font-size: 1.2rem; margin: 0;">★★★★★</p>
        <p style="font-style: italic; color: #333; margin: 10px 0;">"Excelente profesor Mariano, siempre atento a que entiendas y las clases super dinámicas además de estar siempre en contacto para lo que precises. Quedan pocos como el!

Super recomendable!."</p>
        <p style="font-weight: bold; color: #555; margin: 0; font-size: 0.9rem;">— Marcos</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)



# Footer
st.markdown("<br><br><hr><center><small>© 2026. Buenos Aires, Argentina. Todos los derechos reservados.</small></center>", unsafe_allow_html=True)
