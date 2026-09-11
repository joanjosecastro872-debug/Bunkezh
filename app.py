import streamlit as st
import numpy as np
import math
import random

# Configuración inicial de la página en modo ancho
st.set_page_config(
    page_title="Zohan Pronostic - Bunker Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS profesionales: Fondo oscuro profundo #060913 y Tarjetas 3D Neón
st.markdown("""
    <style>
    .stApp { 
        background-color: #060913; 
        color: #f0f6fc; 
    }
    
    /* Cabecera Pro Banner 3D Neón */
    .bunker-header {
        background: linear-gradient(135deg, #121824 0%, #1b2233 100%);
        border: 2px solid #bc8cff;
        box-shadow: 0 0 20px rgba(188, 140, 255, 0.25);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 25px;
    }
    .bunker-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .bunker-subtitle-red {
        color: #ff7b72;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }
    .bunker-desc {
        color: #c9d1d9;
        font-size: 13px;
    }

    /* Tarjetas de Equipo Estilo 3D Neón Horizontal */
    .team-card-purple {
        background: #121824;
        border: 2px solid #bc8cff;
        box-shadow: 0 0 15px rgba(188, 140, 255, 0.15);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .team-card-blue {
        background: #121824;
        border: 2px solid #58a6ff;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.15);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .card-title-p { color: #bc8cff; font-size: 16px; font-weight: bold; margin-bottom: 10px; }
    .card-title-b { color: #58a6ff; font-size: 16px; font-weight: bold; margin-bottom: 10px; }
    .facet-header { font-size: 13px; font-weight: bold; color: #c9d1d9; margin-top: 12px; margin-bottom: 6px; }

    /* Cajas de Resultados */
    .result-box { background-color: #121824; border: 2px solid #58a6ff; box-shadow: 0 0 15px rgba(88, 166, 255, 0.15); padding: 20px; border-radius: 14px; margin-top: 20px; }
    .verdict-box { background-color: #121824; border: 2px solid #238636; box-shadow: 0 0 15px rgba(35, 134, 54, 0.2); padding: 20px; border-radius: 14px; margin-top: 20px; }
    .trend-box { background-color: #121824; border: 2px solid #a371f7; box-shadow: 0 0 15px rgba(163, 113, 247, 0.15); padding: 20px; border-radius: 14px; margin-top: 20px; }
    .warning-box { background-color: #121824; border: 2px solid #d29922; box-shadow: 0 0 15px rgba(210, 153, 34, 0.15); padding: 20px; border-radius: 14px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# CABECERA 3D CANDELOSA
# ----------------------------------------------------
st.markdown("""
<div class="bunker-header">
    <div class="bunker-title">⚽ ZOHAN PRONOSTIC</div>
    <div class="bunker-subtitle-red">BÚNKERS PRO (UNIFIED ENGINE)</div>
    <div class="bunker-desc">Suite analítica avanzada: Diagnóstico inteligente de doble cara completo, ELO, perfiles de liga y motor de Monte Carlo para ambos equipos.</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# FUNCIONES AUXILIARES DE CONVERSIÓN Y MATEMÁTICA
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

