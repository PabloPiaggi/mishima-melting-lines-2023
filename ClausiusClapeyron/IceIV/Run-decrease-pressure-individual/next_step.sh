if [ -d "step.0" ]
then	
	n=$(find . -type d -name 'step*' | sed 's|^\./step.||' | sort -n | tail -n 1)
	newn=$(($n+1))
else
	newn=0
fi

cp -r step-base step.${newn}

echo "New RK step in folder step.${newn}"

