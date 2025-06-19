import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import os

import streamlit as st
import base64

def home():
    def get_base64_of_image(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return encoded
    path_img = r"C:\Users\victo\Downloads\Cycling_points_uci_VFG\docs\logo.png"  # Asegúrate de que la ruta sea correcta
    img_base64 = get_base64_of_image(path_img)

    # Ocultar menú y pie de página
    if os.path.exists(path_img):
        img_base64 = get_base64_of_image(path_img)

        st.markdown(f"""
        <style>
        body {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .overlay {{
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            background-color: rgba(0,0,0,0.5);
            z-index: 0;
        }}
        h1, p {{
            position: relative;
            z-index: 1;
            color: white;
            text-align: center;
        }}
        </style>
        <div class="overlay"></div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Imagen no encontrada en la ruta especificada.")



def mostrar_graficos_riders(df):
    st.subheader("📊 Gráficos de Riders")
    if df.empty:
        st.write("No hay datos para mostrar.")
        return
    fig, ax = plt.subplots()
    sns.histplot(df["Age"], bins=10, kde=True, ax=ax)
    ax.set_title("Distribución de edades")
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    sns.boxplot(x="Specialty", y=df["Time"].apply(lambda x: sum(int(t)*60**i for i,t in enumerate(reversed(x.split(':'))))), data=df, ax=ax2)
    ax2.set_title("Tiempo por tipo (en segundos)")
    st.pyplot(fig2)

def mostrar_graficos_stages(df):
    st.subheader("📈 Perfil de etapas")
    # Filtros de Año y Carrera
    anios = sorted(df["Año"].unique())
    carreras = sorted(df["Carrera"].unique())

    anio_seleccionado = st.selectbox("Selecciona el año", anios)
    carrera_seleccionada = st.selectbox("Selecciona la carrera", carreras)

    # Filtrado del DataFrame
    df_filtrado = df[(df["Año"] == anio_seleccionado) & (df["Carrera"] == carrera_seleccionada)]
    if df_filtrado.empty:
        st.warning("No hay datos para el año y carrera seleccionados.")
        return
    # Slider de etapas
    sliders = st.slider("Número de etapas a mostrar", 1, len(df_filtrado), (1, min(21, len(df_filtrado))))
    df2 = df_filtrado.iloc[sliders[0]-1:sliders[1]]
    # Gráfico de líneas
    st.line_chart(data=df2.set_index("Stage")[["kms", "Vertical_meters"]])  
    # Tabla de datos
    st.dataframe(df2[["Stage", "Route", "kms", "Vertical_meters", "ProfileScore"]])


def mostrar_importancia(modelo, columnas, titulo="Importancia de variables"):
    importancias = modelo.feature_importances_
    indices = sorted(range(len(importancias)), key=lambda i: importancias[i], reverse=True)
    
    plt.figure(figsize=(10,6))
    sns.barplot(x=[importancias[i] for i in indices], y=[columnas[i] for i in indices])
    plt.title(titulo)
    plt.tight_layout()
    st.pyplot(plt)

def mostrar_comparaciones(df):
    st.subheader("📊 Puntos por Ciclista")
    if df.empty:
        st.write("No hay datos para mostrar.")
        return
    print( df.columns)
    # Comparación de puntos por corredor
    puntos_por_rider = df.groupby("Rider")["UCI"].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x="UCI", y="Rider", data=puntos_por_rider, ax=ax)
    ax.set_title("Puntos Totales por Ciclista")
    st.pyplot(fig)
    
    st.dataframe(puntos_por_rider)

        # Comparación de puntos por equipo
    st.subheader("Puntos por equipo")
    equipo_points = df.groupby("Team")["UCI"].sum().reset_index().sort_values(by="UCI", ascending=False)
    fig_equipos = px.bar(equipo_points, x="Team", y="UCI", title="Puntos totales por equipo")
    st.plotly_chart(fig_equipos)

    # Distribución por tipo de etapa
    #st.subheader("Distribución de puntos por tipo de etapa")
    #tipo_etapa_points = df_filtered.groupby("tipo_etapa")["UCI"].sum().reset_index()
    #fig_tipo_etapa = px.pie(tipo_etapa_points, names="tipo_etapa", values="UCI", title="Distribución de puntos por tipo de etapa")
    #st.plotly_chart(fig_tipo_etapa)

    # Comparación entre dos ciclistas
    st.subheader("Comparación entre dos ciclistas")
    corredores_disponibles = df["Rider"].unique()
    cic1 = st.selectbox("Ciclista 1", corredores_disponibles)
    cic2 = st.selectbox("Ciclista 2", corredores_disponibles, index=1 if len(corredores_disponibles) > 1 else 0)

    df_comp = df[df["Rider"].isin([cic1, cic2])]
    fig_comp = px.line(df_comp, x="Etapa", y="UCI", color="Rider", title=f"Comparación de puntos por etapa entre {cic1} y {cic2}")
    st.plotly_chart(fig_comp)


