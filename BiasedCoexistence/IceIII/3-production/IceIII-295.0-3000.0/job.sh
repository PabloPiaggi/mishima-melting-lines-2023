#!/bin/bash
#SBATCH --ntasks=4               # total number of tasks across all nodes
#SBATCH --cpus-per-task=7        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=500M       # memory per cpu-core (4G is default)
#SBATCH --time=72:00:00          # total run time limit (HH:MM:SS)
#SBATCH --job-name="3-295-3000" 
#SBATCH --gres=gpu:4             # number of gpus per node

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
cycles=4
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
