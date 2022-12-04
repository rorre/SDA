# $RUNCMD = "python tp06.py"
$RUNCMD = ".\6.exe"

New-Item -Path 'tc/out2' -ItemType Directory
for ($i = 0; $i -le 50; $i++) {
    Write-Host -NoNewline "Running ${i}... "
    Write-Output (Measure-Command { Invoke-Expression " Get-Content tc/in/in$i.txt | $RUNCMD > tc/out2/out$i.txt" }).TotalMilliseconds
}