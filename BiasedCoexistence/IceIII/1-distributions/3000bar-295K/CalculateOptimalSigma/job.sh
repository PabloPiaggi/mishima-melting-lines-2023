#!/bin/bash
#SBATCH --ntasks=20              # total number of tasks across all nodes
#SBATCH --cpus-per-task=1       # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=300M      # memory per cpu-core (4G is default)
#SBATCH --time=01:00:00         # total run time limit (HH:MM:SS)
#SBATCH --job-name="Analysis" 
#SBATCH --constraint=haswell|broadwell|skylake|cascade   # exclude ivy nodes

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export PLUMED_NUM_THREADS=$SLURM_CPUS_PER_TASK

pwd; hostname; date

module purge
module load intel/2021.1.2
module load intel-mpi/intel/2021.1.1
module load anaconda3/2021.5
module load fftw/intel-2021.1/intel-mpi/3.3.9

source ~/Programs/Plumed/plumed2-master-intel/sourceme.sh

for i in `seq 0.0675 0.0025 0.0675`
do
        for phase in IceIII Liquid
        do
                cd $phase
                sed "s/replace/$i/g" plumed-base.dat > plumed.dat
                srun plumed driver --plumed plumed.dat --mf_dcd dump.dcd > /dev/null
                cd ../
        done
        result=`python script.py`
        echo $i $result
        for phase in IceIII Liquid
        do
                cd $phase
                #rm COLVAR histo*
                cd ../
        done
done
