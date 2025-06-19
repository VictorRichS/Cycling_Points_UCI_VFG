import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import classification_report

@st.cache_data
def preparar_datos(riders, stages):
    df_riders = riders.copy()
    df_stages = stages.copy()

    # Extraer número de etapa de 'Etapa' y convertir a string
    df_riders["StageNum"] = df_riders["Etapa"].str.extract(r"(\d+)", expand=False).astype(str)

    # Convertir también la columna 'Stage' a string
    df_stages["Stage"] = df_stages["Stage"].astype(str)

    # Fusionar por etapa, año y carrera
    df_merged = df_riders.merge(
        df_stages,
        left_on=["StageNum", "Anio", "Carrera"],
        right_on=["Stage", "Año", "Carrera"],
        how="left"
    )

    # Convertir tiempo a segundos
    df_merged["Time_sec"] = df_merged["Time"].apply(
        lambda x: sum(int(t) * 60 ** i for i, t in enumerate(reversed(x.split(':'))))
    )

    # Eliminar columnas irrelevantes
    df_merged = df_merged.drop(
        columns=["Rnk", "Rider", "Time", "Stage", "Año", "Date", "Route", "Image", "StageNum", "Etapa"]
    )

    # Codificar variables categóricas
    df_merged = pd.get_dummies(df_merged, columns=["Specialty", "Team", "Carrera"], drop_first=True)

    # Eliminar nulos
    df_merged = df_merged.dropna()

    return df_merged



def entrenar_modelo(riders, stages):
    st.subheader("🚴‍♂️ Entrenar modelo de tiempo con perfil de etapa")
    df = preparar_datos(riders, stages)
    target = "Time_sec"
    X = df.drop(columns=[target])
    y = df[target]


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    score = modelo.score(X_test, y_test)
    st.write(f"R² en test: {score:.2f}")

    # Guardar modelo y columnas
    pickle.dump((modelo, X.columns.tolist()), open("modelo.pkl", "wb"))
    return modelo, X.columns.tolist()


def hacer_prediccion(modelo_cols, cols=None):
    if modelo_cols is None:
        modelo, cols = pickle.load(open("modelo.pkl", "rb"))
    else:
        modelo, cols = modelo_cols
    st.subheader("Predicción de tiempo (segundos)")
    entrada = {}
    for c in cols:
        entrada[c] = st.number_input(c, value=0.0)
    if st.button("Predecir"):
        df_in = pd.DataFrame([entrada])
        pred = modelo.predict(df_in)[0]
        st.success(f"Tiempo estimado: {int(pred//60)}m {int(pred%60)}s")

def entrenar_modelo_clasificacion(riders, stages):
    st.subheader("🏁 Clasificación: ¿Terminará en el Top 10?")
    df = preparar_datos(riders, stages)
    df["Top10"] = df["Rnk"] <= 10

    X = df.drop(columns=["Time_sec", "Top10", "Rnk"])
    y = df["Top10"]
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    st.write("🔍 Clasification report:")
    y_pred = modelo.predict(X_test)
    st.text(classification_report(y_test, y_pred))

    # Guardar modelo
    pickle.dump((modelo, X.columns.tolist()), open("modelo_clasificacion.pkl", "wb"))

    return modelo, X.columns.tolist()

