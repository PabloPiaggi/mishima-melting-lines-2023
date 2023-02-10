#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --ntasks-per-socket=2
#SBATCH --cpus-per-task=32
#SBATCH --gpu-bind=map_gpu:0,1,2,3
#SBATCH --gpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --job-name="3500bar" 

module purge
module load rh/devtoolset/7
module load cudatoolkit/10.0
module load cudnn/cuda-10.0/7.6.1
module load openmpi/gcc/3.1.4/64
module load anaconda3/2019.3

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export PLUMED_NUM_THREADS=$SLURM_CPUS_PER_TASK

############################################################################
# Variables definition
############################################################################
LAMMPS_HOME=/home/ppiaggi/Programs/DeepMD/lammps2/src
LAMMPS_EXE=${LAMMPS_HOME}/lmp_mpi
cycles=30
partitions=1
pressure=3500
temperatures="270 275"
############################################################################

for temperature in ${temperatures}
do
   cd IceIV-${temperature}.0-${pressure}.0 
   ############################################################################
   # Run
   ############################################################################
   if [ -e runno ] ; then
      #########################################################################
      # Restart runs
      #########################################################################
      srun -N 1 -n 4 $LAMMPS_EXE -partition ${partitions}x4 -in Restart.lmp &
      #########################################################################
   else
      #########################################################################
      # First run
      #########################################################################
      nn=1
      srun -N 1 -n 4 $LAMMPS_EXE -partition ${partitions}x4 -in start.lmp &
      #########################################################################
   fi
   ############################################################################
   cd ../
done

wait

############################################################################
# Prepare next run
############################################################################
# Back up
############################################################################
for temperature in ${temperatures}
do
   cd IceIV-${temperature}.0-${pressure}.0 
   j=0
   nn=`tail -n 1 runno | awk '{print $1}'`
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
   cd ../
done

############################################################################
# Resubmitting again
############################################################################
sbatch --dependency=afterok:$SLURM_JOB_ID job-${pressure}.sh
############################################################################

date
