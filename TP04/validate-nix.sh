mkdir -p tc/outputuser

for i in {0..199}
do
    echo "Running $i"
    python tp04.py < tc/in/$i.txt > tc/out/$i.txt
done
