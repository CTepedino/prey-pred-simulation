import glob
import sys

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def read_simulation_output_as_df(simulation_filename):
    return pd.read_csv(
        simulation_filename,
        sep=' ',
        names=['t', 'id', 'species', 'x', 'y', 'vx', 'vy', 'r', 'lifetime', 'reproduction_time', 'hunger_time', 'status']
    )


def get_temporal_population_levels_for_both_species(data):

    # adding t where last individual dies
    max_t = data.iloc[-1, 0]
    alive_df = data[data['status'] == 'ALIVE']

    population_counts = alive_df.groupby(['t', 'species']).size().reset_index(name='count')
    pivot = population_counts.pivot(index='t', columns='species', values='count').fillna(0)

    t_values = pivot.index.values
    prey_population_values = pivot['PREY'].values
    predator_population_values = pivot['PRED'].values

    return t_values, prey_population_values, predator_population_values

def get_extinction_times(t, prey_pop, pred_pop):
    extinction_times = {}

    # Buscar primer t donde la población es 0
    prey_zero = (prey_pop == 0)
    pred_zero = (pred_pop == 0)

    extinction_times['PREY'] = t[prey_zero][0] if prey_zero.any() else None
    extinction_times['PRED'] = t[pred_zero][0] if pred_zero.any() else None

    return extinction_times


def save_population_to_file(t, prey, pred, output_path):
    df = pd.DataFrame({
        't': t,
        'prey_population': prey,
        'pred_population': pred
    })
    df.to_csv(output_path, sep=' ', index=False)

def get_avg_lifetime_until_first_extinction(df):
    # Obtener poblaciones y extinción
    t, prey, pred = get_temporal_population_levels_for_both_species(df)
    ext = get_extinction_times(t, prey, pred)

    # Tiempo mínimo de extinción válido
    ext_times = [v for v in ext.values() if v is not None]
    t_cutoff = min(ext_times) if ext_times else np.inf

    # Para cada individuo, obtener tiempo de muerte (t_death)
    grouped = df.groupby('id').agg({
        't': ['min', 'max'],
        'species': 'first'
    })
    grouped.columns = ['t_birth', 't_death', 'species']

    # Filtrar individuos que mueren antes o en t_cutoff
    filtered = grouped[grouped['t_death'] <= t_cutoff]

    # Calcular tiempo de vida
    filtered = filtered.assign(life_time=filtered['t_death'] - filtered['t_birth'])

    # Estadísticas por especie
    stats = filtered.groupby('species')['life_time'].agg(['mean', 'std'])

    result = {
        'PREY': (stats.loc['PREY', 'mean'], stats.loc['PREY', 'std']) if 'PREY' in stats.index else (np.nan, np.nan),
        'PRED': (stats.loc['PRED', 'mean'], stats.loc['PRED', 'std']) if 'PRED' in stats.index else (np.nan, np.nan)
    }

    return result


def get_avg_velocity_over_time(df):
    # Calcular magnitud de la velocidad
    df = df.copy()
    df['speed'] = np.sqrt(df['vx']**2 + df['vy']**2)

    # Solo ALIVE
    alive_df = df[df['status'] == 'ALIVE']

    # Agrupar por tiempo y especie, promediar velocidades
    grouped = alive_df.groupby(['t', 'species'])['speed'].mean().reset_index()
    pivot = grouped.pivot(index='t', columns='species', values='speed').fillna(0)

    t_values = pivot.index.values
    prey_velocity = pivot['PREY'].values if 'PREY' in pivot.columns else np.zeros_like(t_values)
    pred_velocity = pivot['PRED'].values if 'PRED' in pivot.columns else np.zeros_like(t_values)

    return t_values, prey_velocity, pred_velocity



if __name__ == "__main__":

    dir_path = sys.argv[1]

    data = read_simulation_output_as_df(f"{dir_path}/0")

    t, prey, pred = get_temporal_population_levels_for_both_species(data)

    save_population_to_file(t, prey, pred, f"{dir_path}/population_t")

    # Recolectar extinciones
    extinctions = {'PREY': [], 'PRED': []}

    for i in range(5):
        data = read_simulation_output_as_df(f"{dir_path}/{i}")
        t, prey, pred = get_temporal_population_levels_for_both_species(data)
        result = get_extinction_times(t, prey, pred)

        for species in ['PREY', 'PRED']:
            valor = result[species]
            if valor is None:
                valor = np.nan
            extinctions[species].append(valor)

    # Calcular media y std ignorando NaN (si alguna especie no se extinguió en una corrida)
    summary = {
        species: (np.nanmean(times), np.nanstd(times))
        for species, times in extinctions.items()
    }

    # Guardar a archivo
    with open(f"{dir_path}/ext", "w") as f:
        f.write("species mean std\n")
        for species, (mean, std) in summary.items():
            f.write(f"{species} {mean:.2f} {std:.2f}\n")


    all_lifetimes = {'PREY': [], 'PRED': []}

    for i in range(5):
        df = read_simulation_output_as_df(f"{dir_path}/{i}")

        mean_std = get_avg_lifetime_until_first_extinction(df)

        for species in ['PREY', 'PRED']:
            mean, std = mean_std[species]
            all_lifetimes[species].append(mean)

    # Ahora calcular media y std de los promedios entre corridas
    summary = {
        species: (np.nanmean(times), np.nanstd(times))
        for species, times in all_lifetimes.items()
    }

    with open(f"{dir_path}/avg_life_t", "w") as f:
        f.write("species mean std\n")
        for species, (mean, std) in summary.items():
            f.write(f"{species} {mean:.2f} {std:.2f}\n")

# ----------- Average velocities over time -----------------
t, prey_v, pred_v = get_avg_velocity_over_time(data)

df_vel = pd.DataFrame({
    't': t,
    'prey_velocity': prey_v,
    'pred_velocity': pred_v
})
df_vel.to_csv(f"{dir_path}/velocity_t", sep=' ', index=False)

# ----------- Average velocities overall -----------------
data_alive = data[data['status'] == 'ALIVE'].copy()
data_alive['speed'] = np.sqrt(data_alive['vx']**2 + data_alive['vy']**2)

# Calcular media y std de velocidades por especie
vel_stats = data_alive.groupby('species')['speed'].agg(['mean', 'std'])

with open(f"{dir_path}/velocity_avg", "w") as f:
    f.write("species mean std\n")
    for species in ['PREY', 'PRED']:
        if species in vel_stats.index:
            mean_v = vel_stats.loc[species, 'mean']
            std_v = vel_stats.loc[species, 'std']
        else:
            mean_v = np.nan
            std_v = np.nan
        f.write(f"{species} {mean_v:.4f} {std_v:.4f}\n")