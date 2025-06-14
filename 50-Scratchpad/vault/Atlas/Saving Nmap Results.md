---
Title: Saving Nmap Results
Folders:
  - "[[Nmap]]"
---
# Saving Nmap Results
---

Output to all formats

```bash
sudo nmap $IP -p- -oA $OUTFILE
```

Create HTML report from XML output

```bash
xsltproc $TARGETFILE -o $OUTFILE
```

![[Pasted image 20241220205758.png]]

