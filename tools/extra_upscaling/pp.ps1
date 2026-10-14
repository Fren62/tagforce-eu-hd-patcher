param([string]$A,[string]$V='orig',[string]$Arg='')
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;using System.Runtime.InteropServices;
public class W{[DllImport("user32.dll")]public static extern bool GetWindowRect(IntPtr h,out R r);
[DllImport("user32.dll")]public static extern bool SetForegroundWindow(IntPtr h);
[DllImport("user32.dll")]public static extern bool SetCursorPos(int x,int y);
[DllImport("user32.dll")]public static extern void keybd_event(byte vk,byte sc,uint f,UIntPtr e);
[DllImport("user32.dll")]public static extern uint MapVirtualKey(uint c,uint t);
public static void Key(int vk,int ms){byte sc=(byte)MapVirtualKey((uint)vk,0);uint ex=(uint)(vk>=0x25&&vk<=0x28?1:0);keybd_event((byte)vk,sc,ex,UIntPtr.Zero);System.Threading.Thread.Sleep(ms);keybd_event((byte)vk,sc,ex|2,UIntPtr.Zero);}
[DllImport("user32.dll")]public static extern IntPtr GetForegroundWindow();
public static void Front(IntPtr h){if(GetForegroundWindow()==h)return;Key(0x12,60);SetForegroundWindow(h);System.Threading.Thread.Sleep(300);Key(0x12,60);System.Threading.Thread.Sleep(300);}
[DllImport("user32.dll")]public static extern void mouse_event(uint f,int dx,int dy,uint d,UIntPtr e);
public static void Click(int x,int y,int ms){SetCursorPos(x,y);System.Threading.Thread.Sleep(80);mouse_event(2,0,0,0,UIntPtr.Zero);System.Threading.Thread.Sleep(ms);mouse_event(4,0,0,0,UIntPtr.Zero);}
public struct R{public int L,T,Rt,B;}}
"@
$T=$env:TEMP;$P="$T\pp";$tex="$P\memstick\PSP\TEXTURES\ULES00600"
function Proc{Get-Process PPSSPPWindows64 -ErrorAction SilentlyContinue|Select -First 1}
[W]::SetCursorPos(2550,1430)|Out-Null
switch($A){
'start'{
  Get-Process PPSSPPWindows64 -ErrorAction SilentlyContinue|Stop-Process -Force; Start-Sleep 1
  Remove-Item "$tex\*" -Recurse -Force -ErrorAction SilentlyContinue
  $sh=if($V -match 'brz'){'Tex4xBRZ'}else{'Off'}
  $rf="$P\res.txt"; $rs=if(Test-Path $rf){(Get-Content $rf).Trim()}else{'4'}
  $sv=if($V -eq 'dump'){'True'}else{'False'}
  (Get-Content "$P\cfg.tpl" -Raw) -replace '%s',$sh -replace '%d',$sv -replace '%r',$rs | Set-Content "$P\memstick\PSP\SYSTEM\ppsspp.ini"
  if(Test-Path "$P\packs\$V"){Copy-Item "$P\packs\$V\*" $tex -Recurse}
  $iso=$env:TF1_ISO   # path of the European ISO (ULES00600), set by the caller
  Start-Process "$P\PPSSPPWindows64.exe" -ArgumentList "`"$iso`"" -WorkingDirectory $P; "started"}
'key'{ # Arg = "hex[:ms],hex[:ms],..."  (350 ms pause between keys)
  $p=Proc;[W]::Key(0x12,60);Start-Sleep -m 300;[W]::SetForegroundWindow($p.MainWindowHandle)|Out-Null;[W]::Key(0x12,60);Start-Sleep -m 400
  foreach($c in $Arg.Split(',')){$a=$c.Split(':');$ms=if($a.Count -gt 1){[int]$a[1]}else{150};[W]::Key([Convert]::ToInt32($a[0],16),$ms);Start-Sleep -m 350}}
'shot'{ # Arg = file name
  $p=Proc;$p.Refresh();$h=$p.MainWindowHandle;$r=New-Object W+R;[W]::GetWindowRect($h,[ref]$r)|Out-Null
  $w=$r.Rt-$r.L;$ht=$r.B-$r.T;$b=New-Object Drawing.Bitmap $w,$ht
  [Drawing.Graphics]::FromImage($b).CopyFromScreen($r.L,$r.T,0,0,$b.Size)
  $d="$T\shots\$V";New-Item -ItemType Directory -Force $d|Out-Null;$b.Save("$d\$Arg.png");$b.Dispose();"$d\$Arg.png"}
'click'{ # Arg = "x:y[:ms]" relative to the window corner
  $p=Proc;$p.Refresh();$r=New-Object W+R;[W]::GetWindowRect($p.MainWindowHandle,[ref]$r)|Out-Null
  $a=$Arg.Split(':');$ms=if($a.Count -gt 2){[int]$a[2]}else{150};[W]::Click($r.L+[int]$a[0],$r.T+[int]$a[1],$ms);[W]::SetCursorPos(2550,1430)|Out-Null}
'alt'{$p=Proc;[W]::Key(0x12,60);Start-Sleep -m 300}
'stop'{Get-Process PPSSPPWindows64 -ErrorAction SilentlyContinue|Stop-Process -Force}
}

