import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrap_etapas_completas():

    # Parámetros de navegación
    header_url = "https://www.procyclingstats.com/race/"
    end_url = "/route/stage-profiles"
    headers = {"User-Agent": "Mozilla/5.0"}

    anios = [str(i) for i in range(2015, 2025)]
    nroads = {
        "giro-d-italia": "Giro",
        "tour-de-france": "Tour",
        "vuelta-a-espana": "Vuelta"
    }

    todas_etapas = []

    # Recorrer todas las carreras y años
    for nroad_key, carrera_nombre in nroads.items():
        for anio in anios:
            print(f"🔍 Procesando {carrera_nombre} {anio}...")
            url = f"{header_url}{nroad_key}/{anio}{end_url}"
            print(f"URL: {url}")
            
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"⚠️ No se pudo acceder a {url} (Código: {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            stages = soup.find_all("li", class_="mt50")
            
            if not stages:
                print(f"⚠️ No se encontraron etapas en {url}")
                continue

            data = []
            for stage in stages:
                try:
                    date = stage.find("div", {"data-pid": "52079"}).text.strip()
                    stage_info = stage.find("div", {"data-pid": "52075"}).text.strip()
                    vertical_meters = stage.find("div", {"data-pid": "52084"}).text.strip()
                    profile_score = stage.find("div", {"data-pid": "52085"}).text.strip()
                    ps_final_25k = stage.find("div", {"data-pid": "64891"}).text.strip()
                    image_url = stage.find("img")["src"]

                    # Separar nombre y distancia
                    if "|" in stage_info:
                        stage_name = stage_info.split("|")[0].strip()
                        route = stage_info.split("|")[1].strip()
                    else:
                        stage_name = stage_info
                        route = ""

                    data.append({
                        "Carrera": carrera_nombre,
                        "Año": anio,
                        "Date": date,
                        "Stage": stage_name,
                        "Route": route,
                        "Vertical meters": vertical_meters,
                        "ProfileScore": profile_score,
                        "PS final 25k": ps_final_25k,
                        "Image": image_url
                    })
                except Exception as e:
                    print(f"⚠️ Error procesando etapa: {e}")

            df = pd.DataFrame(data)

            # Convertir fecha al formato datetime
            try:
                df["Date"] = pd.to_datetime(df["Date"] + f"/{anio}", format="%d/%m/%Y")
            except Exception as e:
                print(f"⚠️ Error convirtiendo fecha en {carrera_nombre} {anio}: {e}")

            todas_etapas.append(df)

    # Concatenar todas las etapas en un único DataFrame
    if todas_etapas:
        df_final = pd.concat(todas_etapas, ignore_index=True)
        df_final.to_csv("todas_las_etapas.csv", index=False, encoding='utf-8-sig')
        print("✅ Archivo guardado como: todas_las_etapas.csv")
    else:
        print("⚠️ No se extrajo ningún dato.")
if __name__ == '__main__':
    scrap_etapas_completas()