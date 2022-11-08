mkdir -p tc/outputuser

for i in {000..094}
do
    echo "Running $i"
    python tp03.py < tc/input/input$i.txt > tc/outputuser/output$i.txt
done
