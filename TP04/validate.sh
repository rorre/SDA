mkdir -p tc2/out

for i in {0..99}
do
    echo "Running $i"
    cat tc2/in/$i.txt | python tp04.py > tc2/myout/$i.txt
done
