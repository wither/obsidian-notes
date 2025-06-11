# Untitled

## Standard Enumeration

My go-to commands for enumerating this service:

### Basic Discovery

quick command to confirm service and version ^untitled-basic

### Detailed Enumeration

thorough enumeration command I use ^untitled-detailed

## Quick Wins to Try

- **Low-hanging fruit:** Common misconfigurations or default creds
- **Version-specific:** Known vulnerabilities for common versions
- **Anonymous access:** How to check for anonymous/guest access

## Attack Patterns

```dataview
LIST FROM #technique AND #untitled
SORT file.name
```

## Tools for This Service

```dataview
LIST FROM #tool AND #untitled
SORT file.name
```

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #untitled
SORT file.ctime DESC
LIMIT 8
```

## Notes

- Gotchas I've encountered
- Environment-specific considerations
- Things that commonly break

#untitled #service