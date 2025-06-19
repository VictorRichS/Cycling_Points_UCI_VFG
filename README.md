# 🚴‍♂️ Cycling Points UCI - VFG

Este proyecto tiene como objetivo clasificar ciclistas que han participado en las tres grandes vueltas (Giro d'Italia, Tour de France y Vuelta a España) durante los últimos 10 años.
El análisis se centra en su rendimiento en distintos perfiles de etapa y en su evolución interna comparada con otros ciclistas.

classify the cyclists who have participated in the 3 grand tours over the last 10 years in order to see their performance in the different stage profiles as well as analyze their own internal performance compared to others.

## 📊 Funcionalidades

- Visualización de datos de etapas y perfiles (kms, metros verticales, perfil)
- Clasificación de ciclistas según características de etapa
- Análisis comparativo entre ciclistas
- Entrenamiento de modelos de ML para predicción de rendimiento

## 🏗️ Estructura del proyecto

```
Cycling_points_uci_VFG/
├── src/
│   ├── app/             # Aplicación principal con Streamlit
│   └── utils/           # Funciones auxiliares y lógica de modelo
│   └── modeling/        # Funciones de modelo y fusión de los datos
│   └── scraping/        # Funciones de scraping para la obtención de los datos
├── data/                # Datos crudos y preprocesados
├── notebooks/           # Funciones utilizadas para scraping y modeling
├── docs/                # Imagen del proyecto
├── README.md
├── requirements.txt
```

## 🚀 Instrucciones de uso

1. Clonar el repositorio:
```bash
git clone https://github.com/tu_usuario/Cycling_points_uci_VFG.git
cd Cycling_points_uci_VFG
```

2. Crear entorno y activar:
```bash
conda create -n Cycling_env python=3.10
conda activate Cycling_env
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar la app:
```bash
streamlit run src/app/app.py
```

## 📦 Requisitos

Python 3.10+  
Streamlit, pandas, scikit-learn, matplotlib, seaborn, requests, BeautifulSoup4

## 📄 Licencia

MIT License - libre para uso académico o personal.
