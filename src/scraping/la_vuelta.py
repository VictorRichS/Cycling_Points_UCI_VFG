import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrap_vuelta():

    BASE_URL = "https://www.procyclingstats.com"
    #RACE_BASE = "/race/vuelta-a-espana/2024/"
    RACE_BASE = "/race/vuelta-a-espana/"
    HEADERS = {"User-Agent": "Mozilla/5.0"}

    # Script para extraer resultados de la Vuelta a España 2015-2024
    anios = [f"{i}/" for i in range(2015, 2025)]  # Años de 2015 a 2024

    # Asumimos 21 etapas
    etapas = [f"stage-{i}" for i in range(1, 22)]


    all_etapas = []

    #recorrer cada año y cada etapa
    for anio in anios:
        print(f"Procesando año: {anio.strip('/')}")

        for etapa in etapas:
            url = BASE_URL + RACE_BASE + anio + etapa
            print(f"Procesando: {url}")

            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                print(f"Error al acceder a la etapa {etapa}: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"class": "results"})

            if not table:
                print(f"No se encontró tabla en {etapa}")
                continue

            headers = [th.text.strip() for th in table.find_all("th")]
            rows = []
            for tr in table.find_all("tr")[1:]:
                cols = [td.text.strip() for td in tr.find_all("td")]
                if cols:
                    rows.append(cols)

            df_etapa = pd.DataFrame(rows, columns=headers)
            df_etapa["Etapa"] = etapa
            df_etapa["Año"] = anio.strip("/")
            all_etapas.append(df_etapa)

            # Esperar para evitar bloqueo
            time.sleep(3)

    # Unir todas las etapas
    df_total = pd.concat(all_etapas, ignore_index=True)
    print(df_total)
    # Guardar como CSV
    df_total.to_csv("vuelta_espana_2015_2024_etapas.csv", index=False)
    print("✅ Archivo CSV generado: vuelta_espana_2015_2024_etapas.csv")


    # In[4]:


    anios = [f"{i}/" for i in range(2015, 2025)]
    print("Años procesados:", anios)


if __name__ == '__main__':
    scrap_vuelta()
