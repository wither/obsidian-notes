---
Title: Firewall IDS and IPS Evasion with Nmap
Folders:
  - "[[Nmap]]"
---
# Firewall IDS and IPS Evasion with Nmap
---

### Scan using decoy IP addresses

To avoid your IP getting blocked by an administrator

```bash
sudo nmap $IP -p 80 -sS -Pn -n --disable-arp-ping --packet-trace -D RND:5
```

### Scan using a different source IP

You must specify the interface

```bash
sudo nmap $IP -n -Pn -p 445 -O -S $SOURCE -e tun0
```

### DNS Proxy

You can change the source port to 53 to emulate legitimate DNS lookups and bypass the firewall.

```bash
sudo nmap $IP -p5000 -sS -Pn -n --disable-arp-ping --source-port 53
```

### Connect to a Filtered port with Netcat

After testing that the firewall accepts TCP port 53, you can attempt to connect to the port with netcat

```bash
ncat -nv --source-port 53 $IP $PORT
```

### Quietly scan for OS details

This could provide information about the operating system from common services like an Apache web server that will leak the OS of the target.

```bash
sudo nmap 10.129.187.247 -Pn -O --disable-arp-ping -n -top-ports=10 -sV
```

### Evade Firewall and quietly scan for DNS version

Maybe a bit overkill to use CloudFlare as a DNS server but it works

```bash
sudo nmap 10.129.25.173 -Pn --disable-arp-ping -n -p53 -sV -sU -dns-server 1.1.1.1 -source-port 53
```
