[Setup]
AppName=FinancePy
AppVersion=1.0
DefaultDirName={pf}\FinancePy
DefaultGroupName=FinancePy
OutputDir=installer
OutputBaseFilename=FinancePy_Setup
SetupIconFile=financepy.ico

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\FinancePy"; Filename: "{app}\main.exe"
Name: "{commondesktop}\FinancePy"; Filename: "{app}\main.exe"
