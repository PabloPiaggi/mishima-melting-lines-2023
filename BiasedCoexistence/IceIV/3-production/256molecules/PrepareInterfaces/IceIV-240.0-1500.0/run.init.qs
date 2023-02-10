#!/bin/bash
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=32
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=500M
#SBATCH --job-name="Eq-240-1500" 
#SBATCH --gres=gpu:2

module purge
module load rh/devtoolset/7
module load cudatoolkit/10.0
module load cudnn/cuda-10.0/7.6.1
module load openmpi/gcc/3.1.4/64
module load anaconda3/2019.3

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

############################################################################
# Variables definition
############################################################################
LAMMPS_HOME=/home/ppiaggi/Programs/DeepMD/lammps2/src
LAMMPS_EXE=${LAMMPS_HOME}/lmp_mpi
############################################################################

# run NPT sampling
mpirun $LAMMPS_EXE -i in.lammps.init
rm in.boxdimensions
python BoxDimensions.py > in.boxdimensions
mpirun $LAMMPS_EXE -i in.lammps.equil
