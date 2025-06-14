---
Title: Host and Port Scanning with Nmap
Folders:
  - "[[Nmap]]"
---
# Host and Port Scanning with Nmap
---

Scan the top ports

```bash
sudo nmap $IP --top-ports=$NUM
```

Trace packets to a port

```bash
sudo nmap $IP -p $PORT --packet-trace -Pn -n --disable-arp-ping
```

TCP connect scan that completes a full handshake

```bash
sudo nmap $IP -p $PORT -sT
```

UDP port scan

```bash
sudo nmap $IP -F -sU
```

Version scan

```bash
sudo nmap $IP -p $PORT -sV
```

