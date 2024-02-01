DIR="$1"
PAPER="$3"
MAX="${4:-0.05}"
OVERRIDE="${5:-0}"
COVFEFE="${6:-1}"

echo "USING MAX DISTANCE OF $MAX"

run_command () {
    echo $2
    if [[ -s $1 ]] && [ $OVERRIDE -ne "1" ]; then
        echo "$1 already exists"
    else    
        eval $2    
    fi
}

INPUT=${DIR}/sequence.fasta

run_command ${DIR}/sequence.bam "bealign -r $2 -m HIV_BETWEEN_F ${DIR}/sequence.fasta ${DIR}/sequence.bam"
run_command ${DIR}/sequence.msa "bam2msa ${DIR}/sequence.bam ${DIR}/sequence.msa"
run_command ${DIR}/tn93.json "tn93 -t $MAX -q -a RMYSKB -o ${DIR}/tn93.csv ${DIR}/sequence.msa > ${DIR}/tn93.json"
#run_command ${DIR}/tn93.json "tn93 -t $MAX -q -o ${DIR}/tn93.csv ${DIR}/sequence.msa > ${DIR}/tn93.json"


echo "Mean distance"
jq '.["Mean distance"]' ${DIR}/tn93.json

hivnetworkcsv -f plain -i ${DIR}/tn93.csv  -A 0 > ${DIR}/autotune.tsv
read F1 F2 F3 F4 F5 F6 F7 <<< $(sort -g -r  -k 7 ${DIR}/autotune.tsv | head -n 1)
echo "AUTO-TUNE D = $F1, SCORE $F7"

echo ""
echo "AUTOTUNE THRESHOLD"
echo ""

hivnetworkcsv -f plain -i ${DIR}/tn93.csv  -t $F1  

echo ""
echo "PUBLISHED THRESHOLD"
echo ""

hivnetworkcsv -f plain -i ${DIR}/tn93.csv  -t $3 

echo ""
echo ""
if [ $COVFEFE -eq "1" ]; then
    hivnetworkcsv -f plain -i ${DIR}/tn93.csv  -t $F1 -n remove -s ${DIR}/sequence.msa -l -J -O ${DIR}/network-autotune.json
    hivnetworkcsv -f plain -i ${DIR}/tn93.csv  -t $3 -n remove -s ${DIR}/sequence.msa -l -J -O ${DIR}/network-paper.json
else
    hivnetworkcsv -f plain -i ${DIR}/tn93.csv  -t $F1 -J -O ${DIR}/network-autotune.json
    hivnetworkcsv -f plain -i ${DIR}/tn93.csv  -t $3  -J -O ${DIR}/network-paper.json
fi

if (( $(echo "$3 > $F1" |bc -l) )); then 
    python3 inject-annotation.py -c ${DIR}/network-autotune.json -r ${DIR}/network-paper.json -f ${DIR}/sequence.msa -t ${DIR}/sequence.msa > ${DIR}/network-contrast.json
    # published threshold is LARGER than AUTO-TUNE
else
    python3 inject-annotation.py -r ${DIR}/network-autotune.json -c ${DIR}/network-paper.json -f ${DIR}/sequence.msa -t ${DIR}/sequence.msa > ${DIR}/network-contrast.json
    # published threshold is SMALLER than AUTO-TUNE
fi

#python3 compare-degrees.py -p ${DIR}/network-paper.json -a ${DIR}/network-autotune.json > ${DIR}/degrees.csv