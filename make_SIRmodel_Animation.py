
from matplotlib import pyplot as plt
from matplotlib import animation

def main():
    
    batch_file = 'RUN_SIRmodel_RecoveryTime-varied.bat'
    files = get_results_files(batch_file)


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