$WshShell = New-Object -ComObject WScript.Shell
$target = Join-Path $PSScriptRoot "related\Close all.bat"
$shortcutPath = Join-Path $PSScriptRoot "Close all.lnk"

$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $target
$shortcut.WorkingDirectory = Split-Path $target
$shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,1"
$shortcut.Save()
Write-Output "Ярлык создан: $shortcutPath"