mkdir -p tc/outputuser

for i in {000..119}
do
    echo "Running $i"
    cat tc/input/input$i.txt | python tp03.py > tc/outputuser/output$i.txt &
done
