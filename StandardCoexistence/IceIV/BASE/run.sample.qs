#!/bin/bash
#SBATCH -N 1   # node count
#SBATCH --ntasks-per-node=4
#SBATCH --ntasks-per-socket=2
#SBATCH --cpus-per-task=7
#SBATCH -t 24:00:00
#SBATCH --gres=gpu:4
#SBATCH --job-name="s-TEMP-PRESS" 

# load environment
module purge
module load cudatoolkit/10.0
module load cudnn/cuda-10.0/7.6.3
module load openmpi/gcc/3.1.3/64

LAMMPS_EXE=/home/ppiaggi/Programs/Software-deepmd-kit-1.0/lammps-git2/src/lmp_mpi
source /home/ppiaggi/Programs/Software-deepmd-kit-1.0/tensorflow-venv/bin/activate

# run NPT sampling
mpirun $LAMMPS_EXE -i in.lammps.sample

if [ -f "Sampledone.txt" ]; then
    echo "Simulation finished"
elif ! grep -q 'ERROR' slurm*; then
    echo "Continuing NPT sampling"
    sbatch --dependency=afterok:$SLURM_JOB_ID run.sample.qs
else
    echo "There is an error"
fi

