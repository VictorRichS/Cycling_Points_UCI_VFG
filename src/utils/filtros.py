import streamlit as st

def aplicar_filtros_riders(df):
    st.subheader("🔎 Filtrar ciclistas")

    equipo = st.sidebar.multiselect("Equipo", df["Team"].unique(), default=df["Team"].unique())
    tipo = st.sidebar.multiselect("Tipo (Specialty)", df["Specialty"].unique(), default=df["Specialty"].unique())
    edad = st.sidebar.slider("Edad", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))
    etapa = st.sidebar.multiselect("Etapa", df["Etapa"].unique(), default=df["Etapa"].unique())

    df2 = df[
        df["Team"].isin(equipo) &
        df["Specialty"].isin(tipo) &
        df["Age"].between(*edad) &
        df["Etapa"].isin(etapa)
    ]
    st.write(f"Registros: {len(df2)}")
    return df2

def aplicar_filtros_comparaciones(df):
    st.subheader("🔎 Filtrar comparaciones")

    vuelta = st.sidebar.multiselect("Carrera", df["Carrera"].unique(), default=df["Carrera"].unique())
    equipo = st.sidebar.multiselect("Team", df["Team"].unique(), default=df["Team"].unique())

    df2 = df[
        df["Carrera"].isin(vuelta) &
        df["Team"].isin(equipo)
    ]
    st.write(f"Registros: {len(df2)}")
    return df2