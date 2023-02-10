temp=$1
press=$2

echo $temp $press
cp -r BASE IceXIII-${temp}.0-${press}.0
cd IceXIII-${temp}.0-${press}.0
sed -i "s/TEMP/$temp/g" in.thermosettings
sed -i "s/PRESS/$press/g" in.thermosettings
sed -i "s/SEED/$RANDOM/g" in.thermosettings
sed -i "s/TEMP/$temp/g" run.init.qs
sed -i "s/PRESS/$press/g" run.init.qs
sbatch < run.init.qs
