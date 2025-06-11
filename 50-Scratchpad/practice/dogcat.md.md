# dogcat
![[Pasted image 20220510192913.png]]

# flag 1

## Nmap
It's running an Apache webserver, lets check it out
![[Pasted image 20220510193114.png]]

You press a button and either a dog or cat is displayed with the parameter in the URL.
![[Pasted image 20220510193337.png]]

But, it only allows us to access cats or dogs
![[Pasted image 20220510195130.png]]

However, we can use php filter bypasses such as b64 encoding to get around this:
![[Pasted image 20220510195329.png]]

As you can see, by decoding the base64 we get the raw index.php code. As you can see in the code, the "**ext**" variable can be set, meaning we could in theory read any file of any extension. Lets try read /etc/passwd
![[Pasted image 20220510195656.png]]

![[Pasted image 20220510200120.png]]

Using the same method, we can access the apache2 log files
![[Pasted image 20220510203504.png]]

capture and send the request in burpsuite
![[Pasted image 20220512135852.png]]

rci using the php in the user agent
![[Pasted image 20220512143116.png]]

Execute a remote shell using the same technique:
![[Pasted image 20220512144107.png]]

Get shell!
![[Pasted image 20220512144152.png]]

Get Flag1
![[Pasted image 20220512144333.png]]

## Flag 2

Get flag2
![[Pasted image 20220512144601.png]]

## Flag 3

Use sudo -l to list all programs that we can run as root, and use env to get a bash shell
![[Pasted image 20220512145051.png]]

we are root!
![[Pasted image 20220512145136.png]]

get flag3
![[Pasted image 20220512145232.png]]

## Flag 4

Using cat/proc/1/cgroup we can see that we are in a docker container
![[Pasted image 20220512145448.png]]

in the /opt/backups folder,backup.sh is being backed up every minute
![[Pasted image 20220512145657.png]]

we can overwrite backup.sh to get a reverse shell
![[Pasted image 20220512145906.png]]

Append the reverse shell onto the file and wait for it to execute to get a shell
![[Pasted image 20220512151632.png]]

get flag4!
![[Pasted image 20220512151733.png]]
