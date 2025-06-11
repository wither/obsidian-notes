# Wonderland
![[Pasted image 20220515210809.png]]

# Enumeration

### Nmap

![[Pasted image 20220515211030.png]]

ssh could be bf'd, influxdb backend, golang?
http-server website:

![[Pasted image 20220515212557.png]]

### fuff
![[Pasted image 20220515212119.png]]
found a folder tree called /r/a/b/b/i/t, leads to:

![[Pasted image 20220515212411.png]]

In the source of this page, theres a hidden message:
"alice:HowDothTheLittleCrocodileImproveHisShiningTail"
These could be ssh credentials?

![[Pasted image 20220515213212.png]]

### User
They are!

![[Pasted image 20220515213537.png]]

### Privilege Escalation

rabbit can run the python script found in the home directory as root
the script uses the random module, create our own random.py to import

![[Pasted image 20220515225105.png]]

### User 2

now the rabbit user

![[Pasted image 20220515225248.png]]

theres a binary called teaparty in rabbits home directory

![[Pasted image 20220515225412.png]]

get this when ran

![[Pasted image 20220515225749.png]]

download teaparty using netcat

![[Pasted image 20220515230254.png]]
![[Pasted image 20220515230218.png]]

using strings we can see the source, it uses 'date' using a path variable maybe its overwritable

![[Pasted image 20220515230433.png]]

### User 3
make a new directory in rabbits home, make a file called date and add the directory to the PATH variable, so that when 'date' is called in teaParty, it executes the file instead

![[Pasted image 20220515233145.png]]

### Root

hatters password is in their home directory

![[Pasted image 20220515233850.png]]

Using getcap we can list binaries with capabilities set, these can be exploited

![[Pasted image 20220515234014.png]]

after switching to the hatter user, using gtfobins' perl capabilities line we can get root

![[Pasted image 20220515234828.png]]

### Flags!

get em

![[Pasted image 20220515235049.png]]
