# wget

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Download all files within a specific web directory
```bash
wget -r -np -nH --cut-dirs=1 --reject "index.html*" -e robots=off http://10.10.237.124/development/
```
^download-web-directory-files

Download all available FTP files:
```shell
wget -m --no-passive ftp://anonymous:anonymous@10.129.14.136
```

```bash
wget url -O path
```
^simple-download


```bash
wget url -O path | bash
```

### Category 2

Brief description of this category

command syntax ^wget-category2

### Category 3

Brief description of this category

command syntax ^wget-category3

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
FROM "06-CTF-Writeups" AND #wget
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#wget #tool