#!/bin/bash
#SBATCH -N 1   # node count
#SBATCH --ntasks-per-node=4
#SBATCH --ntasks-per-socket=2
#SBATCH --cpus-per-task=7
#SBATCH -t 72:00:00
# SBATCH --mem=32G
#SBATCH --gres=gpu:4
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=tgartner@princeton.edu

# load environment
module load cudatoolkit/10.0
module load cudnn/cuda-10.0/7.6.3
module load openmpi/gcc/3.1.3/64
#module load fftw
source /home/tgartner/Software-deepmd-kit-1.0/tensorflow-venv/bin/activate
module load /home/tgartner/modulefiles/plumed-tg
# export OMP_NUM_THREADS=1

# run NPT sampling
mpirun /home/tgartner/Software-deepmd-kit-1.0/lammps-3Mar20/src/lmp_mpi -i in.lammps.init
rm in.boxdimensions
python BoxDimensions.py > in.boxdimensions
mpirun /home/tgartner/Software-deepmd-kit-1.0/lammps-3Mar20/src/lmp_mpi -i in.lammps.equil

if ! grep -q 'ERROR' slurm*; then
    echo "Continuing equilibration"
    sbatch --dependency=afterok:$SLURM_JOB_ID run.sample.qs
else
    echo "There is an error"
fi

