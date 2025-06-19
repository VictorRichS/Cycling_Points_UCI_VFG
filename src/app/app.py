import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


import streamlit as st
import pandas as pd
import os
from utils.filtros import aplicar_filtros_riders
from utils.filtros import aplicar_filtros_comparaciones
from utils.visualizaciones import mostrar_graficos_riders, mostrar_graficos_stages, mostrar_comparaciones
from utils.modelo import  cargar_modelo 


#folder_path = r"C:\Users\victo\Downloads\Cycling_points_uci_VFG"
#sys.path.append(folder_path)

#from utils.visualizaciones import mostrar_graficos_riders, mostrar_graficos_stages
#from utils.modelo import entrenar_modelo, hacer_prediccion

# Asegurarse de que el directorio src esté en el path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


st.set_page_config(page_title="Ciclismo ML", layout="wide")

st.title("Análisis y Predicción de Puntos UCI en las Grandes Vueltas")
st.markdown("Compara el rendimiento de ciclistas y equipos en el Tour, Giro y Vuelta y predice puntos futuros")

csv_folder = r"C:\Users\victo\Downloads\Cycling_points_uci_VFG\data\processed"  # Cambia esto según tu estructura de carpetas
csv_riders = os.path.join(csv_folder, 'all_stages.csv')
csv_stages = os.path.join(csv_folder, 'profiles_all_stages.csv')

# Cargar datos
riders = pd.read_csv(csv_riders)
stages = pd.read_csv(csv_stages, parse_dates=["Date"], dayfirst=True)

opcion = st.sidebar.selectbox("Selecciona opción", [
    "🏠 Inicio" , "📊 Riders", "🔢 Stages" , "🔁 Comparaciones", "🔎  Modelo y predicción"])

if opcion == "🏠 Inicio":
    st.markdown("""
    ## Bienvenido a la App de Análisis de Ciclismo
    Esta aplicación te permite explorar datos de ciclistas y etapas, visualizar gráficos y entrenar modelos de predicción.
    
    ### Opciones:
    - **📊 Riders**: Explora los datos de los ciclistas.
    - **🔢 Stages**: Visualiza el perfil de las etapas.
    - **🔁 Comparaciones**: Compara el rendimiento de ciclistas y equipos.
    - **🔎 Modelo y predicción**: Entrena un modelo para predecir puntos UCI.
    """)
elif opcion == "📊 Riders":
    df = aplicar_filtros_riders(riders)
    mostrar_graficos_riders(df)
elif opcion == "🔢 Stages":
    mostrar_graficos_stages(stages)
elif opcion == "🔁 Comparaciones" :
    df = aplicar_filtros_comparaciones(riders)
    mostrar_comparaciones(df)
else:
    cargar_modelo()

