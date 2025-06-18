import pandas as pd
import os
import re


""" -------------------------------------------------------------------------------------------------------------------------------------------------
Funciones auxiliares para limpieza de datos

Estas funciones son utilizadas para limpiar y normalizar los datos en el DataFrame.
"""



def eliminar_filas_vacias(df, columna):
    """
    Elimina filas con valores nulos o vacíos en la columna indicada.
    """
    return df[df[columna].notnull() & (df[columna] != '')]

def remover_caracteres_no_deseados(df):
    df["Time"] = df["Time"].str.replace(',,', '', regex=False)
    df["Time"] = df["Time"].str.replace('.', ':', regex=False)
    df["Time"] = df["Time"].str.replace(',', ':', regex=False)
    df["Time"] = df["Time"].str.replace('"', '', regex=False)
    return df


def normalizar_time(df):
    """
    Normaliza la columna 'Time' según el patrón solicitado.
    """
    def ajustar_time(valor):
        if pd.isnull(valor):
            return valor
        valor = str(valor)
        if len(valor) == 4:
            if re.match(r'^\d:\d{2}$', valor):
                return "0:0" + valor
            elif re.match(r'^\d{2}:\d$', valor):
                return "0:" + valor
        return valor

    df["Time"] = df["Time"].apply(ajustar_time)
    return df

def evaluar_operaciones_uci(df):
    """
    Si 'uci' contiene una operación matemática, la evalúa y pone el resultado.
    Si es un número, lo deja igual. Si está vacío o nulo, pone 0.
    """
    def eval_uci(valor):
        if pd.isnull(valor) or valor == '':
            return 0
        valor_str = str(valor).replace(' ', '')
        # Solo permite números y + - * /
        if re.match(r'^[\d\+\-\.]+$', valor_str):
            try:
                return eval(valor_str)
            except Exception:
                return valor
        return valor
    df["UCI"] = df["UCI"].replace('', 0)
    df["UCI"] = df["UCI"].fillna(0)
    df["UCI"] = df["UCI"].apply(eval_uci)
    return df



""" -------------------------------------------------------------------------------------------------------------------------------------------------
Script principal para procesar los datos de las etapas
- Este script carga un archivo CSV, limpia y normaliza los datos, y guarda el resultado en un nuevo archivo CSV.
- Se enfoca en las columnas relacionadas con los ciclistas, sus tiempos y posiciones.
- También maneja casos especiales como DNF, DNS, DQ, etc.
- Finalmente, guarda el DataFrame procesado en un archivo CSV.
------------------------------------------------------------------------------------------------------------------------------------------------------"""
# Ruta relativa a la carpeta donde están los CSV
csv_folder = r"C:\Users\victo\Downloads\Cycling_points_uci_VFG\data\raw"  # Cambia esto según tu estructura de carpetas
csv_folder_out = r"C:\Users\victo\Downloads\Cycling_points_uci_VFG\data\processed"  # Cambia esto según tu estructura de carpetas
csv_file = os.path.join(csv_folder, 'etapas_final.csv')

print(csv_file)

df_final = []

df_temp = pd.read_csv(csv_file, encoding='utf-8', sep=',')

df_temp = eliminar_filas_vacias(df_temp, "Rider")

df_temp.columns = df_temp.columns.str.strip()

# Limpiar Rider
df_temp["Rider"] = df_temp.apply(lambda row: row["Rider"][:row["Rider"].__len__() - row["Team"].__len__()], axis=1)

#Limpiar DFs
df_temp["Rnk"] = df_temp.apply(lambda row: row["GC"] if str(row["Rnk"]) == "DF" else row["Rnk"], axis=1)

#Eliminamos los DNF, DNS, DQ, etc. por 999
df_temp["Rnk"] = pd.to_numeric(df_temp["Rnk"], errors='coerce').fillna(999).astype(int)

#Limpiar GCs
df_temp["GC"] = df_temp.apply(lambda row: row["Rnk"] if pd.isnull(row["GC"]) or row["GC"] == "" else row["GC"], axis=1)


# Limpiar Time
df_temp = remover_caracteres_no_deseados(df_temp)
df_temp["Time"] = df_temp.apply(lambda row: row["Time"][:4] if str(row["Rnk"]) != "1" and pd.notnull(row["Time"]) else row["Time"],axis=1)

#método para normalizar el formato de la columna 'Time'
df_temp = normalizar_time(df_temp)

df_temp["Time"] = df_temp.apply(lambda row: "9:99:99" if row["Rnk"] == 999 else row["Time"],axis=1)
df_temp["Time"] = df_temp.apply(lambda row: row["Time"][:7] if str(row["Rnk"]) == "1" and pd.notnull(row["Time"]) else row["Time"],axis=1)


#Limpiamos la columna UCI
df_temp = evaluar_operaciones_uci(df_temp)

df_final.append(df_temp)

# Concatenar todos los DataFrames en uno solo
df_final = pd.concat(df_final, ignore_index=False)

#Guardar el DataFrame final en un archivo CSV
output_file = os.path.join(csv_folder_out, 'all_stages.csv')
df_final.to_csv(output_file, index=False)
print(f"Archivo final guardado en: {output_file}")


