powershell -ExecutionPolicy Bypass -File "%~dp0related/CreateShortcut.ps1"
Start "" "%~dp0related\Configs\DH1_Speedrun.xmbcp"
Start "" "%~dp0related\Start_D1_Speedrun.exe"
move "%~dp0D1_Install.exe" "%~dp0related"
ren "%~dp0related\CreateShortcut.ps1" "CreateShortcutOFF.ps1"

