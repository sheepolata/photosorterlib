; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Photo Sorter"
#define MyAppVersion "0.2"
#define MyAppPublisher "Sheepolata"
#define MyAppURL "https://github.com/sheepolata/photosorterlib"
#define MyAppExeName "Photo Sorter.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{62083434-415B-4510-866F-EA4B06FC96A6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputBaseFilename=photosorter_installer_v0.2
SetupIconFile=D:\Developpement\Git\photosorterlib\data\tri.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "D:\Developpement\Git\photosorterlib\build\exe.win-amd64-3.10\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Developpement\Git\photosorterlib\build\exe.win-amd64-3.10\python3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Developpement\Git\photosorterlib\build\exe.win-amd64-3.10\python310.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Developpement\Git\photosorterlib\build\exe.win-amd64-3.10\lib\*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

