#!/bin/bash
# Script to run psipred with multiple core
# If the result is present, skip that search
# 2016/07/11

inputDir='fasta'
outDir='psipred'
cpuNo=4

if [ ! -d "$outDir" ]; then
        mkdir $outDir
else
        echo "${outDir} exists. Continue in 2s anyway ..!"
        sleep 2s;
fi

count=0

for i in ${inputDir}/*.fasta;
do
        foo=${i#${inputDir}/}
        foo=${foo/.fasta}
        if [ ! -e "${outDir}/${foo}.horiz" ]; then 
                runpsipredplus $i &

                let count=$count+1        
                if [ "$count" -eq "$cpuNo" ]; then
                        wait
                        count=0
                fi

        else
                echo "Skip ${foo}"
        fi
done

# Move result to outDir
mv *.horiz $outDir
