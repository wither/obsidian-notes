---
Title: Service Enumeration with Nmap
Folders:
  - "[[Nmap]]"
---
# Service Enumeration with Nmap
---

Show the scan status on a timer

```bash
sudo nmap $IP -p- -sV --status-every=$SECs
```

Increase the verbosity

```bash
sudo nmap $IP -p- -sV -vv
```

