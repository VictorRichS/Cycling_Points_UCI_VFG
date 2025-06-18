import pandas as pd
import os

def unificar_csv_stages():
    """
    Unifica los archivos CSV de etapas de carreras ciclistas en un solo DataFrame.
    """
    pass

    # Ruta relativa a la carpeta donde están los CSV
    csv_folder = r"C:\Users\victo\Downloads\Cycling_points_uci_VFG\data\raw"  # Cambia esto según tu estructura de carpetas

    # Unir la ruta relativa con el nombre del archivo
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

    print(csv_files)

    df_final = []
    # Reunir todas las columnas posibles
    todas_las_columnas = set()
    carrera = ''
    for archivo in csv_files:
        print(f"Procesando archivo: {archivo}")
        if archivo.startswith('00_'):
                carrera = archivo
                archivo = os.path.join(csv_folder, archivo)
                df_temp = pd.read_csv(archivo)

                order_columns = ['Rnk', 'GC', 'Specialty', 'Rider', 'Team', 'Age', 'Time', 'Etapa', 'Anio', 'UCI']
                df_temp = df_temp[order_columns]

                print(f"antes de renombrar las columnas: {archivo}")
                


                #añado la columna de archivo
                if carrera.startswith('00_giro'):
                    carrera = 'Giro'
                    print("Giro")
                elif carrera.startswith('00_tour'):
                    carrera = 'Tour'
                    print("Tour")
                elif carrera.startswith('00_vuelta'):
                    carrera = 'Vuelta'
                df_temp['Carrera'] = carrera

                df_final.append(df_temp)
        continue

    # Unificar los CSV
    #
    print("Unificando archivos CSV...")

    # Concatenar todos los DataFrames en uno solo
    df_final = pd.concat(df_final, ignore_index=False)

    #Guardar el DataFrame final en un archivo CSV
    output_file = os.path.join(csv_folder, 'etapas_final.csv')
    df_final.to_csv(output_file, index=False)
    print(f"Archivo final guardado en: {output_file}")

if __name__ == '__main__':
    unificar_csv_stages()