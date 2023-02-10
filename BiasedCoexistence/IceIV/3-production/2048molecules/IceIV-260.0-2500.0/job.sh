#!/bin/bash
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=32
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=500M
#SBATCH --job-name="L-260-2500" 
#SBATCH --gres=gpu:4

module purge
module load cudatoolkit/10.0
module load cudnn/cuda-10.0/7.6.1
module load openmpi/gcc/3.1.4/64
module load anaconda3/2019.3

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export PLUMED_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SLURM_WHOLE=1

############################################################################
# Variables definition
############################################################################
LAMMPS_HOME=/home/ppiaggi/Programs/DeepMD/lammps2/src
LAMMPS_EXE=${LAMMPS_HOME}/lmp_mpi
cycles=45
partitions=1
############################################################################

############################################################################
# Run
############################################################################
if [ -e Startdone.txt ] ; then
   #########################################################################
   # Restart runs
   #########################################################################
   nn=`tail -n 1 runno | awk '{print $1}'`
   mpirun -np $SLURM_NTASKS $LAMMPS_EXE -partition ${partitions}x4 -in Restart.lmp
   #########################################################################
elif [ -e Equildone.txt ] ; then
   #########################################################################
   # First run
   #########################################################################
   nn=1
   mpirun -np $SLURM_NTASKS $LAMMPS_EXE -partition ${partitions}x4 -in start.lmp
   #########################################################################
elif [ -e Bulkdone.txt ] ; then
   #########################################################################
   # Equilibration
   #########################################################################
   mpirun -np $SLURM_NTASKS $LAMMPS_EXE -partition ${partitions}x4 -in equil.lmp
   #########################################################################
else
   #########################################################################
   # Bulk equilibration for dimensions
   #########################################################################
   nn=1
   mpirun -np $SLURM_NTASKS $LAMMPS_EXE -partition ${partitions}x4 -in bulk.lmp
   python BoxDimensions.py > in.boxdimensions
   #########################################################################
fi
############################################################################


############################################################################
# If production run has started
############################################################################
if [ -e Startdone.txt ] ; then
   ############################################################################
   # Prepare next run
   ############################################################################
   # Back up
   ############################################################################
   j=0
   cp restart2.lmp.${j} restart2.lmp.${j}.${nn}
   cp restart.lmp.${j} restart.lmp.${j}.${nn}
   cp data.final.${j} data.final.${j}.${nn}
   cp log.lammps.${j} log.lammps.${j}.${nn}
   
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
fi
############################################################################

############################################################################
# Resubmitting again if everything went well so far
############################################################################
if ! grep -q 'ERROR' log.lammps.*; then
        sbatch --dependency=afterok:$SLURM_JOB_ID job.sh
fi
############################################################################

date
