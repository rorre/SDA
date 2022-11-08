mkdir -p tc/outputuser

for i in {0..99}
do
    echo "Running $i"
    python tp04.py < in/$i.txt > out/$i.txt
done
