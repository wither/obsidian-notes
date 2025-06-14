---
Title: Nmap Performance
Folders:
  - "[[Nmap]]"
---
# Nmap Performance
---

Optimising RTT (Round -Trip-Time)

```bash
sudo nmap $IP -F --initial-rtt-timeout 50ms --max-rtt-timeout 100ms
```

Specify the retry rate of sent packets

```bash
sudo nmap $IP -F --max-retries 0
```

Optimising packet rate

```bash
sudo nmap $IP -f --min-rate 300
```

Timing level

```bash
sudo nmap $IP -F -T 5
```

