# find

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Find binaries with the SUID bit set
```bash
find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
```

Find binaries with the SETGID bit set 
```bash
find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null
```

Find world-writeable directories
```bash
find / -path /proc -prune -o -type d -perm -o+w 2>/dev/null
```

Find world-writeable files 
```bash
find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null
```
^find-category3

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
FROM "06-CTF-Writeups" AND #find
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#find #tool