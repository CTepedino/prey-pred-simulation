import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re

def plot_extinction_time_vs_N(base_dir):
    data_records = []

    folders = glob.glob(os.path.join(base_dir, "N=*"))

    def extract_N(folder_path):
        match = re.search(r'N=(\d+)', os.path.basename(folder_path))
        return int(match.group(1)) if match else None

    for folder in folders:
        N = extract_N(folder)
        if N is None:
            continue

        ext_file = os.path.join(folder, "ext")
        if not os.path.exists(ext_file):
            continue

        df = pd.read_csv(ext_file, sep=' ')
        prey_row = df[df['species'] == 'PREY'].iloc[0]
        pred_row = df[df['species'] == 'PRED'].iloc[0]

        record = {
            'N': N,
            'PREY_mean': float(prey_row['mean']),
            'PREY_std': float(prey_row['std']),
            'PRED_mean': float(pred_row['mean']),
            'PRED_std': float(pred_row['std'])
        }
        data_records.append(record)

    # Crear DataFrame y ordenar por N
    data_df = pd.DataFrame(data_records).sort_values(by='N')

    # Plot
    plt.figure(figsize=(10, 6))

    # PREY
    prey_df = data_df.dropna(subset=['PREY_mean'])
    if not prey_df.empty:
        plt.errorbar(
            prey_df['N'],
            prey_df['PREY_mean'],
            yerr=prey_df['PREY_std'],
            fmt='o-',
            color='green',
            ecolor='gray', elinewidth=1, capsize=3,
            label='Presas'
        )

    # PRED
    pred_df = data_df.dropna(subset=['PRED_mean'])
    if not pred_df.empty:
        plt.errorbar(
            pred_df['N'],
            pred_df['PRED_mean'],
            yerr=pred_df['PRED_std'],
            fmt='s-',
            color='red',
            ecolor='gray', elinewidth=1, capsize=3,
            label='Depredadores'
        )

    plt.xlabel(r"$N_{depredadores}$", fontsize=20)
    plt.ylabel("Tiempo de extinción promedio", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True)
    plt.legend(fontsize=20)
    plt.tight_layout()

    results_dir = os.path.join(base_dir, "results_extinction_vs_N")
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, "extinction_vs_N.png")
    plt.savefig(output_path)

    print(f"Gráfico guardado en: {output_path}")

# Ejemplo de uso:
plot_extinction_time_vs_N("results")
