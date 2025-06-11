# <% tp.file.title %>

_Last Updated: <% tp.date.now("DD/MM/YYYY HH:mm") %>_

## Active Credentials

### Domain Accounts

|Username|Password|Hash|Domain|Privileges|Source Machine|Status|
|---|---|---|---|---|---|---|
||||||||

### Local Accounts

|Machine|Username|Password|Hash|Privileges|Notes|
|---|---|---|---|---|---|
|||||||

### Service Accounts

|Service|Username|Password|Hash|Machine|Access Level|
|---|---|---|---|---|---|
|||||||

## Credential Testing Results

### Password Spray Results

Track which passwords work across multiple accounts:

**Password Pattern: "PATTERN"**

- ✅ account1 (Role)
- ❌ account2 (Role)
- 🔄 account3 (Testing)

### Hash Cracking Results

|Account|Hash Type|Crackable|Password|Time to Crack|Notes|
|---|---|---|---|---|---|
|||||||

## Access Matrix

Track which credentials work on which machines:

|Credential|Machine1|Machine2|Machine3|Machine4|
|---|---|---|---|---|
|domain\user1|❓ Unknown|❓ Unknown|❓ Unknown|❓ Unknown|

## Attack Technique Results

### Kerberoasting Results

|Account|Service|Crackable|Password|Hash Strength|Notes|
|---|---|---|---|---|---|
|||||||

### ASREPRoasting Results

|Account|Crackable|Password|Time to Crack|Notes|
|---|---|---|---|---|
||||||

### NTLM Relay Results

|Source|Target|Success|Access Gained|Notes|
|---|---|---|---|---|
||||||

## Privilege Escalation Paths

Document how to escalate with discovered credentials:

1. **Current Position → Target:**
    - Method: [[Technique-Name]]
    - Requirements: Specific credentials/access
    - Command: `command sequence`

## Environment Notes

- **Password Policy:** Policy details (length, complexity, etc.)
- **Lockout Policy:** Lockout thresholds and timing
- **Common Patterns:** Observed password patterns
- **Service Account Patterns:** Naming conventions for service accounts
- **Default Credentials:** Any default creds that worked

## Credential Sources

Track where different types of credentials typically come from:

- **Memory dumps:** Mimikatz, procdump, etc.
- **Registry:** SAM/SYSTEM dumps
- **Files:** Configuration files, scripts
- **Network:** Responder, packet capture
- **Brute force:** Hydra, password spray
- **Social engineering:** Phishing, etc.

## Quick Reference Commands

```bash
# Password spraying
# netexec smb IP-RANGE -u users.txt -p passwords.txt

# Hash dumping
# secretsdump.py domain/user:password@IP

# Kerberoasting
# impacket-GetUserSPNs domain/user:password -dc-ip IP -request

# ASREPRoasting  
# impacket-GetNPUsers domain/ -usersfile users.txt -format hashcat
```

## Links

- **Network overview:** [[00-<% tp.file.title.split('-')[0] %>-Overview]]
- **Network map:** [[01-Network-Map]]
- **Machines folder:** [[<% tp.file.folder() %>/Machines]]

#<% tp.file.title.toLowerCase().replace(/\s+/g, '-') %> #credentials #<% tp.file.folder().split('/').pop().toLowerCase().replace(/\s+/g, '-') %>