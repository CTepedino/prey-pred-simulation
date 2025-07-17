import os

import pandas as pd
from matplotlib import pyplot as plt


def plot_populations_temporal_evolution_fixed_alpha(times, prey_population_levels, pred_population_levels, variables_label):
    results_subdir = "results/population/fixed_alpha"
    if not os.path.exists(results_subdir):
        os.makedirs(results_subdir)
    plt.figure(figsize=(20,8))

    plt.plot(times[1], prey_population_levels[1], marker="o", linestyle="dashdot", label=r"$Presas$", color="limegreen")
    plt.plot(times[1], pred_population_levels[1], marker="o", linestyle="dashdot", label=r"$Depredadores$", color="red")

    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.ylim(0, None)
    plt.legend(loc="upper right", fontsize=30)
    plt.grid(True)
    plt.xlabel("Tiempo (s)", fontsize=30)
    plt.ylabel(f"Velocidad promedio (m/s)", fontsize=30)
    plt.tight_layout()
    plt.savefig(f"{results_subdir}/vel_vs_time_N_pred_(5-35-70)_alpha_{variables_label}.png")

if __name__ == "__main__":
    sim_paths = [
        "results/100/N=35_a=0.80",    # reemplaza con el path real
        "results/100/N=35_a=1.00",
        "results/100/N=35_a=1.20"
    ]

    times = []
    prey_population_levels = []
    pred_population_levels = []

    for path in sim_paths:
        df = pd.read_csv(f"{path}/velocity_t", sep=' ')
        times.append(df['t'].values)
        prey_population_levels.append(df['prey_velocity'].values)
        pred_population_levels.append(df['pred_velocity'].values)

    # Ahora llama a tu función para graficar
    variables_label = "0.25"  # o el valor que desees colocar en el nombre del archivo
    plot_populations_temporal_evolution_fixed_alpha(times, prey_population_levels, pred_population_levels, variables_label)


