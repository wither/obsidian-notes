# smbmap

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

SMBmap:
```shell
smbmap -H 10.129.14.128
```
^smbmap-category3

smbmap can also download
```shell
smbmap -H 10.129.14.128 --download "notes\note.txt"
```

and upload files to/from the share
```shell
smbmap -H 10.129.14.128 --upload test.txt "notes\test.txt"
```

both can be done authenticated
```shell
smbmap -u jason -p '34c8zuNBo91!@28Bszh' -H 10.129.203.6 --download "GGJ\id_rsa"
```


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
FROM "06-CTF-Writeups" AND #smbmap
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#smbmap #tool