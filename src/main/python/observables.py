import matplotlib.pyplot as plt
import numpy as np
import os

from parse import get_temporal_population_levels_for_both_species, get_extinction_time_for_both_species, get_mean_velocities_per_time_for_both_species, get_mean_life_duration_for_both_species 

def plot_population_temporal_evolution(times, population_levels, species_label, variables_label):
    results_subdir = "results/population"
    if not os.path.exists(results_subdir):
        os.makedirs(results_subdir)
    plt.figure(figsize=(10,8))
    plt.plot(times, population_levels, marker="o")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True)
    plt.xlabel("Tiempo (s)", fontsize=20)
    plt.ylabel(f"Población de {species_label}", fontsize=20)
    plt.tight_layout()
    plt.savefig(f"{results_subdir}/{species_label}_population_vs_time_{variables_label}.png")

def plot_extinction_time_vs_variable(x_variable_values, extinction_times, species_label, x_variable_label, variables_label):
    results_subdir = "results/extinction_time"
    if not os.path.exists(results_subdir):
        os.makedirs(results_subdir)
    plt.figure(figsize=(10,8))
    plt.plot(x_variable_values, extinction_times, marker="o")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True)
    plt.xlabel(x_variable_label.capitalize(), fontsize=20)
    plt.ylabel(f"Tiempo de extinción para {species_label} (s)", fontsize=20)
    plt.tight_layout()
    plt.savefig(f"{results_subdir}/{species_label}_extinction_time_vs_{x_variable_label}_{variables_label}.png")

def plot_mean_velocities_vs_variable(x_variable_values, mean_velocities, std_errors, species_label, x_variable_label, variables_label):
    results_subdir = "results/mean_velocities"
    if not os.path.exists(results_subdir):
        os.makedirs(results_subdir)
    plt.figure(figsize=(10,8))
    plt.errorbar(x_variable_values, mean_velocities, yerr=std_errors, fmt='o-', capsize=5, ecolor="black")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True)
    plt.xlabel(x_variable_label.capitalize(), fontsize=20)
    plt.ylabel(f"Velocidad media para {species_label} (m/s)", fontsize=20)
    plt.tight_layout()
    plt.savefig(f"{results_subdir}/{species_label}_mean_velocities_vs_{x_variable_label}_{variables_label}.png") 

def plot_mean_life_duration_vs_variable(x_variable_values, mean_life_durations, std_errors, species_label, x_variable_label, variables_label):
    results_subdir = "results/mean_life"
    if not os.path.exists(results_subdir):
        os.makedirs(results_subdir)
    plt.figure(figsize=(10,8))
    plt.errorbar(x_variable_values, mean_life_durations, yerr=std_errors, fmt='o-', capsize=5, ecolor="black")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True)
    plt.xlabel(x_variable_label.capitalize(), fontsize=20)
    plt.ylabel(f"Tiempo medio de vida para {species_label} (s)", fontsize=20)
    plt.tight_layout()
    plt.savefig(f"{results_subdir}/{species_label}_mean_life_duration_vs_{x_variable_label}_{variables_label}.png") 

if __name__ == '__main__':
    basic_output_filename = "simulation"
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    # observables
    # output filename: "simulation_N_pred_2_alpha_1.2_iteration_1.txt"

    # Evoluciones temporales de las poblaciones de cada especie
    # variables: alpha and N_predators
    iteration = 1
    alpha_values = [0.8, 0.9, 1.0, 1.1, 1.2]
    #alpha_values = [1.2]
    N_predators = [5, 10, 20, 30, 40, 50, 60, 70]
    #N_predators = [2, 3]

    for N_pred in N_predators:
        for alpha in alpha_values:
            variables_label = f"N_pred_{N_pred}_alpha_{alpha}_iteration_{iteration}"
            output_filename = f"{basic_output_filename}_{variables_label}.txt"
            times, prey_population, predator_population = get_temporal_population_levels_for_both_species(output_filename)
            plot_population_temporal_evolution(times, prey_population, "presas", variables_label)
            plot_population_temporal_evolution(times, predator_population, "depredadores", variables_label)

    # Tiempo de extinción para cada especie
    iteration = 1
    # extinction_time vs alpha -> check N_pred 
    fixed_N_pred = 20
    #fixed_N_pred = 2
    prey_extinction_times = []
    predator_extinction_times = []
    for alpha in alpha_values:
        variables_label = f"N_pred_{N_pred}_alpha_{alpha}_iteration_{iteration}"
        output_filename = f"{basic_output_filename}_{variables_label}.txt" 
        prey_extinction_time, predator_extinction_time = get_extinction_time_for_both_species(output_filename)
        prey_extinction_times.append(prey_extinction_time)
        predator_extinction_times.append(predator_extinction_time)
    
    plot_extinction_time_vs_variable(alpha_values, predator_extinction_times, "depredadores", "alpha", f"N_pred_{fixed_N_pred}")
    plot_extinction_time_vs_variable(alpha_values, prey_extinction_times, "presas", "alpha",f"N_pred_{fixed_N_pred}")

    # extinction_time vs N_pred -> check alpha
    fixed_alpha = 0.9
    #fixed_alpha = 1.2
    prey_extinction_times = []
    predator_extinction_times = []
    for N_pred in N_predators:
        variables_label = f"N_pred_{N_pred}_alpha_{fixed_alpha}_iteration_{iteration}"
        output_filename = f"{basic_output_filename}_{variables_label}.txt" 
        prey_extinction_time, predator_extinction_time = get_extinction_time_for_both_species(output_filename)
        prey_extinction_times.append(prey_extinction_time)
        predator_extinction_times.append(predator_extinction_time)
         
    plot_extinction_time_vs_variable(N_predators, prey_extinction_times, "presas", "Población inicial de depredadores", f"N_pred_{fixed_N_pred}")
    plot_extinction_time_vs_variable(N_predators, predator_extinction_times, "depredadores", "Población inicial de depredadores", f"N_pred_{fixed_N_pred}")

    # Promedio de velocidades por especie (en un momento de tiempo y en promedio de la simulación)
    # check alpha to make better comparisons
    fixed_alpha = 0.9
    #fixed_alpha = 1.2
    iterations = 10
    #iterations = 2

    # mean_velocity vs N_pred
    prey_mean_velocities_variable = []
    predator_mean_velocities_variable = []
    prey_velocities_std_variable = []
    predator_velocities_std_variable = [] 

    for N_pred in N_predators:
        prey_mean_velocities_iterations = []
        predator_mean_velocities_iterations = []
        prey_velocities_std_iterations = []
        predator_velocities_std_iterations = [] 
        for iteration in range(1, iterations):
            variables_label = f"N_pred_{N_pred}_alpha_{fixed_alpha}_iteration_{iteration}"
            output_filename = f"{basic_output_filename}_{variables_label}.txt" 
            t_values, prey_mean_velocities_arr, prey_velocities_std_arr, predator_mean_velocities_arr, predator_velocities_std_arr = get_mean_velocities_per_time_for_both_species(output_filename)
            prey_mean_velocities_iterations.append(prey_mean_velocities_arr)
            prey_velocities_std_iterations.append(prey_velocities_std_arr)
            predator_mean_velocities_iterations.append(predator_mean_velocities_arr)
            predator_velocities_std_iterations.append(predator_velocities_std_arr)
        
        # mean_velocity (across iterations) vs time

        prey_velocities = np.vstack(prey_mean_velocities_iterations)
        prey_std = np.vstack(prey_velocities_std_iterations)
        pred_velocities = np.vstack(predator_mean_velocities_iterations)
        pred_std = np.vstack(predator_velocities_std_iterations)

        prey_mean_velocities = np.mean(prey_velocities, axis=0)
        prey_mean_std= np.mean(prey_std, axis=0)
        
        plot_mean_velocities_vs_variable(t_values, prey_mean_velocities, prey_mean_std, "presas", "Tiempo (s)", f"N_pred_{N_pred}_alpha_{fixed_alpha}_iterations_{iterations}")

        pred_mean_velocities = np.mean(pred_velocities, axis=0)
        pred_mean_std= np.mean(pred_std, axis=0)

        plot_mean_velocities_vs_variable(t_values, pred_mean_velocities, pred_mean_std, "depredadores", "Tiempo (s)", f"N_pred_{N_pred}_alpha_{fixed_alpha}_iterations_{iterations}")

        prey_total_mean_velocity = np.mean(prey_mean_velocities)
        pred_total_mean_velocity = np.mean(pred_mean_velocities)
        #check
        prey_total_velocity_std = np.std(prey_mean_velocities)
        pred_total_velocity_std = np.std(pred_mean_velocities)

        prey_mean_velocities_variable.append(prey_total_mean_velocity)
        predator_mean_velocities_variable.append(pred_total_mean_velocity)

        prey_velocities_std_variable.append(prey_total_velocity_std)
        predator_velocities_std_variable.append(pred_total_velocity_std)

    plot_mean_velocities_vs_variable(N_predators, prey_mean_velocities_variable, prey_velocities_std_variable, "presas", "Población inicial de depredadores",f"N_pred_{N_predators}_alpha_{fixed_alpha}_iterations_{iterations}") 
    plot_mean_velocities_vs_variable(N_predators, predator_mean_velocities_variable, predator_velocities_std_variable, "depredadores", "Población inicial de depredadores",f"N_pred_{N_predators}_alpha_{fixed_alpha}_iterations_{iterations}") 

    # Tiempo medio de vida por especie
    # check alpha to make better comparisons
    fixed_alpha = 0.9
    #fixed_alpha = 1.2
    iterations = 10
    #iterations = 2

    # mean_life vs N_pred
    prey_mean_lives_variable = []
    predator_mean_lives_variable = []
    prey_lives_std_variable = []
    predator_lives_std_variable = [] 

    for N_pred in N_predators:
        prey_mean_lives_iterations = []
        predator_mean_lives_iterations = []
        prey_lives_std_iterations = []
        predator_lives_std_iterations = [] 
        for iteration in range(1, iterations):
            variables_label = f"N_pred_{N_pred}_alpha_{fixed_alpha}_iteration_{iteration}"
            output_filename = f"{basic_output_filename}_{variables_label}.txt" 
            prey_mean_lives, prey_lives_std, predator_mean_lives, predator_lives_std = get_mean_life_duration_for_both_species(output_filename)
            prey_mean_lives_iterations.append(prey_mean_lives)
            prey_lives_std_iterations.append(prey_lives_std)
            predator_mean_lives_iterations.append(predator_mean_lives)
            predator_lives_std_iterations.append(predator_lives_std)
        
        prey_mean_lives= np.mean(prey_mean_lives_iterations)
        prey_mean_std= np.mean(prey_lives_std_iterations)
        prey_mean_lives_variable.append(prey_mean_lives)
        prey_lives_std_variable.append(prey_mean_std)

        pred_mean_lives = np.mean(predator_mean_lives_iterations)
        pred_mean_std= np.mean(predator_lives_std_iterations)
        predator_mean_lives_variable.append(pred_mean_lives)
        predator_lives_std_variable.append(pred_mean_std)

    plot_mean_life_duration_vs_variable(N_predators, prey_mean_lives_variable, prey_lives_std_variable, "presas", "Población inicial de depredadores",f"N_pred_{N_predators}_alpha_{fixed_alpha}_iterations_{iterations}") 
    plot_mean_life_duration_vs_variable(N_predators, predator_mean_lives_variable, predator_lives_std_variable, "depredadores", "Población inicial de depredadores",f"N_pred_{N_predators}_alpha_{fixed_alpha}_iterations_{iterations}") 

    # mean_life vs alpha
    # check for best N_pred
    fixed_N_pred = 20
    #fixed_N_pred = 2

    prey_mean_lives_variable = []
    predator_mean_lives_variable = []
    prey_lives_std_variable = []
    predator_lives_std_variable = []  
    for alpha in alpha_values:
        prey_mean_lives_iterations = []
        predator_mean_lives_iterations = []
        prey_lives_std_iterations = []
        predator_lives_std_iterations = [] 
        for iteration in range(1, iterations):
            variables_label = f"N_pred_{fixed_N_pred}_alpha_{alpha}_iteration_{iteration}"
            output_filename = f"{basic_output_filename}_{variables_label}.txt" 
            prey_mean_lives, prey_lives_std, predator_mean_lives, predator_lives_std = get_mean_life_duration_for_both_species(output_filename)
            prey_mean_lives_iterations.append(prey_mean_lives)
            prey_lives_std_iterations.append(prey_lives_std)
            predator_mean_lives_iterations.append(predator_mean_lives)
            predator_lives_std_iterations.append(predator_lives_std)
        
        prey_mean_lives= np.mean(prey_mean_lives_iterations)
        prey_mean_std= np.mean(prey_lives_std_iterations)
        prey_mean_lives_variable.append(prey_mean_lives)
        prey_lives_std_variable.append(prey_mean_std)

        pred_mean_lives = np.mean(predator_mean_lives_iterations)
        pred_mean_std= np.mean(predator_lives_std_iterations)
        predator_mean_lives_variable.append(pred_mean_lives)
        predator_lives_std_variable.append(pred_mean_std)

    plot_mean_life_duration_vs_variable(alpha_values, prey_mean_lives_variable, prey_lives_std_variable, "presas", "Alpha",f"N_pred_{fixed_N_pred}_alpha_{alpha_values}_iterations_{iterations}") 
    plot_mean_life_duration_vs_variable(alpha_values, predator_mean_lives_variable, predator_lives_std_variable, "depredadores", "Alpha",f"N_pred_{fixed_N_pred}_alpha_{alpha_values}_iterations_{iterations}") 