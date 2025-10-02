
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.integrate import solve_ivp

def main(args):

    N = args.population_size
    Ii = args.infected
    Ri = args.recovered
    Si = N - Ii - Ri
    
    beta = args.beta
    gamma = 1 / args.recovery_time
    delta = args.delta
    n_days = args.days
    days = np.linspace(0, n_days, n_days) 
    
    output = open(args.output_file, 'w')
    output.write(f'PARAMETERS: population_size={N} infected={Ii} recovered={Ri} beta={beta} gamma={gamma} delta={delta} days={n_days}\n')
    output.write('\t'.join(['Day', 'Category', 'Value (Number of People)']) + '\n')
    
    yi = Si, Ii, Ri
    sol = solve_ivp(equations, [min(days), max(days)], yi, args=(N, beta, gamma, delta), t_eval=days)
    labels = ['Susceptible', 'Infected', 'Recovered', 'Effective Reproduction Number']

    solutions = list(sol.y)

    effective_reproduction_numbers = [(beta * (S/N)) / gamma for i, S in enumerate(sol.y[0])]
    solutions.append( effective_reproduction_numbers )
    
    for i, vals in enumerate(solutions):
        label = labels[i]
        for j, val in enumerate(vals):
            output.write('\t'.join([str(x) for x in (j, label, val)]) + '\n')
            
    output.close()
    

def equations(n_days, y, N, beta, gamma, delta):
    
    S, I, R = y
    dSdt = -(beta * S * I) / N + (delta * R)
    dIdt = (beta * S * I) / N - (gamma * I)
    dRdt = (gamma * I) - (delta * R)
    
    return dSdt, dIdt, dRdt
    

def get_args(arguments):
    
    parser = argparse.ArgumentParser(description='Run SIR model simulation.', prog='SIR')
    
    parser.add_argument('-p', '--population_size', type=int, default=1000, help="""Population size in number of individuals ("N" in many epidemiological models).""")
    parser.add_argument('-i', '--infected', type=int, default=1, help="""Number of infected individuals at the start of the simulation.""")
    parser.add_argument('-r', '--recovered', type=int, default=0, help="""Number of recovered individuals at the start of the simulation.""")
    parser.add_argument('-b', '--beta', type=float, default=0.25, help="""Beta transmission rate.""")
    parser.add_argument('-v', '--recovery_time', type=float, default=10, help="""Recovery time in days. This is used to calculate gamma (inverse of recovery time).""")
    parser.add_argument('-d', '--days', type=int, default=365, help="""Number of days to run the simulation for.""")
    parser.add_argument('-l', '--delta', type=float, default=0.05, help="""Rate of immunity loss.""")
    parser.add_argument('-o', '--output_file', type=str, default='SIRSmodel_Results.tsv', help="""Output file to write SIR model results to.""")

    args = parser.parse_args(arguments)
    
    return args
    
    
if __name__ == '__main__':
    import sys, argparse
    args = get_args(sys.argv[1:])
    main(args)