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
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.90), rgba(255, 255, 255, 0.90)), 
            url("https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* CORRECCIÓN ANTI-MODO OSCURO PARA CELULARES */
    /* Fuerza textos oscuros en métricas y labels de formulario */
    [data-testid="stMetricValue"] > div, [data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    .stTextInput label p, .stSelectbox label p, .stTextArea label p {
        color: #1a1a1a !important;
        font-weight: 500;
    }
    
    /* Hero */
    .hero { 
        text-align: center; 
        padding: 3rem 1rem; 
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px); 
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px; 
        margin-bottom: 2rem; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .hero h1 { font-weight: 900; font-size: clamp(2rem, 5vw, 3.2rem); color: #1a1a1a; line-height: 1.2; margin-bottom: 1rem; }
    .hero p { font-size: clamp(1rem, 3vw, 1.25rem); color: #4a4a4a; max-width: 700px; margin: 0 auto 2rem auto; }
    
    /* Pills */
    .pills-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-bottom: 2rem; }
    .pill { 
        background-color: rgba(255, 255, 255, 0.9); border: 1px solid #e0e0e0; 
        padding: 8px 16px; border-radius: 50px; font-weight: 600; 
        color: #2c3e50; font-size: 0.9rem; box-shadow: 0 2px 5px rgba(0,0,0,0.02); 
    }
    
    /* Tarjetas y Contenedores */
    .teacher-card {
        background-color: rgba(255, 255, 255, 0.85); padding: 25px; border-radius: 15px; 
        border-left: 5px solid #0056b3; margin-bottom: 2rem;
        backdrop-filter: blur(5px);
    }
    
    .step-container { display: flex; align-items: flex-start; margin-bottom: 1.5rem; }
    .step-icon { 
        background-color: #0056b3; color: white !important; width: 35px; height: 35px; 
        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
        font-weight: bold; font-size: 1.1rem; margin-right: 15px; flex-shrink: 0; 
    }
    .step-text h4 { margin: 0 0 5px 0; font-weight: 700; color: #1a1a1a !important; font-size: 1.1rem;}
    .step-text p { margin: 0; color: #333333 !important; font-size: 1rem; line-height: 1.5; }
    
    div[data-testid="stForm"] { 
        background-color: rgba(255, 255, 255, 0.95); 
        border: 1px solid #eaeaea; 
        border-radius: 20px; 
        padding: clamp(15px, 5vw, 35px);
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        backdrop-filter: blur(5px);
    }
    
    .whatsapp-btn { 
        display: flex; align-items: center; justify-content: center; gap: 10px;
        background-color: #25D366; color: white !important; padding: 15px 20px; 
        text-decoration: none; border-radius: 12px; font-weight: 700; 
        font-size: 1.1rem; transition: transform 0.2s, background-color 0.2s; 
        box-shadow: 0 4px 15px rgba(37,211,102,0.3); margin-top: 1rem; 
        text-align: center;
    }
    .whatsapp-btn:hover { background-color: #1ebc59; transform: translateY(-3px); }
    
    .disclaimer-box {
        background-color: rgba(252, 252, 252, 0.9);
        border: 1px dashed #cccccc;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        font-size: 0.85rem;
        color: #4a4a4a;
        line-height: 1.4;
    }

    /* GRID RESPONSIVE PARA RESEÑAS */
    .reviews-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-bottom: 2rem;
    }
    .review-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .review-card p.stars { color: #f39c12; font-size: 1.2rem; margin: 0; }
    .review-card p.text { font-style: italic; color: #333; margin: 15px 0; flex-grow: 1; font-size: 0.95rem; line-height: 1.5; }
    .review-card p.author { font-weight: bold; color: #555; margin: 0; font-size: 0.9rem; text-align: right; }
    
    /* AJUSTES PARA CELULARES */
    @media (max-width: 768px) {
        .step-container { flex-direction: column; align-items: center; text-align: center; }
        .step-icon { margin-right: 0; margin-bottom: 10px; }
        div[data-testid="column"] { width: 100% !important; min-width: 100% !important; flex: 1 1 100% !important; }
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

st.markdown("<hr style='border: 1px solid #eaeaea;'>", unsafe_allow_html=True)

# ==========================================
# 4. ESTRUCTURA PRINCIPAL (2 Columnas)
# ==========================================
col_info, col_form = st.columns([1.1, 1], gap="large")

with col_info:
    st.markdown("""
    <div class="teacher-card">
        <h3 style="margin-top:0; color: #1a1a1a;">👨‍🏫 Sobre el Docente</h3>
        <p style="margin-bottom:0; font-size: 1.05rem; color: #333;">
        Soy docente universitario e investigador. Mi formación en ciencias exactas y mi experiencia diaria en las aulas me permiten brindarte herramientas concretas, métodos claros y el enfoque exacto para superar los exámenes más exigentes.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #1a1a1a; margin-top: 10px;'>¿Cómo funciona el proceso?</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4a4a4a; margin-bottom: 20px;'>Te acompaño paso a paso para que recuperes la confianza y apruebes.</p>", unsafe_allow_html=True)
    
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

    url_whatsapp = f"https://wa.me/{TU_CELULAR}?text=Hola,%20te%20escribo%20desde%20tu%20página%20web%20para%20consultar%20por%20clases."
    st.markdown(f'<a href="{url_whatsapp}" target="_blank" class="whatsapp-btn">💬 Consultar disponibilidad por WhatsApp</a>', unsafe_allow_html=True)

with col_form:
    st.markdown("<h3 style='margin-bottom: 0px; color: #1a1a1a;'>📬 Solicitar información</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4a4a4a; margin-bottom: 15px;'>Tus datos son confidenciales. Te responderé a la brevedad con aranceles y horarios disponibles.</p>", unsafe_allow_html=True)
    
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

    st.markdown("""
    <div class="disclaimer-box">
        <strong style="color: #1a1a1a;">Aviso importante sobre disponibilidad:</strong><br>
        Debido a mis compromisos de docencia e investigación universitaria, mi agenda suele estar completa. Si no recibís una respuesta a tu consulta a la brevedad, te ruego desestimarla, ya que significará que lamentablemente no cuento con cupos disponibles en este momento. Por este motivo, <strong style="color: #1a1a1a;">no es posible atender urgencias a pocos días de un examen</strong>. Gracias por comprender.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. SECCIÓN DE OPINIONES / RESEÑAS (Responsive)
# ==========================================
st.markdown("<br><hr style='border: 1px solid #eaeaea;'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #1a1a1a; margin-bottom: 30px;'>⭐ Lo que dicen las reseñas de mis alumnas y alumnos </h2>", unsafe_allow_html=True)

# Grilla con las 15 reseñas
st.markdown("""
<div class="reviews-grid">
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Eternamente agradecida un excelente profesor que sabe transmitir sus conocimientos con toda la paciencia del mundo. Preparo a mí nene para rendir matemáticas y aprobó sin ningún error. Feliz de haber encontrado un profesor como vos que le dio a mí nene las herramientas que necesitaba para ser resolutivo y lo más importante le diste la confianza que le faltaba para sentirse seguro. Todos los laureles para vos y vamos por más para que lo prepares para el curso de ingreso a la universidad."</p>
        <p class="author">— Karina</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Excelente profesor Mariano, siempre atento a que entiendas y las clases super dinámicas además de estar siempre en contacto para lo que precises. Quedan pocos como el! Super recomendable!."</p>
        <p class="author">— Marcos</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Excelente docente y persona! Es muy práctico y muy seguro con sus conocimientos.💫"</p>
        <p class="author">— Melissa</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Excelente profesional, muy buena persona, súper paciente y atento a todo! Lo queremos❤️⭐️"</p>
        <p class="author">— Debora</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"El mejor que pude encontrar muy copado y te explica las veces que quieras, la verdad súper recomendado"</p>
        <p class="author">— Maximo</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Excelente profesor!! Tiene una forma de explicar las cosas muy buena hasta llegar a entender lo que no entendiste. Muy recomendable!"</p>
        <p class="author">— Tiziana</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Muy buen profe,explica muy bien recomendable."</p>
        <p class="author">— Gastón</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"El mejor profesor que pude encontrar sin duda ! Explica súper bien y es muy paciente , súper recomendado!"</p>
        <p class="author">— Lur</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"El profesor Mariano , el mejor de todos , le explico a mi hijo , estamos felices saco 10!!!!! Geniooo super recomendable"</p>
        <p class="author">— Natalia</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"muy buena enseñanza y muy atento con sus alumnos!! Gracias Mariano"</p>
        <p class="author">— Delfina</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"El mejor profesor que pude encontrar sin duda ! Explica súper bien y es muy paciente ,te va a explicar las veces que sea necesario hasta que lo entiendas , súper recomendado!"</p>
        <p class="author">— Mikaa</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Es un profesor excelente, me ayudo a rendir 5 temas en dos semanas! Es muy bueno para explicar de una forma mas específica para alguien que le cuesta más entender (como a mí) Súper súper recomendable"</p>
        <p class="author">— Facundo</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Excelente profesor, sabe explicar y busca la forma para que lo entiendas. Se preocupa por sus alumnos y que les vaya bien. Muy recomendable"</p>
        <p class="author">— Leonardo</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Muy contenta con el profe,explica muy bien. Lo super recomiendo!"</p>
        <p class="author">— Alejandra</p>
    </div>
    <div class="review-card">
        <p class="stars">★★★★★</p>
        <p class="text">"Super recomendable! Explica muy bien, tiene paciencia, aprobé mis 2 parciales 🙂 Exelente profesor!!"</p>
        <p class="author">— Florencia</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<br><center><small style='color: #4a4a4a;'>© 2026. Buenos Aires, Argentina. Todos los derechos reservados.</small></center>", unsafe_allow_html=True)
