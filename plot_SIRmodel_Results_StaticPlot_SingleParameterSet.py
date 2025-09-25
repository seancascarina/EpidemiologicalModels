    
import matplotlib.pyplot as plt
import seaborn as sns

def main():

    file = 'SIRmodel_4.0-RecoveryTime_Results.tsv'
    df, params = get_data(file)
    print(df)

def get_data(file):
    
    df = {'Day':[],
            'Number of Individuals\n(per 1000)':[],
            'Category':[]}
            
    h = open(file)
    params_header = h.readline().rstrip().split(' ')
    params = parse_params_header(params_header)
        
    header = h.readline()
    for line in h:
        day, category, value = line.rstrip().split('\t')
        df['Day'].append( int(day) )
        df['Number of Individuals\n(per 1000)'].append( float(value) )
        df['Category'].append( category )
        
        # df[file][category] = df[file].get(category, [])
        # df[file][category].append(float(value))
        
    h.close()
    
    return df, params
    

def parse_params_header(params_header):
    
    params = [x.split('=')[1] for x in params_header[1:]]
    
    return params
    

if __name__ == '__main__':
    main()
