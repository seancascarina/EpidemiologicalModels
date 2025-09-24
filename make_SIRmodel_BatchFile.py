
import numpy as np

def main():

    
    # CHANGE THESE TO VARY DIFFERENT PARAMETERS====
    variable = 'RecoveryTime'
    flag = '-v'
    values = np.linspace(3, 12, num=19)
    #==============================================
    
    output = open(f'RUN_SIRmodel_{variable}-varied.bat', 'w')
    for value in values:
        output.write(f'python basic_SIR_model.py {flag} {value} -d 200 -o SIRmodel_{value}-{variable}_Results.tsv\n')
        
    output.close()
        

if __name__ == '__main__':
    main()