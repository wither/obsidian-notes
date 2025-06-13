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

Create an FTP server with write permissions
```bash
sudo python3 -m pyftpdlib --port 21 --write
```
^write-create-ftp-server

Create an webserver in python3
```bash
python3 -m http.server
```
^python3-webserver

Create an webserver in python2.7
```bash
python2.7 -m SimpleHTTPServer
```
^python2-7-webserver

Create an webserver with upload page
```bash
sudo python3 -m uploadserver
```
^uploadserver

Create a Webdav share in the /tmp folder on port 80 with anonymous login
```bash
sudo wsgidav --host=0.0.0.0 --port=80 --root=/tmp --auth=anonymous 
```
^wsgidav-create-share

Unzip a file
```bash
python3 -m zipfile -e upload.zip .
```
^unzip-file

### Category 2

Pipe raw bytes to a file input
```bash
python3 -c '__import__("sys").stdout.buffer.write(b"A"*56 + b"\x5a\x1e\x3c\x5a\x00\x00\x00\x00")' | /challenge/binary-exploitation-var-control 
```
^pipe-raw-bytes

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