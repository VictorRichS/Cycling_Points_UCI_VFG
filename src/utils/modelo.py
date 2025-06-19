import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from io import BytesIO

def cargar_modelo():
    uploaded_file = st.file_uploader(
        "Sube un archivo CSV con datos UCI (Rider, Team, Carrera, stage, UCI_points, Specialty)",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Filtros
        col1, col2 = st.columns(2)
        carreras = col1.multiselect("Selecciona la(s) carrera(s)", df["Carrera"].unique(), default=df["Carrera"].unique())
        equipos = col2.multiselect("Filtrar por equipo(s)", df["Team"].unique(), default=df["Team"].unique())

        df_filtered = df[(df["Carrera"].isin(carreras)) & (df["Team"].isin(equipos))]

        entrenar_modelo(df_filtered)
    else:
        st.info("Por favor, sube un archivo CSV para comenzar.")

def entrenar_modelo(df):
    st.subheader("Predicción de puntos por etapa")
    st.markdown("Este modelo usa Random Forest para predecir los puntos en futuras etapas basado en la información disponible.")

    df_model = df.copy()
    df_model = pd.get_dummies(df_model, columns=["Carrera", "Team", "Specialty"], drop_first=True)

    if "UCI_points" in df_model.columns and "stage" in df_model.columns:
        X = df_model.drop(columns=["Rider", "UCI_points"])
        y = df_model["UCI_points"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        st.write(f"Error cuadrático medio del modelo: {mse:.2f}")

        st.markdown("### Estimar puntos para una etapa personalizada")

        etapa = st.number_input("Número de etapa", min_value=1, step=1)
        vuelta_sel = st.selectbox("Carrera", df["Carrera"].unique())
        equipo_sel = st.selectbox("Team", df["Team"].unique())
        tipo_rol_sel = st.selectbox("Tipo de rol", df["Specialty"].unique())
        ciclista_sel = st.selectbox("Selecciona un ciclista", df["Rider"].unique())

        input_dict = {col: 0 for col in X.columns}
        input_dict["stage"] = etapa

        for col in X.columns:
            if vuelta_sel in col:
                input_dict[col] = 1
            if equipo_sel in col:
                input_dict[col] = 1
            if tipo_rol_sel in col:
                input_dict[col] = 1

        input_df = pd.DataFrame([input_dict])
        pred_puntos = model.predict(input_df)[0]

        st.success(f"{ciclista_sel} obtendría aproximadamente {pred_puntos:.2f} puntos en esta etapa")

        # Ranking estimado
        st.markdown("### Ranking estimado de puntos en esta etapa")
        ranking_data = []
        for corredor in df["Rider"].unique():
            corredor_input = input_dict.copy()
            puntos_est = model.predict(pd.DataFrame([corredor_input]))[0]
            ranking_data.append({"Rider": corredor, "puntos_estimados": puntos_est})

        ranking_df = pd.DataFrame(ranking_data).sort_values(by="puntos_estimados", ascending=False).reset_index(drop=True)

        def format_row(row):
            if row["Rider"] == ciclista_sel:
                return f"**:green[{row['Rider']}]**"
            return row["Rider"]

        ranking_df["Rider"] = ranking_df.apply(format_row, axis=1)

        st.dataframe(ranking_df[["Rider", "puntos_estimados"]])

        # Exportar a Excel
        st.markdown("### Exportar ranking a Excel")
        excel_df = pd.DataFrame(ranking_data).sort_values(by="puntos_estimados", ascending=False)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            excel_df.to_excel(writer, index=False, sheet_name='Ranking')
        st.download_button(
            label="📥 Descargar Excel",
            data=output.getvalue(),
            file_name="ranking_estimado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )