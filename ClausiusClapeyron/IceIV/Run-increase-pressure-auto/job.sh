#!/bin/bash
#SBATCH --nodes=2               
#SBATCH --ntasks=8               # total number of tasks across all nodes
#SBATCH --ntasks-per-node=4      # total number of tasks in each node
#SBATCH --cpus-per-task=7        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=300M       # memory per cpu-core (4G is default)
#SBATCH --time=80:00:00          # total run time limit (HH:MM:SS)
#SBATCH --job-name="RK4up" 
#SBATCH --gres=gpu:4             # number of gpus per node

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_WHOLE=1
pwd; hostname; date

module purge
module load cudatoolkit/10.0
module load cudnn/cuda-10.0/7.6.1
module load openmpi/gcc/3.1.4/64
module load anaconda3/2019.3

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_WHOLE=1

python integrate-clausius-clapeyron.py

date
