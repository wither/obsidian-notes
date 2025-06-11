# Linux File Transfer

## Overview

What this technique is and when I need it

## Downloading

### Base64 Encoding

**Step 1:** Check the MD5 hash of the contents.
```bash
md5sum id_rsa
```

**Step 2:** Encode contents to base64 and copy it to clipboard.
```bash
cat id_rsa | base64 -w 0; echo
```

**Step 3:** On the second Linux machine, decode the Base64 file content.
```bash
echo -n 'encoded' | base64 -d > id_rsa
```

**Step 4:** Confirm the MD5 hash matches.
```bash
md5sum id_rsa
```

### wget

Download a file.
![[wget#^simple-download]]

### cURL

Download a file.
![[curl#^simple-download]]











## Uploading

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
FROM "06-CTF-Writeups" AND #linux-file-transfer
SORT file.ctime DESC
LIMIT 5
```

## Learning Resources

- 

#linux-file-transfer #technique