#!/bin/sh
#!/bin/bash

cp ../local_test_data/EmailEnron input.txt
#cp ../local_test_data/GNPn100p05 input.txt

for i in {1..50}
do
./pagerank_map.py < input.txt | sort -k 1,1 | ./pagerank_reduce.py | ./process_map.py | sort -n -k 1,1 | ./process_reduce.py > output.txt

echo "$i"
grep Final output.txt


if [ $? -eq 0 ]; then
exit
fi
cp output.txt input.txt
done
