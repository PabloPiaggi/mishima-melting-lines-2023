#!/bin/bash
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=7
#SBATCH --time=144:00:00
#SBATCH --mem-per-cpu=500M
#SBATCH --job-name="Eq-270-3000" 
#SBATCH --gres=gpu:4

module purge
module load rh/devtoolset/4
module load cudatoolkit/10.0
module load cudnn/cuda-10.0/7.6.3
module load openmpi/gcc/3.1.3/64

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export PLUMED_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_WHOLE=1

############################################################################
# Variables definition
############################################################################
LAMMPS_EXE=/home/ppiaggi/Programs/Software-deepmd-kit-1.0/lammps-git4/src/lmp_mpi
############################################################################

# run NPT sampling
mpirun $LAMMPS_EXE -i in.lammps.init
rm in.boxdimensions
python BoxDimensions.py > in.boxdimensions
mpirun $LAMMPS_EXE -i in.lammps.equil

date
