---
Title: Host Discovery with Nmap
Folders:
  - "[[Nmap]]"
---
# Host Discovery with Nmap
---

Discover hosts on a specific subnet 

```bash
sudo nmap $IP -sn -oA $OUTFILE | grep for | cut -d" " -f5
```

Scan a list of IPs

```bash
sudo nmap -sn -oA $OUTFILE -iL $FILE | grep for | cut -d" " -f5
```

Scan multiple IPs

```bash
sudo nmap -sn -oA $OUTFILE $IP1 $IP2 $IP3 | grep for | cut -d" " -f5
```

Scan a range of IPs in the same subnet

```bash
sudo nmap -sn -oA $OUTFILE 10.0.1.18-20 | grep for | cut -d" " -f5
```

Scan a single IP

```bash
sudo nmap $IP -sn oA $OUTFILE
```

ICMP ping and packet trace

```bash
sudo nmap $IP -sn oA $OUTFILE -PE --packet-trace --disable-arp-ping
```

Show the ARP request details

```bash
sudo nmap $IP -sn oA $OUTFILE -PE --reason
```

