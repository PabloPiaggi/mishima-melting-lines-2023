temp=$1
press=$2

echo $temp $press
cp -r BASE IceIV-${temp}.0-${press}.0
cd IceIV-${temp}.0-${press}.0
sed -i "s/TEMP/$temp/g" in.temp
sed -i "s/PRESS/$press/g" in.pressure
sed -i "s/SEED/$RANDOM/g" in.seed
sed -i "s/TEMP/$temp/g" job.sh
sed -i "s/PRESS/$press/g" job.sh
sed -i "s/TEMPX/$temp/g" plumed.dat
sbatch < job.sh
