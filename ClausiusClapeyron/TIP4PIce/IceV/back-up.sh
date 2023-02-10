if [ -d "bck.0" ]
then	
	n=$(find . -type d -name 'bck*' | sed 's|^\./bck.||' | sort -n | tail -n 1)
	newn=$(($n+1))
else
	newn=0
fi

mkdir bck.${newn}
cp * bck.${newn}
cp -r phase* bck.${newn}

echo "Files backed up to bck.${newn}"

