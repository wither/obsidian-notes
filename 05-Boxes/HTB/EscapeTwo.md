---
target_ip: 10.10.11.51
platform: HTB
difficulty: Easy
os: Windows
date_started: 2025-06-15
status: in_progress
services: ['ncacn_http', 'microsoft-ds', 'kpasswd5', 'domain', 'http', 'kerberos-sec', 'msrpc', 'netbios-ssn', 'ldap', 'ms-sql-s']
techniques_used: []
tools_used: [nmap]
---

# EscapeTwo

**Platform:** HTB | **Difficulty:** Easy | **OS:** Windows | **Date:** 15/06/2025

## Overview 


---

## Phase 1: Reconnaissance 

### Network Discovery

```bash
nmap -sC -sV -T4 10.10.11.51 -oA nmap/escapetwo
```

| Port | Service      | Version                                      |
| ---- | ------------ | -------------------------------------------- |
| 53   | domain       | Simple DNS Plus                              |
| 88   | kerberos-sec | Microsoft Windows Kerberos                   |
| 135  | msrpc        | Microsoft Windows RPC                        |
| 139  | netbios-ssn  | Microsoft Windows netbios-ssn                |
| 389  | ldap         | Microsoft Windows Active Directory LDAP      |
| 445  | microsoft-ds | N/A                                          |
| 464  | kpasswd5     | N/A                                          |
| 593  | ncacn_http   | Microsoft Windows RPC over HTTP 1.0          |
| 636  | ldap         | Microsoft Windows Active Directory LDAP      |
| 1433 | ms-sql-s     | Microsoft SQL Server 2019 15.00.2000.00; RTM |
| 3268 | ldap         | Microsoft Windows Active Directory LDAP      |
| 3269 | ldap         | Microsoft Windows Active Directory LDAP      |
| 5985 | http         | Microsoft HTTPAPI httpd 2.0                  |
hosts
```bash
nxc smb '10.10.11.51' --generate-hosts-file files/hosts && sudo tee -a /etc/hosts < files/hosts

...
10.10.11.51     DC01.sequel.htb DC01
```










## Enumeration

---

## Phase 2: Exploitation


---

## Phase 3: Privilege Escalation



## References
- 

---
#escapetwo #htb #easy #windows