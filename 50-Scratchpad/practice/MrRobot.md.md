# Mr Robot CTF
![[Pasted image 20220510142049.png]]
# Key 1
## NMap

![[Pasted image 20220510143823.png]]

Web server is running, lets check it out.

![[Pasted image 20220510144631.png]]

## ffuf
Seems to be a shell/terminal application. Let's scan for files and directories using ffuf.

![[Pasted image 20220510153609.png]]

We get this:

```bash
.hta
.htaccess-marco
.htaccess-dev
.htaccess.save
.htpasswd_test
.ht_wsr.txt
.htaccess.orig
login
templates/rhuk_milkyway/index.php
.htgroup
bitrix/admin/index.php
phpmyadmin/scripts/setup.php
.htaccess.bak
.htusers
sql/index.php
templates/beez/index.php
.htpasswds
.htaccess.bak1
wp-content/uploads/
pma/index.php
.htaccessold
wp-register.php
.htaccessold2
.htaccess_sc
.htaccess.sample
templates/ja-helio-farsi/index.php
wp-content/plugins/akismet/akismet.php
tmp/index.php
.htaccess~
.htaccess
.htaccess.old
.htpasswd
wp-content/plugins/akismet/admin.php
.htpasswd-old
.htaccess-local
.htaccess_orig
.htaccessbak
myadmin/index.php
admin/.htaccess
apc/index.php
wp-admin/setup-config.php
.user.ini
.htaccess.txt
.htaccess_extra
phpmyadmin/
```

Notably, ffuf discovered **robots.txt**, which given the name of the CTF, I think the correct priority here.

![[Pasted image 20220510153944.png]]

As you can see, there seems to be a reference to the first key hidden in a text file.

# Key 2

For this key, I'll be focussing my attention on the wordpress login form that we found when fuzzing ('/**login**').
![[Pasted image 20220510160316.png]]

## WPScan
First, we need to get the login. I'm going to use the dictionary file referred to in the robots .txt file ('**fsocity.dic**') to find the username. But it has some duplicates, so I need to remove those:
![[Pasted image 20220510182207.png]]

We found **Elliott**, now to find his password. I'm going to use the same dictionary to attack the password field.
![[Pasted image 20220510183114.png]]

Found it!
![[Pasted image 20220510182403.png]]

## Reverse Shell
Now that we've logged in, as you can see here, in the dashboard we are able to edit php files, thus allowing us to upload and run a reverse shell.
![[Pasted image 20220510185052.png]]

Open a netcat listener
![[Pasted image 20220510185330.png]]

Run the compromised file
![[Pasted image 20220510185427.png]]

Get and upgrade shell
![[Pasted image 20220510185536.png]]

get key #2
![[Pasted image 20220510185702.png]]

we can't!
![[Pasted image 20220510185826.png]]

we need to escalate our privelages to root.

# PrivEsc
Search for setuid binaries:
![[Pasted image 20220510191455.png]]

We're going to abuse the nmap binary to get root
![[Pasted image 20220510191848.png]]

## Keys 2 and 3

We can now read key2
![[Pasted image 20220510192012.png]]

And key3
![[Pasted image 20220510192241.png]]

## Complete!
![[Pasted image 20220510192517.png]]


