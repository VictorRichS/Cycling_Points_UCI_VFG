import pandas as pd
import os

# Ruta relativa a la carpeta donde están los CSV
csv_folder = r"C:\Users\victo\Downloads\Cycling_points_uci_VFG\data\raw"  # Cambia esto según tu estructura de carpetas
csv_folder_out = r"C:\Users\victo\Downloads\Cycling_points_uci_VFG\data\processed"  # Cambia esto según tu estructura de carpetas
csv_file = os.path.join(csv_folder, 'perfiles_etapas_all.csv')

print(csv_file)

df_final = []

df_temp = pd.read_csv(csv_file, encoding='utf-8', sep=',')


df_temp.columns = df_temp.columns.str.strip()

# Limpiar "Vertical_meters"
df_temp["Vertical_meters"] = df_temp["Vertical_meters"].str.extract(r'(\d+)', expand=False)

# Limpiar "ProfileScore"
df_temp["ProfileScore"] = df_temp["ProfileScore"].str.extract(r'(\d+)', expand=False)

# Limpiar "PS final 25k"
df_temp["PS_final_25k"] = df_temp["PS_final_25k"].str.replace('PS final 25k', '', regex=False)

# Opcional: limpiar "Date" o "Stage" si tienen prefijos no deseados
df_temp["Date"] = df_temp["Date"].str.replace("Date", "", regex=False)
df_temp["Stage"] = df_temp["Stage"].str.replace("Stage", "", regex=False)

# Extraer los kms  entre paréntesis en la columna 'route'
kms = df_temp['Route'].str.extract(r'\((.*?)\)')

kms = kms[0].str.replace('km', '', regex=False).astype(float)
# Añadir la columna 'kms' al DataFrame
df_temp['kms'] = kms


df_final.append(df_temp)

# Concatenar todos los DataFrames en uno solo
df_final = pd.concat(df_final, ignore_index=False)

#Guardar el DataFrame final en un archivo CSV
output_file = os.path.join(csv_folder_out, 'profiles_all_stages.csv')
df_final.to_csv(output_file, index=False)
print(f"Archivo final guardado en: {output_file}")