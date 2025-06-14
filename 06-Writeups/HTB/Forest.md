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

| Port | Service | Version |
|------|---------|---------|
| 53 | domain | Simple DNS Plus |
| 88 | kerberos-sec | Microsoft Windows Kerberos |
| 135 | msrpc | Microsoft Windows RPC |
| 139 | netbios-ssn | Microsoft Windows netbios-ssn |
| 389 | ldap | Microsoft Windows Active Directory LDAP |
| 445 | microsoft-ds | Windows Server 2016 Standard 14393 microsoft-ds |
| 464 | kpasswd5 | N/A |
| 593 | ncacn_http | Microsoft Windows RPC over HTTP 1.0 |
| 636 | tcpwrapped | N/A |
| 3268 | ldap | Microsoft Windows Active Directory LDAP |
| 3269 | tcpwrapped | N/A |
| 5985 | http | Microsoft HTTPAPI httpd 2.0 |

## Enumeration

Generated and appended a hosts file to `/etc/hosts` to avoid possible DNS issues later on with Kerberos.
```bash
nxc smb '10.10.10.161' --generate-hosts-file files/hosts && sudo tee -a /etc/hosts < files/hosts
```

Enumerated the domain users.
```bash
nxc ldap 'FOREST' -u '' -p '' -d htb.local --users-export files/users.txt
```



## Exploitation

### Initial Access

### User Flag

## Privilege Escalation

### Enumeration

### Escalation

### Root Flag

## References

---
#forest #htb #easy #windows