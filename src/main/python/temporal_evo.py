import os

import pandas as pd
from matplotlib import pyplot as plt


def plot_populations_temporal_evolution_fixed_alpha(times, prey_population_levels, pred_population_levels, variables_label):
    results_subdir = "results/population/fixed_alpha"
    if not os.path.exists(results_subdir):
        os.makedirs(results_subdir)
    plt.figure(figsize=(20,8))

    plt.plot(times[0], prey_population_levels[0], marker="v", linestyle="dashed", label=r"$Presas - N_{depred} = 5$", color="cornflowerblue")
    plt.plot(times[0], pred_population_levels[0], marker="v", linestyle="dashed", label=r"$Depredadores - N_{depred} = 5$", color="royalblue")
    plt.plot(times[1], prey_population_levels[1], marker="o", linestyle="dashdot", label=r"$Presas - N_{depred} = 35$", color="limegreen")
    plt.plot(times[1], pred_population_levels[1], marker="o", linestyle="dashdot", label=r"$Depredadores - N_{depred} = 35$", color="forestgreen")
    plt.plot(times[2], prey_population_levels[2], marker="^", linestyle="solid", label=r"$Presas - N_{depred} = 70$", color="orange")
    plt.plot(times[2], pred_population_levels[2], marker="^", linestyle="solid", label=r"$Depredadores - N_{depred} = 70$", color="red")

    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.ylim(0, None)
    plt.legend(loc="upper left", fontsize=20)
    plt.grid(True)
    plt.xlabel("Tiempo (s)", fontsize=30)
    plt.ylabel(f"Población", fontsize=30)
    plt.tight_layout()
    plt.savefig(f"{results_subdir}/populations_vs_time_N_pred_(5-40-70)_alpha_{variables_label}.png")

if __name__ == "__main__":
    sim_paths = [
        "results/101/N=5",    # reemplaza con el path real
        "results/101/N=35",
        "results/101/N=70"
    ]

    times = []
    prey_population_levels = []
    pred_population_levels = []

    for path in sim_paths:
        df = pd.read_csv(f"{path}/population_t", sep=' ')
        times.append(df['t'].values)
        prey_population_levels.append(df['prey_population'].values)
        pred_population_levels.append(df['pred_population'].values)

    # Ahora llama a tu función para graficar
    variables_label = "0.25"  # o el valor que desees colocar en el nombre del archivo
    plot_populations_temporal_evolution_fixed_alpha(times, prey_population_levels, pred_population_levels, variables_label)


