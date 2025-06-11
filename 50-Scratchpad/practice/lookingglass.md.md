# Looking Glass

![[Pasted image 20220516132748.png]]

## Enumeration

### Nmap

![[Pasted image 20220516142933.png]]

ssh open from port 9000 to 13999

![[Pasted image 20220516143110.png]]

13999 says "higher"

![[Pasted image 20220516143147.png]]

9000 says "lower"
somewhere in between?

![[Pasted image 20220516143533.png]]

port 12330 reveals a secret message

![[Pasted image 20220516151034.png]]

decrypting that message using decrypt.fr's vinegere decryptor gives us the secret

## User
![[Pasted image 20220516151323.png]]

entering the secret gives us the user ssh login

CalculationBeautifullyRespectableNearly

## Flag 1

![[Pasted image 20220516152305.png]]


## Privilege Escalation

![[Pasted image 20220516155901.png]]

a bash file runs as root on reboot

![[Pasted image 20220516155945.png]]

jabberwock can run sudo reboot

![[Pasted image 20220516161615.png]]

edit the twasBrillig.sh file to spawn a reverse shell and reboot



