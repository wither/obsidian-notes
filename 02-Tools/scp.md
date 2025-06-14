# SCP

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Download a file.
```bash
scp plaintext@192.168.49.128:/root/myroot.txt . 
```
^download-file-from-linux

Upload a file.
```bash
scp /etc/passwd htb-student@10.129.86.90:/home/htb-student/
```
^upload-file-to-linux



## Personal Notes

- Things I learned from experience
- Common mistakes I made
- Environment-specific quirks

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #scp
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#scp #tool