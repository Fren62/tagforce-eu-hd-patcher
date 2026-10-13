param([string[]]$L,[string]$Shot)
$D="$env:TEMP\vigem"; $f="$env:TEMP\shots\dump\$Shot.png"; Remove-Item $f -ea 0
Add-Content "$D\cmd.txt" ($L + "shot $Shot dump")
$t=0; while(-not (Test-Path $f) -and $t -lt 100){ Start-Sleep 1; $t++ }; Start-Sleep 1
