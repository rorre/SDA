mkdir -p tc/outputuser

for i in {0..199}
do
    echo "Running $i"
    python tp04.py < tc2/in/$i.txt > tc2/out/$i.txt
done
