import streamlit as st
import numpy as np
import math
import random

# Configuración inicial de la página
st.set_page_config(
    page_title="Zohan Pronostic - Bunker Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS profesionales en modo oscuro
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #f0f6fc; }
    .card { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 20px; }
    .result-box { background-color: #161f2c; border-left: 5px solid #58a6ff; padding: 15px; border-radius: 4px; margin-top: 15px; }
    .verdict-box { background-color: #1a2332; border-left: 5px solid #238636; padding: 15px; border-radius: 4px; margin-top: 15px; }
    .warning-box { background-color: #2b2216; border-left: 5px solid #d29922; padding: 15px; border-radius: 4px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #58a6ff;'>⚽ ZOHAN PRONOSTIC - BUNKER PRO (DIXON-COLES & MONTE CARLO)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Suite analítica unificada: Diagnóstico de comportamiento dual, inercia Fibonacci, perfil automático de liga y simulador estocástico.</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# FUNCIONES AUXILIARES DE MATEMÁTICA Y CONVERSIÓN
# ==========================================
def americano_a_decimal(cuota_am):
    try:
        val = float(cuota_am)
        return round((val / 100.0) + 1.0, 2) if val > 0 else round((100.0 / abs(val)) + 1.0, 2)
    except:
        return None

def decimal_a_americano(dec):
    try:
        dec = float(dec)
        if dec >= 2.0:
            return f"+{int(round((dec - 1.0) * 100))}"
        else:
            return f"{int(round(-100.0 / (dec - 1.0)))}"
    except:
        return "+100"

def calcular_inercia_fibonacci(goles_favor, goles_contra):
    balance = sum(goles_favor) - sum(goles_contra)
    if balance > 3:
        return 1.12, "En racha alcista / Sólido ofensivamente"
    elif balance >= 0:
        return 1.0, "Estable / En línea media competitiva"
    else:
        return 0.88, "En retroceso / Con dudas estructurales"

# ==========================================
# INTERFAZ: TARJETAS DE ENTRADA (DOBLE FACETA)
# ==========================================
col_eq1, col_eq2 = st.columns(2)

with col_eq1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏠 Equipo A (Local)")
    nombre_local = st.text_input("Nombre Local", "Equipo Local", key="nl")
    
    st.markdown("---")
    st.markdown("<b>Faceta de Local (En su casa):</b>", unsafe_allow_html=True)
    ca_g = st.number_input("Ganados (Casa)", 0, 50, 5, key="ca_g")
    ca_e = st.number_input("Empatados (Casa)", 0, 50, 2, key="ca_e")
    ca_p = st.number_input("Perdidos (Casa)", 0, 50, 1, key="ca_p")
    ca_gf = st.number_input("Goles Favor (Casa)", 0, 200, 14, key="ca_gf")
    ca_ga = st.number_input("Goles Contra (Casa)", 0, 200, 6, key="ca_ga")

    st.markdown("<b>Faceta de Visitante (Cuando sale):</b>", unsafe_allow_html=True)
    va_g = st.number_input("Ganados (Fuera A)", 0, 50, 2, key="va_g")
    va_e = st.number_input("Empatados (Fuera A)", 0, 50, 3, key="va_e")
    va_p = st.number_input("Perdidos (Fuera A)", 0, 50, 3, key="va_p")
    va_gf = st.number_input("Goles Favor (Fuera A)", 0, 200, 8, key="va_gf")
    va_ga = st.number_input("Goles Contra (Fuera A)", 0, 200, 10, key="va_ga")
    st.markdown("</div>", unsafe_allow_html=True)

with col_eq2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✈️ Equipo B (Visitante)")
    nombre_vis = st.text_input("Nombre Visitante", "Equipo Visitante", key="nv")
    
    st.markdown("---")
    st.markdown("<b>Faceta de Local (En su casa):</b>", unsafe_allow_html=True)
    cb_g = st.number_input("Ganados (Casa B)", 0, 50, 4, key="cb_g")
    cb_e = st.number_input("Empatados (Casa B)", 0, 50, 2, key="cb_e")
    cb_p = st.number_input("Perdidos (Casa B)", 0, 50, 2, key="cb_p")
    cb_gf = st.number_input("Goles Favor (Casa B)", 0, 200, 12, key="cb_gf")
    cb_ga = st.number_input("Goles Contra (Casa B)", 0, 200, 8, key="cb_ga")

    st.markdown("<b>Faceta de Visitante (Cuando sale):</b>", unsafe_allow_html=True)
    vb_g = st.number_input("Ganados (Fuera B)", 0, 50, 3, key="vb_g")
    vb_e = st.number_input("Empatados (Fuera B)", 0, 50, 3, key="vb_e")
    vb_p = st.number_input("Perdidos (Fuera B)", 0, 50, 2, key="vb_p")
    vb_gf = st.number_input("Goles Favor (Fuera B)", 0, 200, 9, key="vb_gf")
    vb_ga = st.number_input("Goles Contra (Fuera B)", 0, 200, 9, key="vb_ga")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("🎯 Cuotas de Mercado (Opcional - Formato Americano)")
st.markdown("<p style='color: #8b949e; font-size: 13px;'>Déjalas en blanco o vacías si solo deseas el pronóstico estadístico puro.</p>", unsafe_allow_html=True)
col_c1, col_c2 = st.columns(2)
with col_c1:
    cuota_l_am = st.text_input(f"Cuota Americana - {nombre_local} (Ej: +115)", "", key="cam_l")
with col_c2:
    cuota_v_am = st.text_input(f"Cuota Americana - {nombre_vis} (Ej: +230)", "", key="cam_v")

st.markdown("---")

if st.button("🚀 Ejecutar Búnker Analítico Unificado", type="primary", use_container_width=True):
    # 1. PROCESAMIENTO DE PROMEDIOS
    partidos_a_casa = max(1, ca_g + ca_e + ca_p)
    partidos_a_vis = max(1, va_g + va_e + va_p)
    partidos_b_casa = max(1, cb_g + cb_e + cb_p)
    partidos_b_vis = max(1, vb_g + vb_e + vb_p)

    prom_gf_l_casa = ca_gf / partidos_a_casa
    prom_ga_l_casa = ca_ga / partidos_a_casa
    prom_gf_v_vis = vb_gf / partidos_b_vis
    prom_ga_v_vis = vb_ga / partidos_b_vis

    # Inercia Fibonacci y Estados de Comportamiento
    factor_fib_l, estado_l_txt = calcular_inercia_fibonacci([ca_gf, va_gf], [ca_ga, va_ga])
    factor_fib_v, estado_v_txt = calcular_inercia_fibonacci([cb_gf, vb_gf], [cb_ga, vb_ga])

    # xG Base Cruzado
    xg_l = ((prom_gf_l_casa + prom_ga_v_vis) / 2.0) * factor_fib_l
    xg_v = ((prom_gf_v_vis + prom_ga_l_casa) / 2.0) * factor_fib_v
    promedio_global_goles = xg_l + xg_v

    # Detección Automática de Perfil de Liga
    if promedio_global_goles >= 2.8:
        perfil_liga = "Abierta / Alta Goleada (Dinámica ofensiva elevada)"
        factor_ajuste_dc = 0.95
    elif promedio_global_goles <= 2.2:
        perfil_liga = "Cerrada / Táctica (Defensas rocosas / Margen de error bajo)"
        factor_ajuste_dc = 1.18
    else:
        perfil_liga = "Equilibrada / Estándar"
        factor_ajuste_dc = 1.05

    # 2. RADIOGRAFÍA HUMANA Y COMPORTAMENTAL (El diagnóstico narrativo)
    st.markdown("### 📊 Radiografía de Comportamiento y Perfil Operativo")
    st.markdown(f"""
        <div class='result-box'>
            <h4>⚖️ Lectura Dual y Contexto del Partido</h4>
            <p><b>Entorno de Liga Detectado:</b> <code>{perfil_liga}</code> (Expectativa combinada: <b>{promedio_global_goles:.2f} goles</b>)</p>
            <hr style='border-color: #30363d;'>
            <p><b>🏠 {nombre_local} (Local):</b> Estado operativo -> <b>{estado_l_txt}</b>. Sólido en su reducto, evaluando la consistencia defensiva de su contraparte de gira.</p>
            <p><b>✈️ {nombre_vis} (Visitante):</b> Estado operativo -> <b>{estado_v_txt}</b>. Comportamiento competitivo analizado bajo su rendimiento real fuera de casa.</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. MOTOR HÍBRIDO AVANZADO: DIXON-COLES + MONTE CARLO (3,000 iteraciones)
    max_g = 6
    matriz_base = np.zeros((max_g + 1, max_g + 1))

    for i in range(max_g + 1):
        for j in range(max_g + 1):
            p_i = ((xg_l ** i) * math.exp(-xg_l)) / math.factorial(min(i, 20))
            p_j = ((xg_v ** j) * math.exp(-xg_v)) / math.factorial(min(j, 20))
            val = p_i * p_j
            
            # Corrección Dixon-Coles en marcadores bajos
            if i == 0 and j == 0:
                val *= (1.0 - (xg_l * xg_v * 0.05)) * factor_ajuste_dc
            elif (i == 1 and j == 0) or (i == 0 and j == 1):
                val *= factor_ajuste_dc * 0.98
            elif i == 1 and j == 1:
                val *= factor_ajuste_dc
                
            matriz_base[i, j] = max(0.0, val)

    suma_total = np.sum(matriz_base)
    if suma_total > 0:
        matriz_base /= suma_total

    # Simulación Monte Carlo
    flat_probs = matriz_base.flatten()
    flat_probs /= np.sum(flat_probs)
    
    simulaciones = 3000
    resultados_simulados = np.random.choice(len(flat_probs), size=simulaciones, p=flat_probs)
    
    conteo_marcadores = {}
    wins_l, wins_v, empates, overs, btts = 0, 0, 0, 0, 0

    for idx in resultados_simulados:
        i = idx // (max_g + 1)
        j = idx % (max_g + 1)
        
        key = (int(i), int(j))
        conteo_marcadores[key] = conteo_marcadores.get(key, 0) + 1
        
        if i > j:
            wins_l += 1
        elif j > i:
            wins_v += 1
        else:
            empates += 1
            
        if (i + j) > 2.5:
            overs += 1
        if i > 0 and j > 0:
            btts += 1

    p_local = (wins_l / simulaciones) * 100
    p_empate = (empates / simulaciones) * 100
    p_vis = (wins_v / simulaciones) * 100
    p_over = (overs / simulaciones) * 100
    p_btts = (btts / simulaciones) * 100

    top_3_ordenados = sorted(conteo_marcadores.items(), key=lambda x: x[1], reverse=True)[:3]
    top_3_formato = [(k[0], k[1], (v / simulaciones) * 100) for k, v in top_3_ordenados]

    fair_dec_l = (1.0 / (p_local / 100.0)) if p_local > 0 else 99.0
    fair_dec_v = (1.0 / (p_vis / 100.0)) if p_vis > 0 else 99.0
    fair_am_l = decimal_a_americano(fair_dec_l)
    fair_am_v = decimal_a_americano(fair_dec_v)

    if abs(p_local - p_vis) < 7.0 and p_empate > 26.0:
        veredicto_paridad = f"⚠️ <b>Alerta de Zona de Paridad Estricta:</b> El simulador arroja un escenario de fuerzas cerradas. El factor de localía inclina sutilmente la balanza para {nombre_local}, pero el empate técnico tiene un peso muy alto."
    else:
        fav = nombre_local if p_local > p_vis else nombre_vis
        veredicto_paridad = f"🎯 <b>Tendencia Consolidada:</b> La simulación estocástica detecta ventaja estructural en favor de <b>{fav}</b>."

    top_3_html = "".join([f"<li><b>{item[0]} - {item[1]}</b> ({item[2]:.1f}%)</li>" for item in top_3_formato])

    st.markdown(f"""
        <div class='verdict-box'>
            <h4>🔬 Motor Avanzado Pro (Dixon-Coles + Monte Carlo x {simulaciones})</h4>
            <p><b>xG Base Local:</b> <code>{xg_l:.2f}</code> | <b>xG Base Visitante:</b> <code>{xg_v:.2f}</code></p>
            <hr style='border-color: #238636;'>
            <p><b>Victoria {nombre_local}:</b> <b>{p_local:.1f}%</b> | Cuota Justa Americana: <b>{fair_am_l}</b> (Dec: {fair_dec_l:.2f})</p>
            <p><b>Empate:</b> <b>{p_empate:.1f}%</b></p>
            <p><b>Victoria {nombre_vis}:</b> <b>{p_vis:.1f}%</b> | Cuota Justa Americana: <b>{fair_am_v}</b> (Dec: {fair_dec_v:.2f})</p>
            <hr style='border-color: #238636;'>
            <p><b>Ambos Marcan (BTTS):</b> <b>{p_btts:.1f}%</b> | <b>Más de 2.5 Goles:</b> <b>{p_over:.1f}%</b></p>
            <hr style='border-color: #238636;'>
            <p><b>🎯 Top 3 Marcadores Exactos Más Probables (Simulación Estocástica):</b></p>
            <ul>
                {top_3_html}
            </ul>
            <p>{veredicto_paridad}</p>
        </div>
    """, unsafe_allow_html=True)

    # 4. AUDITORÍA FINANCIERA (Opcional)
    dec_ofrecida_l = americano_a_decimal(cuota_l_am)
    dec_ofrecida_v = americano_a_decimal(cuota_v_am)

    if dec_ofrecida_l or dec_ofrecida_v:
        txt_l = ""
        txt_v = ""
        
        if dec_ofrecida_l:
            val_l = dec_ofrecida_l > fair_dec_l
            txt_l = f"🟢 **VALOR OCULTO EN LOCAL ({nombre_local}):** La casa paga <code>{cuota_l_am}</code>, pero el modelo exige un valor justo de <b>{fair_am_l}</b>. Hay margen favorable." if val_l else f"🔴 **SIN VALOR EN LOCAL ({nombre_local}):** La cuota (<code>{cuota_l_am}</code>) castiga el riesgo. El modelo exige al menos <b>{fair_am_l}</b>."
        
        if dec_ofrecida_v:
            val_v = dec_ofrecida_v > fair_dec_v
            txt_v = f"🟢 **VALOR OCULTO EN VISITANTE ({nombre_vis}):** La casa paga <code>{cuota_v_am}</code>, pero el modelo exige un valor justo de <b>{fair_am_v}</b>. Hay margen favorable." if val_v else f"🔴 **SIN VALOR EN VISITANTE ({nombre_vis}):** La cuota (<code>{cuota_v_am}</code>) castiga el riesgo. El modelo exige al menos <b>{fair_am_v}</b>."

        st.markdown(f"""
            <div class='warning-box'>
                <h4>💰 Auditoría de Mercado (Cuotas Americanas)</h4>
                {f"<p>{txt_l}</p>" if txt_l else ""}
                {f"<p>{txt_v}</p>" if txt_v else ""}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No ingresaste cuotas americanas; el búnker operó en modo pronóstico puro y análisis de probabilidades.")

    st.success("✨ ¡Análisis unificado completado con éxito!")

