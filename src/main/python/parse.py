import pandas as pd
import numpy as np

def read_simulation_output_as_df(simulation_filename):
    return pd.read_csv(
        simulation_filename,
        sep=' ',
        names=['t', 'id', 'species', 'status', 'x', 'y', 'vx', 'vy', 'r']
    ) 

# get population level per species for each time step
def get_temporal_population_levels_for_both_species(simulation_filename):
    data = read_simulation_output_as_df(simulation_filename)

    # adding t where last individual dies 
    max_t = data.iloc[-1, 0]
    alive_df = data[data['status'] == 'alive']

    population_counts = alive_df.groupby(['t', 'species']).size().reset_index(name='count')
    pivot = population_counts.pivot(index='t', columns='species', values='count').fillna(0)

    t_values = pivot.index.values
    prey_population_values = pivot['prey'].values
    predator_population_values = pivot['predator'].values

    # check the simulation reaches extinction to add these lines
    #t_values = np.append(t_values, max_t)
    #prey_population_values = np.append(prey_population_values, 0.0)
    #predator_population_values = np.append(predator_population_values, 0.0)
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
    data = read_simulation_output_as_df(simulation_filename)
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

def get_mean_life_duration_for_both_species(simulation_filename):
    data = read_simulation_output_as_df(simulation_filename)
    initial_id = 1
    max_id = np.max(data['id'].values)
    prey_life_durations = []
    pred_life_durations = []
    #iterate through id's check if they die during simulation update
    for id in range(initial_id, max_id):
        filtered_by_id = data[data['id'] == id]
        if (filtered_by_id.iloc[-1,3] == 'alive'):
            continue
        birth_time = filtered_by_id.iloc[0,0]
        death_time = filtered_by_id.iloc[-1,0]
        life_time = death_time - birth_time

        species = filtered_by_id.iloc[0,2]
        if (species == 'prey'):
            prey_life_durations.append(life_time)
        else:
            pred_life_durations.append(life_time)

    prey_mean_life_duration = np.mean(prey_life_durations)
    prey_std_life_duration = np.std(prey_life_durations)

    pred_mean_life_duration = np.mean(pred_life_durations)
    pred_std_life_duration = np.std(pred_life_durations)

    return prey_mean_life_duration, prey_std_life_duration, pred_mean_life_duration, pred_std_life_duration
