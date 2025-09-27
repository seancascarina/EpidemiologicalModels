
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import seaborn as sns
categories = ['Susceptible', 'Infected', 'Recovered', 'Effective Reproduction Number']
color_palette = sns.color_palette()[:len(categories)]


def animate(i, df, param_values, num_interpolations):

    y = df[categories[0]][i]
    x = [x for x in range(len(y))]
    line1.set_data(x, y)
    
    y = df[categories[1]][i]
    line2.set_data(x, y)
    
    y = df[categories[2]][i]
    line3.set_data(x, y)
    
    y = df[categories[3]][i]
    line4.set_data(x, y)

    if i % num_interpolations == 0:
        index = int(i / num_interpolations)
        value = param_values[index]
        title.set_text(f"Recovery Time: {value} days")
    
    return line1, line2, line3, line4, title
    
    
def calc_interpolations(df, num_interpolations):
    
    files = list(df.keys())
    interps_df = {}
    for category in categories:
        interps_matrix = []
        for i, file in enumerate(files[:-1]):
            next_file = files[i+1]
            interp = np.array( [ np.linspace(df[file][category][j], df[next_file][category][j], num=num_interpolations) for j in range(len(df[file][category])) ] )
            interps_matrix += list(interp.T)    # TRANSPOSE THE INTERPOLATION SO THAT EACH ROW REPRESENTS THE NEW Y-AXIS INTERPOLATION VALUES OF LENGTH 200 (REPRESENTING THE NUMBER OF DAYS)

        interps_matrix = np.array(interps_matrix)
        interps_df[category] = interps_matrix

    return interps_df


def init():
    """Initialization function. Plots the background of each frame.
    """
    
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])

    return line1, line2, line3, line4
    

def get_data(file, df, params):
    
    h = open(file)
    params_header = h.readline().rstrip().split(' ')
    if not params:
        params = parse_params_header(params_header)
        
    header = h.readline()
    for line in h:
        day, category, value = line.rstrip().split('\t')
        df[file][category] = df[file].get(category, [])
        df[file][category].append(float(value))
        
    h.close()
    
    return df, params
    
        
def parse_params_header(params_header):
    
    params = [x.split('=')[1] for x in params_header[1:]]
    
    return params
    

def get_results_files(batch_file):
    
    files = []
    h = open(batch_file)
    for line in h:
        start, end = line.rstrip().split('-o ')
        results_file, *_ = end.split(' ')
        files.append(results_file)
        
    h.close()
    
    return files
    
    
def get_ReproductionNumber_bounds(files):
    
    max_Rt = 0
    for file in files:
        h = open(file)
        header = h.readline()
        
        for line in h:
            day, category, value = line.rstrip().split('\t')
            if category != 'Effective Reproduction Number':
                continue
                
            value = float(value)
            if value > max_Rt:
                max_Rt = value
                
    return max_Rt
    
    
batch_file = 'RUN_SIRmodel_with_EffectiveReproductionNumber_RecoveryTime-varied.bat'
param_values = list(np.linspace(3, 12, num=19))
initial_title = f"Recovery Time: {param_values.pop(0)} days"
files = get_results_files(batch_file)
num_interpolations = 5
fps = 30

df = {}
params = []
for file in files:
    df[file] = df.get(file, {})
    df, params = get_data(file, df, params)
interps_df = calc_interpolations(df, num_interpolations)

N = int(params[0])
days = int(params[-1])
max_Rt = get_ReproductionNumber_bounds(files)

# INITIALIZE THE FIGURE
fig = plt.figure()
ax = plt.axes(xlim=(0, days), ylim=(0, N))
ax2 = ax.twinx()
ax2.set_ylim(0, max_Rt)
ax2.tick_params(axis='y', colors=color_palette[-1], which='both')
ax2.set_ylabel('Effective Reproduction Number', fontname='Arial', fontsize=14, color=color_palette[-1])

ax.set_xlabel('Day', fontname='Arial', fontsize=14)
ax.set_ylabel('Number of Individuals\n(per 1000)', fontname='Arial', fontsize=14)
for tick in ax.get_xticklabels():
    tick.set_fontsize(12)
    tick.set_fontname('Arial')
for tick in ax.get_yticklabels():
    tick.set_fontsize(12)
    tick.set_fontname('Arial')
line1, = ax.plot([], [], lw=2, color=color_palette[0], label=categories[0])
line2, = ax.plot([], [], lw=2, color=color_palette[1], label=categories[1])
line3, = ax.plot([], [], lw=2, color=color_palette[2], label=categories[2])
line4, = ax2.plot([], [], lw=2, color=color_palette[3], label=categories[3])
lines = [line1, line2, line3]
ax.legend(loc=3, bbox_to_anchor=(1,1))
title = ax.text(0.5, 1.0, initial_title,
                ha='center', va='bottom', transform=ax.transAxes, animated=True)

fig.tight_layout()

all_frames = []
frame = 0
for i in range(len(df) - 1):
    new_frames = [x for x in range(frame, frame+num_interpolations)]
    new_frames += [max(new_frames)]*fps
    all_frames += new_frames
    frame = max(new_frames) + 1
    
print(all_frames)
num_frames = num_interpolations * (len(df) - 1)
anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=(interps_df, param_values, num_interpolations),
                           frames=all_frames, interval=1, blit=True)

anim.save('SIRmodel_withEffectiveReproductionNumber_RecoveryTimeVaried.gif', fps=fps, dpi=300)
plt.close()
# plt.show()
