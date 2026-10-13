param([string[]]$Variants,[string]$File="replay.txt")
$D="$env:TEMP\vigem"
$lines=Get-Content "$D\$File"
foreach($v in $Variants){
  Set-Content "$D\cmd.txt" "" ; Remove-Item "$D\log.txt" -ea 0
  # il daemon tiene un puntatore di riga: lo riavvio per ogni variante
  Get-CimInstance Win32_Process -Filter "Name='python.exe'" | ? CommandLine -match 'pad.py' | % { Stop-Process -Id $_.ProcessId -Force }
  Start-Sleep 1; Start-Process python -ArgumentList "$D\pad.py" -WindowStyle Hidden; Start-Sleep 5
  & "$env:TEMP\pp.ps1" -A start -V $v | Out-Null; Start-Sleep 14
  ($lines -replace ' V$'," $v") | Add-Content "$D\cmd.txt"
  $n=$lines.Count
  while($true){ Start-Sleep 5; $l=Get-Content "$D\log.txt" -ea 0; if($l -and [int]($l -replace 'done ','') -ge $n){break} }
  "$v finito"
}
Get-Process PPSSPPWindows64 -ea 0 | Stop-Process -Force
