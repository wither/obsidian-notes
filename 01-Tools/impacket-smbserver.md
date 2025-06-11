# impacket-smbserver

_What this tool does and when I reach for it_

## Primary Use Cases

- Starting an SMB server for file transfer.

## Command Patterns

### Category 1

Create SMB server with username and password.
```bash
sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test
```
^create-authenticated-smb-server

### Category 2

Brief description of this category

command syntax ^impacket-smbserver-category2

### Category 3

Brief description of this category

command syntax ^impacket-smbserver-category3

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
FROM "06-CTF-Writeups" AND #impacket-smbserver
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#impacket-smbserver #tool