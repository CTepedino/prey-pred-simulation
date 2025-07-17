import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re

def plot_extinction_time_vs_alpha(base_dir):
    data_records = []

    folders = glob.glob(os.path.join(base_dir, "N=*"))

    def extract_alpha(folder_path):
        match = re.search(r'a=([0-9]*\.?[0-9]+)', os.path.basename(folder_path))
        return float(match.group(1)) if match else None

    for folder in folders:
        alpha = extract_alpha(folder)
        if alpha is None:
            continue

        ext_file = os.path.join(folder, "avg_life_t")
        if not os.path.exists(ext_file):
            continue

        df = pd.read_csv(ext_file, sep=' ')
        prey_row = df[df['species'] == 'PREY'].iloc[0]
        pred_row = df[df['species'] == 'PRED'].iloc[0]

        record = {
            'alpha': alpha,
            'PREY_mean': float(prey_row['mean']),
            'PREY_std': float(prey_row['std']),
            'PRED_mean': float(pred_row['mean']),
            'PRED_std': float(pred_row['std'])
        }
        data_records.append(record)

    if not data_records:
        print("No se encontraron datos válidos para graficar.")
        return

    # Crear DataFrame y ordenar por alpha
    data_df = pd.DataFrame(data_records).sort_values(by='alpha')

    # Plot
    plt.figure(figsize=(10, 6))

    # PREY
    prey_df = data_df.dropna(subset=['PREY_mean'])
    if not prey_df.empty:
        plt.errorbar(
            prey_df['alpha'],
            prey_df['PREY_mean'],
            yerr=prey_df['PREY_std'],
            fmt='o-',
            color='green',
            ecolor='green', elinewidth=1, capsize=3,
            label='Presas'
        )

    # PRED
    pred_df = data_df.dropna(subset=['PRED_mean'])
    if not pred_df.empty:
        plt.errorbar(
            pred_df['alpha'],
            pred_df['PRED_mean'],
            yerr=pred_df['PRED_std'],
            fmt='s-',
            color='red',
            ecolor='red', elinewidth=1, capsize=3,
            label='Depredadores'
        )

    plt.xlabel(r"$\alpha$", fontsize=20)
    plt.ylabel("Tiempo de vida promedio (s)", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True)
    plt.legend(fontsize=20)
    plt.tight_layout()

    results_dir = os.path.join(base_dir, "results_avg_life_time_vs_alpha")
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, "avg_life_time_vs_alpha.png")
    plt.savefig(output_path, dpi=300)

    print(f"Gráfico guardado en: {output_path}")

# Ejemplo de uso:
plot_extinction_time_vs_alpha("results")
