base_directory=`pwd`
for file in `find . -name "*plumed*"`
do
        folder=${file%/*}
	onlyfilename=$(basename $file)
	echo $file
        cd $folder
	plumed --no-mpi driver --natoms 100000 --parse-only --kt 2.49 --plumed $onlyfilename > /dev/null; echo $?
	rm COLVAR* DELTAFS
        cd $base_directory
	read -p "Press any key to continue... " -n1 -s
done

