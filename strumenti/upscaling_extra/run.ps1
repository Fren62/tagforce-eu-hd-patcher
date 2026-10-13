param([string]$V,[int]$Secs=70,[int]$Step=3,[string[]]$Keys=@())
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;using System.Runtime.InteropServices;
public class W{[DllImport("user32.dll")]public static extern bool GetWindowRect(IntPtr h,out R r);
[DllImport("user32.dll")]public static extern bool SetForegroundWindow(IntPtr h);
[DllImport("user32.dll")]public static extern bool PostMessage(IntPtr h,uint m,IntPtr w,IntPtr l);
[DllImport("user32.dll")]public static extern void keybd_event(byte vk,byte sc,uint f,UIntPtr e);
[DllImport("user32.dll")]public static extern uint MapVirtualKey(uint c,uint t);
public static void Key(int vk){byte sc=(byte)MapVirtualKey((uint)vk,0);keybd_event((byte)vk,sc,(uint)(vk>=0x25&&vk<=0x28?1:0),UIntPtr.Zero);System.Threading.Thread.Sleep(150);keybd_event((byte)vk,sc,(uint)(vk>=0x25&&vk<=0x28?3:2),UIntPtr.Zero);}
public static void Front(IntPtr h){keybd_event(0x12,0,0,UIntPtr.Zero);SetForegroundWindow(h);keybd_event(0x12,0,2,UIntPtr.Zero);}
public struct R{public int L,T,Rt,B;}}
"@
$T=$env:TEMP;$P="$T\pp";$tex="$P\memstick\PSP\TEXTURES\ULES00600"
Get-Process PPSSPPWindows64 -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item "$tex\*" -Recurse -Force -ErrorAction SilentlyContinue
$shader = if($V -eq 'brz'){'Tex4xBRZ'}else{'Off'}
(Get-Content "$P\cfg.tpl" -Raw) -replace '%s',$shader | Set-Content "$P\memstick\PSP\SYSTEM\ppsspp.ini"
if(Test-Path "$P\packs\$V"){Copy-Item "$P\packs\$V\*" $tex}
$out="$T\shots\$V";Remove-Item $out -Recurse -Force -ErrorAction SilentlyContinue;New-Item -ItemType Directory $out|Out-Null
$iso="F:\Progetti\Mods\Yu-Gi-Oh! Tag Force\Tag Force Versione Pomodoro Mistico\PSP\GAME\ULES00600_YuGiOh_GX_TagForce_EUR.iso"
$p=Start-Process "$P\PPSSPPWindows64.exe" -ArgumentList "`"$iso`"" -WorkingDirectory $P -PassThru
for($i=0;$i -lt $Secs/$Step;$i++){
  Start-Sleep $Step
  $t=$i*$Step
  foreach($k in $Keys){$a=$k.Split('|');if([int]$a[0] -eq $t){$p.Refresh();[W]::Front($p.MainWindowHandle);Start-Sleep -m 400;foreach($c in $a[1].Split(',')){[W]::Key([Convert]::ToInt32($c,16));Start-Sleep -m 350}}}
  $p.Refresh();$h=$p.MainWindowHandle
  if($h -eq 0){continue}
  $r=New-Object W+R;[W]::GetWindowRect($h,[ref]$r)|Out-Null
  $w=$r.Rt-$r.L;$ht=$r.B-$r.T
  $bmp=New-Object Drawing.Bitmap $w,$ht
  [Drawing.Graphics]::FromImage($bmp).CopyFromScreen($r.L,$r.T,0,0,$bmp.Size)
  $bmp.Save(("{0}\{1:000}.png" -f $out,($i*$Step)));$bmp.Dispose()
}
Stop-Process $p -Force -ErrorAction SilentlyContinue
