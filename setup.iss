; Inno Setup Script pour Meeting & Project Manager AI
; Génération d'un installateur Windows

[Setup]
AppId={{A1B2C3D4-E5F6-7890-GHIJ-KLMNOPQRSTUV}
AppName=Meeting & Project Manager AI
AppVersion=1.0.0
AppPublisher=Votre Société
AppContact=contact@votresociete.com
AppSupportURL=https://votresociete.com/support
AppUpdatesURL=https://votresociete.com/updates
DefaultDirName={autopf}\MeetingManager
DefaultGroupName=Meeting Manager
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=dist\installer
OutputBaseFilename=MeetingManager-Setup-1.0.0
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\MeetingManager.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Languages\English.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\MeetingManager\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Meeting Manager"; Filename: "{app}\MeetingManager.exe"
Name: "{autodesktop}\Meeting Manager"; Filename: "{app}\MeetingManager.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Meeting Manager"; Filename: "{app}\MeetingManager.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\MeetingManager.exe"; Description: "{cm:LaunchProgram,Meeting & Project Manager AI}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  // Vérifications préalables si nécessaire
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Actions post-installation
  end;
end;
