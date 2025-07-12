import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

# animation

# show preys as blue circles
# show predators as red circles
# death animations: after changing its colors it dissapears after 2 seconds
# if a predator dies of hunger -> circle turns to green
# if a predator/prey dies of age -> circle turns to black
# if a prey is hunted -> prey circle turns to gray

#check: change later
output_file = "simulation_N_pred_20_alpha_0.80_iteration_1.txt"

data = pd.read_csv(
    output_file,
    sep=' ',
    names=['t', 'id', 'species', 'x', 'y', 'vx', 'vy', 'r', 'lifetime', 'reproduction_time', 'hunger_time', 'status']
)

# Collect unique time steps
time_steps = sorted(data['t'].unique())

# To track death animations
death_registry = {}

# Create figure
fig, ax = plt.subplots(figsize=(8, 8))

# Set limits to show circular border
ax.set_xlim(-16, 16)
ax.set_ylim(-16, 16)
ax.set_aspect('equal')

# Draw border circle
border = patches.Circle((0, 0), radius=15,
                        fill=False, edgecolor='black', linewidth=2)
ax.add_patch(border)

circle_artists = []

def get_color(species, status):
    if status == 'ALIVE':
        return 'blue' if species == 'PREY' else 'red'
    elif status == 'DEAD_HUNGER':
        return 'green'
    elif status == 'DEAD_AGE':
        return 'black'
    elif status == 'DEAD_EATEN':
        return 'gray'
    else:
        return 'pink'

def update(frame):
    global death_registry, circle_artists

    # Remove previous circles
    for c in circle_artists:
        c.remove()
    circle_artists = []

    t = time_steps[frame]
    df_t = data[data['t'] == t]

    # Alive individuals
    alive = df_t[df_t['status'] == 'ALIVE']
    for _, row in alive.iterrows():
        color = get_color(row['species'], row['status'])
        circle = patches.Circle(
            (row['x'], row['y']),
            radius=row['r'],
            facecolor=color,
            edgecolor='black'
        )
        ax.add_patch(circle)
        circle_artists.append(circle)

    # Newly dead individuals
    dead = df_t[df_t['status'] != 'ALIVE']
    for _, row in dead.iterrows():
        death_registry[row['id']] = {
            'x': row['x'],
            'y': row['y'],
            'r': row['r'],
            'species': row['species'],
            'status': row['status'],
            't_death': t
        }

    # Show dying individuals if they’re still in 2s window
    still_showing = {}
    for obj_id, info in death_registry.items():
        if t - info['t_death'] <= 2:
            color = get_color(info['species'], info['status'])
            circle = patches.Circle(
                (info['x'], info['y']),
                radius=info['r'],
                facecolor=color,
                edgecolor='black'
            )
            ax.add_patch(circle)
            circle_artists.append(circle)
            still_showing[obj_id] = info
    death_registry = still_showing

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(time_steps),
    interval=500,
    repeat=False
)

plt.show()
