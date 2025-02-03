import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from PIL import Image

# 📌 Configuración de la App
st.set_page_config(page_title="Predicción Energética", layout="wide")

# 📌 Título de la App
st.title("🔋 Predicción del Consumo Energético en Europa (2022-2030)")

# 📂 Directorios de archivos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Raíz del proyecto
DATA_DIR = os.path.join(BASE_DIR, "data", "predicciones")  # 📁 Carpeta de predicciones
IMG_DIR = os.path.join(BASE_DIR, "results")  # 📁 Carpeta de imágenes

# 📁 Obtener todos los archivos CSV disponibles
csv_files = [f for f in os.listdir(DATA_DIR) if f.startswith("predicciones_") and f.endswith(".csv")]

# 📌 Extraer nombres de los países de los archivos CSV
country_names = {f.replace("predicciones_", "").replace("_2030.csv", ""): f for f in csv_files}

# 📌 Selección de país
selected_country = st.selectbox("🌍 Selecciona un país:", list(country_names.keys()))

if selected_country:
    # 📌 Cargar datos del país seleccionado
    file_path = os.path.join(DATA_DIR, country_names[selected_country])
    df = pd.read_csv(file_path)
    df['ds'] = pd.to_datetime(df['ds'])

    # 📊 Visualización de los datos
    st.subheader(f"📈 Predicción para {selected_country}")

    # 📌 Verificar si existe el gráfico para el país seleccionado
    img_filename = f"grafico_prediccion_{selected_country}.png"
    img_path = os.path.join(IMG_DIR, img_filename)

    if os.path.exists(img_path):
        # 📌 Mostrar la imagen del gráfico guardado
        image = Image.open(img_path)
        st.image(image, caption=f"Predicción de consumo energético en {selected_country}", use_column_width=True)
    else:
        # 📊 Si no existe el gráfico, generar la gráfica en tiempo real
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(df['ds'], df['prediction'], label="Predicción (2022-2030)", color="red", linestyle="dashed")
        ax.set_title(f"Consumo Energético en {selected_country} (2022-2030)")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Consumo Energético (GWh)")
        ax.legend()
        ax.grid()
        st.pyplot(fig)

    # 📥 Botón para descargar los datos
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar Predicción en CSV",
        data=csv,
        file_name=f"Prediccion_{selected_country}.csv",
        mime="text/csv"
    )

st.sidebar.info("📌 Selecciona un país en el menú para ver su predicción de consumo energético.")
