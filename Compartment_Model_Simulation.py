
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.integrate import solve_ivp

def main(args):

    N = args.population_size
    Ii = args.infected
    Ri = args.recovered
    Di = 0  # MIGHT WANT TO MAKE THESE COMMAND-LINE ARGUMENTS
    Vi = 0  # MIGHT WANT TO MAKE THESE COMMAND-LINE ARGUMENTS
    Ei = 0  # MIGHT WANT TO MAKE THESE COMMAND-LINE ARGUMENTS
    Si = N - Ii - Ri    # MIGHT WANT TO INCORPORATE NEW VARIABLES INTO THIS CALCULATION
    
    beta = args.beta
    gamma = 1 / args.recovery_time
    delta = args.delta
    mortality_rate = args.mortality_rate
    vaccination_rate = args.vaccination_rate
    latency = args.latency
    n_days = args.days
    days = np.linspace(0, n_days, n_days) 
    
    model_type = args.type_of_model
    output_file = args.output_file
    if not output_file:
        output_file = model_type + '_Model_Results.tsv'
    else:
        if '.' not in output_file:
            output_file += '.tsv'
        
    output = open(output_file, 'w')
    output.write(f'PARAMETERS: population_size={N} infected={Ii} recovered={Ri} beta={beta} gamma={gamma} delta={delta} days={n_days}\n')
    output.write('\t'.join(['Day', 'Category', 'Value (Number of People)']) + '\n')
    
    if model_type == 'SIR':
        yi = Si, Ii, Ri
        labels = ['Susceptible', 'Infected', 'Recovered', 'Effective Reproduction Number']
        sol = solve_ivp(equations_SIR, [min(days), max(days)], yi, args=(N, beta, gamma), t_eval=days)
    elif model_type == 'SIRS':
        yi = Si, Ii, Ri
        labels = ['Susceptible', 'Infected', 'Recovered', 'Effective Reproduction Number']
        sol = solve_ivp(equations_SIRS, [min(days), max(days)], yi, args=(N, beta, gamma, delta), t_eval=days)
    elif model_type == 'SIS':
        yi = Si, Ii
        labels = ['Susceptible', 'Infected', 'Effective Reproduction Number']
        sol = solve_ivp(equations_SIS, [min(days), max(days)], yi, args=(N, beta, gamma), t_eval=days)
    elif model_type == 'SIRD':
        yi = Si, Ii, Ri, Di
        labels = ['Susceptible', 'Infected', 'Recovered', 'Deceased', 'Effective Reproduction Number']
        sol = solve_ivp(equations_SIRD, [min(days), max(days)], yi, args=(N, beta, gamma, mortality_rate), t_eval=days)
    elif model_type == 'SIRV':
        yi = Si, Ii, Ri, Vi
        labels = ['Susceptible', 'Infected', 'Recovered', 'Vaccinated', 'Effective Reproduction Number']
        sol = solve_ivp(equations_SIRV, [min(days), max(days)], yi, args=(N, beta, gamma, vaccination_rate), t_eval=days)
    elif model_type == 'SEIR':
        yi = Si, Ei, Ii, Ri
        labels = ['Susceptible', 'Exposed', 'Infected', 'Recovered', 'Effective Reproduction Number']
        sol = solve_ivp(equations_SEIR, [min(days), max(days)], yi, args=(N, beta, gamma, latency), t_eval=days)
    elif model_type == 'SEIRS':
        yi = Si, Ei, Ii, Ri
        labels = ['Susceptible', 'Exposed', 'Infected', 'Recovered', 'Effective Reproduction Number']
        sol = solve_ivp(equations_SEIRS, [min(days), max(days)], yi, args=(N, beta, gamma, delta, latency), t_eval=days)
    
    # labels = ['Susceptible', 'Infected', 'Recovered', 'Effective Reproduction Number']

    solutions = list(sol.y)

    effective_reproduction_numbers = [(beta * (S/N)) / gamma for i, S in enumerate(sol.y[0])]
    solutions.append( effective_reproduction_numbers )
    
    for i, vals in enumerate(solutions):
        label = labels[i]
        for j, val in enumerate(vals):
            output.write('\t'.join([str(x) for x in (j, label, val)]) + '\n')
            
    output.close()
    
    
def equations_SIR(n_days, y, N, beta, gamma):
    
    S, I, R = y
    dSdt = -(beta * S * I) / N
    dIdt = (beta * S * I) / N - (gamma * I)
    dRdt = gamma * I

    return dSdt, dIdt, dRdt
    

def equations_SIRS(n_days, y, N, beta, gamma, delta):
    
    S, I, R = y
    dSdt = -(beta * S * I) / N + (delta * R)
    dIdt = (beta * S * I) / N - (gamma * I)
    dRdt = (gamma * I) - (delta * R)
    
    return dSdt, dIdt, dRdt
    
    
def equations_SIS(n_days, y, N, beta, gamma):
    
    S, I = y
    dSdt = -(beta * S * I) / N + (gamma * I)
    dIdt = (beta * S * I) / N - (gamma * I)

    return dSdt, dIdt
    
    
def equations_SIRD(n_days, y, N, beta, gamma, mortality_rate):
    
    S, I, R, D = y
    dSdt = -(beta * S * I) / N
    dIdt = (beta * S * I) / N - (gamma * I) - (mortality_rate * I)
    dRdt = gamma * I
    dDdt = mortality_rate * I

    return dSdt, dIdt, dRdt, dDdt
    
    
def equations_SIRV(n_days, y, N, beta, gamma, vaccination_rate):
    
    S, I, R, V = y
    # dSdt = -(beta * S * I) / N - (vaccination_rate * S) + (delta * V)     # COULD MODEL THIS WITH SOME RATE OF IMMUNITY LOSS, EITHER USING delta OR A SEPARATE RATE OF IMMUNITY LOSS IF IMMUNITY IS LOST AT A DIFFERENT RATE COMPARED TO IMMUNITY LOSS IN RECOVERED INDIVIDUALS
    dSdt = -(beta * S * I) / N - (vaccination_rate * S)
    dIdt = (beta * S * I) / N - (gamma * I)
    dRdt = gamma * I
    # dVdt = (vaccination_rate * S) - (delta * V)     # COULD MODEL THIS WITH SOME RATE OF IMMUNITY LOSS, EITHER USING delta OR A SEPARATE RATE OF IMMUNITY LOSS IF IMMUNITY IS LOST AT A DIFFERENT RATE COMPARED TO IMMUNITY LOSS IN RECOVERED INDIVIDUALS
    dVdt = vaccination_rate * S

    return dSdt, dIdt, dRdt, dVdt
    
    
def equations_SEIR(n_days, y, N, beta, gamma, latency):
    
    S, E, I, R = y
    dSdt = -(beta * S * I) / N
    dEdt = (beta * S * I) / N - (latency * E)
    dIdt = (latency * E) - (gamma * I)
    dRdt = gamma * I

    return dSdt, dEdt, dIdt, dRdt
    
    
def equations_SEIRS(n_days, y, N, beta, gamma, delta, latency):
    
    S, E, I, R = y
    dSdt = -(beta * S * I) / N + (delta * R)
    dEdt = (beta * S * I) / N - (latency * E)
    dIdt = (latency * E) - (gamma * I)
    dRdt = (gamma * I) - (delta * R)

    return dSdt, dEdt, dIdt, dRdt
    

def get_args(arguments):
    
    parser = argparse.ArgumentParser(description='Run compartment model simulation.', prog='CompartmentModel')
    
    parser.add_argument('-p', '--population_size', type=int, default=1000, help="""Population size in number of individuals ("N" in many epidemiological models).""")
    parser.add_argument('-i', '--infected', type=int, default=1, help="""Number of infected individuals at the start of the simulation.""")
    parser.add_argument('-r', '--recovered', type=int, default=0, help="""Number of recovered individuals at the start of the simulation.""")
    parser.add_argument('-b', '--beta', type=float, default=0.25, help="""Beta transmission rate.""")
    parser.add_argument('-v', '--recovery_time', type=float, default=10, help="""Recovery time in days. This is used to calculate gamma (inverse of recovery time).""")
    parser.add_argument('-d', '--days', type=int, default=365, help="""Number of days to run the simulation for.""")
    parser.add_argument('-l', '--delta', type=float, default=0.05, help="""Rate of immunity loss.""")
    parser.add_argument('-m', '--mortality_rate', type=float, default=0.005, help="""Rate of mortality (death) from the pathogen.""")
    parser.add_argument('-x', '--vaccination_rate', type=float, default=0.01, help="""Rate of vaccination.""")
    parser.add_argument('-w', '--latency', type=float, default=0.2, help="""Latency between exposure and infectious (i.e., the rate at which an individual passes from "Exposed" to "Infectious" in a SEIR-type model).""")
    parser.add_argument('-t', '--type_of_model', type=str, default='SIR', help="""Type of compartment model to use. Must be one of the following: SIR, SIRS, SIS.""")
    parser.add_argument('-o', '--output_file', type=str, default=None, help="""Output file to write compartment model results to.""")

    args = parser.parse_args(arguments)
    
    return args
    
    
if __name__ == '__main__':
    import sys, argparse
    args = get_args(sys.argv[1:])
    main(args)