# Ncat

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Sending a file
```bash
sudo ncat -l -p 443 --send-only < SharpKatz.exe
```
^send-file-to-listener

Receiving a file
```bash
sudo ncat -l -p 443 --send-only < SharpKatz.exe
```
^receive-file-from-listener

## Personal Notes

- Things I learned from experience
- Common mistakes I made
- Environment-specific quirks

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #ncat
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#ncat #tool