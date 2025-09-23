
import numpy as np
from scipy.integrate import solve_ivp

def main():

    N = 10000   # POPULATION SIZE
    Ii = 1       # INITIAL NUMBER OF INFECTED PEOPLE
    Ri = 0       # INITIAL NUMBER OF RECOVERED PEOPLE
    Si = N - Ii - Ri   # INITIAL NUMBER OF SUSCEPTIBLE PEOPLE
    
    beta = 0.2  # RATE OF TRANSMISSION (NUMBER OF PEOPLE INFECTED PER DAY FOR EACH INFECTED PERSON)
    gamma = 1/7    # RATE OF RECOVERY (INVERSE OF AVERAGE NUMBER OF DAYS FROM INFECTION ONSET TO RECOVERY)
    n_days = np.linspace(0, 365, num=365)  # NUMBER OF DAYS TO RUN THE SIMULATION FOR
    
    yi = Si, Ii, Ri
    sol = solve_ivp(equations, [min(n_days), max(n_days)], yi, args=(N, beta, gamma), t_eval=n_days)
    labels = ['Susceptible', 'Infected', 'Recovered']
    df = make_plotting_df(sol.y, labels)
    


def make_plotting_df(vals_list, labels):
    
    df = {'Number of People':[],
        'Day':[],
        'Category':[]}
    for i, vals in enumerate(vals_list):
        label = labels[i]
        df['Number of People'] += list(vals)
        df['Day'] += [x for x in range(len(vals))]
        df['Category'] += [label]*len(vals)
        
    return df
    

def equations(n_days, y, N, beta, gamma):
    
    S, I, R = y
    dSdt = -(beta * S * I) / N
    dIdt = (beta * S * I) / N - (gamma * I)
    dRdt = gamma * I
    
    return dSdt, dIdt, dRdt
    

if __name__ == '__main__':
    main()