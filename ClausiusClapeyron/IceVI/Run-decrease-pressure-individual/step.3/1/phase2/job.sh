#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=4              # total number of tasks across all nodes
#SBATCH --ntasks-per-node=4      # total number of tasks in each node
#SBATCH --cpus-per-task=7
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=500M
#SBATCH --job-name="liqVI" 
#SBATCH --gres=gpu:4

module purge
module load anaconda3
module load cudatoolkit/10.0
module load cudnn/cuda-10.0/7.6.3
module load openmpi/gcc/3.1.3/64
module list

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_WHOLE=1

############################################################################
# Variables definition
############################################################################
LAMMPS_HOME=/home/ppiaggi/Programs/Software-deepmd-kit-1.0/lammps-git4/src
LAMMPS_EXE=${LAMMPS_HOME}/lmp_mpi
cycles=1
############################################################################

############################################################################
# Run
############################################################################
if [ -e runno ] ; then
   #########################################################################
   # Restart runs
   #########################################################################
   nn=`tail -n 1 runno | awk '{print $1}'`
   mpirun -np 4 $LAMMPS_EXE -sf omp -i in.lammps.phase2.restart
   #########################################################################
else
   #########################################################################
   # First run
   #########################################################################
   nn=1
   # Number of partitions
   mpirun -np 4 $LAMMPS_EXE -sf omp -i in.lammps.phase2
   #########################################################################
fi
############################################################################


############################################################################
# Prepare next run
############################################################################
# Back up
############################################################################
cp water.data.final.phase2 water.data.final.phase2.${nn}
cp restart.lmp restart.lmp.${nn}
cp log.lammps log.lammps.${nn}

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
