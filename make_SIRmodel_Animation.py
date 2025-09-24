
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

def main():
    
    batch_file = 'RUN_SIRmodel_RecoveryTime-varied.bat'
    values = np.linspace(3, 12, num=19)
    files = get_results_files(batch_file)
    
    df = {}
    params = []
    for file in files:
        df[file] = df.get(file, {})
        df, params = get_data(file, df, params)
    calc_interpolations(df)
    N = int(params[0])
    days = int(params[-1])

    # INITIALIZE THE FIGURE
    fig = plt.figure()
    ax = plt.axes(xlim=(0, days), ylim=(0, N))
    line, = ax.plot([], [], lw=2)
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=(df),
                               frames=days, interval=20, blit=True)
    
def calc_interpolations(df):
    
    files = list(df.keys())
    interps_df = {}
    for category in ['Susceptible', 'Infected', 'Recovered']:
        interps_df[category] = []
        for i, file in enumerate(files[:-1]):
            next_file = files[i+1]
            interp = [ np.linspace(df[file][category][j], df[next_file][category][j], num=200) for j in range(len(df[file][category])) ]
            interps_df[category] += interp
            
    print(interps_df, len(interps_df['Susceptible']))
    
    return interps_df


def init():
    """Initialization function. Plots the background of each frame.
    """
    
    line.set_data([], [])
    return line,
    

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
    

if __name__ == '__main__':
    main()