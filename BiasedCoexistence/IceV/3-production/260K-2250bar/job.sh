#!/bin/bash
#SBATCH -N 1   # node count
#SBATCH --ntasks-per-node=4
#SBATCH --ntasks-per-socket=2
#SBATCH --cpus-per-task=7
#SBATCH -t 25:00:00
#SBATCH --mem-per-cpu=300M       # memory per cpu-core (4G is default)
# SBATCH --mem=32G
#SBATCH --gres=gpu:4
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=tgartner@princeton.edu

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export PLUMED_NUM_THREADS=$SLURM_CPUS_PER_TASK

pwd; hostname; date

module purge
module load rh/devtoolset/4
module load cudatoolkit/10.0
module load cudnn/cuda-10.0/7.6.3
module load openmpi/gcc/3.1.3/64

############################################################################
# Variables definition
############################################################################
LAMMPS_EXE=/home/ppiaggi/Programs/Software-deepmd-kit-1.0/lammps-git4/src/lmp_mpi
source /home/ppiaggi/Programs/Software-deepmd-kit-1.0/tensorflow-venv/bin/activate
cycles=40
############################################################################

############################################################################
# Run
############################################################################
if [ -e runno ] ; then
   #########################################################################
   # Restart runs
   #########################################################################
   nn=`tail -n 1 runno | awk '{print $1}'`
   export SLURM_WHOLE=1
   mpirun -np $SLURM_NTASKS $LAMMPS_EXE -sf omp -in Restart.lmp
   #########################################################################
else
   #########################################################################
   # First run
   #########################################################################
   nn=1
   # Number of partitions
   export SLURM_WHOLE=1
   mpirun -np $SLURM_NTASKS $LAMMPS_EXE -sf omp -in start.lmp
   #########################################################################
fi
############################################################################


############################################################################
# Prepare next run
############################################################################
# Back up
############################################################################
j=0
cp log.lammps.${j} log.lammps.${j}.${nn}
cp restart2.lmp.${j} restart2.lmp.${j}.${nn}
cp restart.lmp.${j} restart.lmp.${j}.${nn}
cp data.final.${j} data.final.${j}.${nn}

############################################################################
# Check number of cycles
############################################################################
mm=$((nn+1))
echo ${mm} > runno
#cheking number of cycles
if [ ${nn} -ge ${cycles} ]; then
  exit
fi
############################################################################

############################################################################
# Resubmitting again
############################################################################
sbatch < job.sh
############################################################################

date
