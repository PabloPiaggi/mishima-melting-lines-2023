#!/bin/bash
#SBATCH --nodes=1               
#SBATCH --ntasks=28              # total number of tasks across all nodes
#SBATCH --ntasks-per-node=28     # total number of tasks in each node
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=300M       # memory per cpu-core (4G is default)
#SBATCH --time=97:00:00          # total run time limit (HH:MM:SS)
#SBATCH --job-name="V-1" 

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_WHOLE=1
export SLURM_OVERLAP=1
pwd; hostname; date

module purge
module load anaconda3/2021.5
module load intel/2021.1.2
module load intel-mpi/intel/2021.1.1
module load fftw/intel-2021.1/intel-mpi/3.3.9

python integrate-clausius-clapeyron.py

date
