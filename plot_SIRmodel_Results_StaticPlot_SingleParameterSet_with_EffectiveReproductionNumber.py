    
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
color_palette = sns.color_palette()

def main(args):

    file = args.data_file
    df, params = get_data(file)
    lineplot(df, file)
    
        
def lineplot(df, file):
    
    Rt_vals = [x for i, x in enumerate(df['Number of Individuals']) if df['Category'][i] == 'Effective Reproduction Number']
    df = pd.DataFrame(df)
    df = df[df['Category'] != 'Effective Reproduction Number']
    
    ax = sns.lineplot(x='Day', y='Number of Individuals', data=df, hue='Category')
    ax2 = ax.twinx()
    ax2.plot([x for x in range(len(Rt_vals))], Rt_vals, lw=2, color=color_palette[3], label=r'$\it{Rt}$')
    ax2.set_ylim(0, max(Rt_vals)+0.2)
    plt.xticks(fontname='Arial', fontsize=12)
    plt.yticks(fontname='Arial', fontsize=12)
    plt.xlabel('Day', fontname='Arial', fontsize=14)
    plt.ylabel('Number of Individuals\n(per 1000)', fontname='Arial', fontsize=14)
    plt.legend(loc=2, bbox_to_anchor=(1,1))
    plt.savefig(file.replace('_Results.tsv', 'with_Rt_Lineplot.png'), bbox_inches='tight', dpi=600)
    plt.close()
    

def get_data(file):
    
    df = {'Day':[],
            'Number of Individuals':[],
            'Category':[]}
            
    h = open(file)
    params_header = h.readline().rstrip().split(' ')
    params = parse_params_header(params_header)
        
    header = h.readline()
    for line in h:
        day, category, value = line.rstrip().split('\t')
        df['Day'].append( int(day) )
        df['Number of Individuals'].append( float(value) )
        df['Category'].append( category )
        
        # df[file][category] = df[file].get(category, [])
        # df[file][category].append(float(value))
        
    h.close()
    
    return df, params
    

def parse_params_header(params_header):
    
    params = [x.split('=')[1] for x in params_header[1:]]
    
    return params
    

def get_args(arguments):
    
    parser = argparse.ArgumentParser(description='Plot epidemiological model results.', prog='plot_SIRmodel_data')
    
    parser.add_argument('data_file', type=str, help="""Results file from an epidemiological model simulation.""")

    args = parser.parse_args(arguments)
    
    return args
    
    
if __name__ == '__main__':
    import sys, argparse
    args = get_args(sys.argv[1:])
    main(args)
