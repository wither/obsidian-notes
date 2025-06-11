# Active Directory PowerShell Module Commands
---

List specific information about the domain:
```powershell
Get-ADDomain | Select-Object NetBIOSName, DNSRoot, InfrastructureMaster
```

List all domains within the forest:
```powershell
Get-ADForest | Select-Object Domains
```

Pull specific information about trusts on the domain:
```powershell
Get-ADTrust -Filter * | Select-Object Direction,Source,Target
```




