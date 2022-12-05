mkdir -p tc/out2

for i in {0..50}
do
    echo "Running $i"
    time (cat tc/in/in$i.txt | python tp06.py > tc/out2/out$i.txt)
done
