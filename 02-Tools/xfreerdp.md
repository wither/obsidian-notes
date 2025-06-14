# xfreerdp

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

RDP with clipboard
```bash
xfreerdp3 /u:'user' /p:'pass' /v:'ip' +clipboard
```
^rdp-with-clipboard

RDP (Always on Top)
```bash
xfreerdp3 /u:'user' /p:'pass' /v:'ip' +clipboard & sleep 3 && wmctrl -r "FreeRDP" -b add,above
```
^always-on-top

Mount Linux folder
```bash
xfreerdp3 /v:10.10.10.132 /d:HTB /u:administrator /p:'Password0@' /drive:linux,/home/plaintext/htb/academy/filetransfer
```
^mount-linux-folder

```bash
xfreerdp3 /v:10.129.201.55 /u:htb-student /p:'HTB_@cademy_stdnt!' /d:HTB +clipboard /drive:WITHER,/home/wither/CTF/HTB/Academy +fonts /cert:ignore +window-drag +menu-anims +video +gfx /network:auto /compression-level:2 /sound:sys:alsa /dynamic-resolution +auto-reconnect /auto-reconnect-max-retries:5 +relax-order-checks /log-level:WARN /kbd:unicode:on +async-update +async-channels 2>/dev/null
```

## Personal Notes

- Things I learned from experience
- Common mistakes I made
- Environment-specific quirks

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #xfreerdp
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#xfreerdp #tool