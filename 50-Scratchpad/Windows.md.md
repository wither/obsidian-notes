# Windows Privilege Escalation

### Winpeas

Usage
```Shell
winpeas.exe > outputfile.txt
```

### PowerUp

Launch powershell, bypassing execution policy restrictions
```shell
powershell.exe -nop -exec bypass
```

Usage
```Shell
PowerUp.ps1 Invoke-PrivescAudit
```

### Windows Exploit Suggester

Update exploit database
```Shell
windows-exploit-suggester.py –update
```

Output systeminfo to file to use
```Shell
systeminfo > sysinfo_output.txt
```

Usage
```Shell
windows-exploit-suggester.py --database 2021-09-21-mssb.xls --systeminfo sysinfo_output.txt
```

### Metasploit

if you already have meterpreter shell
```Shell
use multi/recon/local_exploit_suggester
```
