mkdir -p tc/out

for i in {0..100}
do
    echo "Running $i"
    time (cat tc/in/in$i.txt | python tp06.py > tc/out/out$i.txt)
    echo "-------------"
done
