# SMB

## Standard Enumeration

My go-to commands for enumerating this service:

### Basic Discovery

quick command to confirm service and version ^smb-basic

### Detailed Enumeration

thorough enumeration command I use ^smb-detailed

## Quick Wins to Try

- **Low-hanging fruit:** Common misconfigurations or default creds
- **Version-specific:** Known vulnerabilities for common versions
- **Anonymous access:** How to check for anonymous/guest access

## Attack Patterns

```dataview
LIST FROM #technique AND #smb
SORT file.name
```

## Tools for This Service

```dataview
LIST FROM #tool AND #smb
SORT file.name
```

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #smb
SORT file.ctime DESC
LIMIT 8
```

## Notes

- Gotchas I've encountered
- Environment-specific considerations
- Things that commonly break

#smb #service