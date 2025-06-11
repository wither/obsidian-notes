```
Nmap scan report for 10.200.29.219

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
```
Nmap scan report for 10.200.29.138

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
```
Nmap scan report for 10.200.29.232

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
```
Nmap scan report for 10.200.29.147

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 826a0e59326e23ceef921201abf5e1e0 (RSA)
|   256 91184486e26f3bb00ef95a7fdad24441 (ECDSA)
|_  256 da0a7ff5d8156c99cb35940e15a2f4ac (ED25519)
1337/tcp open  http    Node.js Express framework
|_http-title: Error
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
