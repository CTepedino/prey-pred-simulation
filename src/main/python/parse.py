import pandas as pd
import numpy as np

# get population level per species for each time step
def get_temporal_population_levels_for_both_species(simulation_filename):
    data = pd.read_csv(
        simulation_filename,
        sep=' ',
        names=['t', 'id', 'species', 'status', 'x', 'y', 'vx', 'vy', 'r']
    )

    alive_df = data[data['status'] == 'alive']

    population_counts = alive_df.groupby(['t', 'species']).size().reset_index(name='count')
    pivot = population_counts.pivot(index='t', columns='species', values='count').fillna(0)

    t_values = pivot.index.values
    prey_population_values = pivot['prey'].values
    predator_population_values = pivot['predator'].values
    return t_values, prey_population_values, predator_population_values

def get_extinction_time_for_both_species(simulation_filename):
    t_values, prey_population, predator_population = get_temporal_population_levels_for_both_species(simulation_filename)
    if (np.min(prey_population) > 0):
        raise AttributeError("the simulation hasn't reached prey's extinction")
    if (np.min(prey_population) > 0):
        raise AttributeError("the simulation hasn't reached predator's extinction")

    prey_extinction_index = np.argmin(prey_population)
    predator_extinction_index = np.argmin(predator_population)
    return t_values[prey_extinction_index], t_values[predator_extinction_index]

def get_mean_velocities_per_time_for_both_species(simulation_filename):
    data = pd.read_csv(
        simulation_filename,
        sep=' ',
        names=['t', 'id', 'species', 'status', 'x', 'y', 'vx', 'vy', 'r']
    )
    alive_df = data[data['status'] == 'alive'].copy()
    alive_df['v_mag'] = np.sqrt(alive_df['vx']**2 + alive_df['vy']**2)
    mean_velocities = (
        alive_df
        .groupby(['t', 'species'])['v_mag']
        .mean()
        .reset_index(name='mean_velocity')
    )
    pivot = mean_velocities.pivot(index='t', columns='species', values='mean_velocity').fillna(0)
    t_values = pivot.index.values
    prey_mean_velocities = pivot['prey'].values
    predator_mean_velocities = pivot['predator'].values
    std_velocities = (
        alive_df
        .groupby(['t', 'species'])['v_mag']
        .std()
        .reset_index(name='std')
    )
    pivot = std_velocities.pivot(index='t', columns='species', values='std').fillna(0)
    prey_velocities_std = pivot['prey'].values
    predator_velocities_std = pivot['predator'].values
    return t_values, prey_mean_velocities, prey_velocities_std, predator_mean_velocities, predator_velocities_std
