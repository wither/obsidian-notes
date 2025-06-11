# Python

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Create an FTP server
```bash
sudo python3 -m pyftpdlib --port 21
```
^create-ftp-server

Pipe raw bytes to a file input
```bash
python3 -c '__import__("sys").stdout.buffer.write(b"A"*56 + b"\x5a\x1e\x3c\x5a\x00\x00\x00\x00")' | /challenge/binary-exploitation-var-control 
```
^pipe-raw-bytes
### Category 2

Brief description of this category

command syntax ^python-category2

### Category 3

Brief description of this category

command syntax ^python-category3

## Syntax I Forget

- Flag or option I always look up
- Parameter format I can't remember
- Output options or file formats

## When I Use This vs Alternatives

- **Use this tool when:** Specific circumstances
- **Use alternative when:** When other tools are better
- **Combines well with:** Tools that work together with this

## Personal Notes

- Things I learned from experience
- Common mistakes I made
- Environment-specific quirks

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #python
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#python #tool