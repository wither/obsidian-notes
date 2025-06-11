# Powerview 3.0 Commands
---
List all operating systems on the domain:
```powershell
Get-NetComputer -fulldata | select operatingsystem
```

List all users on the domain:
```powershell
Get-NetUser | select cn
```

List domain groups:
```powershell
Get-NetGroup -GroupName *
```

List basic information about the domain:
```powershell
Get-NetDomain
```

List all domain controllers on the network:
```powershell
Get-NetDomainController
```

List domains on the forest:
```powershell
Get-NetForest
```

List domain trusts:
```powershell
Get-NetDomainTrust
```


