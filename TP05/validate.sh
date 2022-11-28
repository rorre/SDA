mkdir -p tc/out

for i in {0..4}
do
    echo "Running $i"
    cat tc/in/in$i.txt | python tp05.py > tc/out/out$i.txt
done
