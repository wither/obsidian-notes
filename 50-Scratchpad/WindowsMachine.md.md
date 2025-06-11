# Windows Enumeration

### Users

Show current user's privileges
```Shell
whoami /priv
```

List all users
```Shell
net users
```

List details about a user
```Shell
net user username
```

View all currently logged in users
```Shell
query session
```

### Groups

List all usergroups
```Shell
net localgroup
```

List members of a specific usergroup
```Shell
net localgroup groupname
```

### System

Get detailed information about the system
```Shell
systeminfo
```

Grep specific system information
```Shell
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
```

Search for specific files
```Shell
findstr /si password *.txt
```

Get patch level
```Shell
wmic qfe get Caption,Description,HotFixID,InstalledOn
```

### Network

List all open ports
```Shell
netstat -ano
```

### Scheduled Tasks

List all scheduled tasks
```Shell
schtasks /query /fo LIST /v
```

### Drivers

List installed drivers
```Shell
driverquery
```

### Windows Defender

Get Windows Defender service name
```Shell
wmic service get name,displayname,pathname,startmode | findstr "Defender"
```

Get state of Windows Defender
```Shell
sc query windefend
```

