---
Title: Nmap Scripting Engine
Folders:
  - "[[Nmap]]"
---
# Nmap Scripting Engine
---

Default scripts 

```bash
sudo nmap $IP -sC
```

Specific script category

```bash
sudo nmap $IP --script $CATEGORY
```

Defined scripts

```bash
sudo nmap $IP --script $NAME1,$NAME2
```

Aggressive scan

```bash
sudo nmap $IP -p 80 -A
```

