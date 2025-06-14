# xfreerdp

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

RDP with clipboard
```bash
xfreerdp3 /v:'10.129.201.55' /u:'htb-student' /p:'HTB_@cademy_stdnt!' /d:HTB +clipboard
```
^rdp-with-clipboard

RDP (Always on Top)
```bash
xfreerdp3 /v:'10.129.201.55' /u:'htb-student' /p:'HTB_@cademy_stdnt!' /d:HTB +clipboard & sleep 3 && wmctrl -r "FreeRDP" -b add,above
```
^always-on-top

Mount Linux folder
```bash
xfreerdp3 /v:'10.129.201.55' /u:'htb-student' /p:'HTB_@cademy_stdnt!' /d:HTB /drive:linux,/home/plaintext/htb/academy/filetransfer
```
^mount-linux-folder

Ultimate command
```bash
xfreerdp3 /v:'10.129.201.55' /u:'htb-student' /p:'HTB_@cademy_stdnt!' /d:HTB +clipboard /drive:WITHER,/home/wither/CTF/HTB/Academy /cert:ignore +window-drag +video +gfx /gfx:AVC420 +fonts /network:auto /compression-level:2 /sound:sys:alsa /dynamic-resolution +auto-reconnect /auto-reconnect-max-retries:5 +relax-order-checks /kbd:unicode:on +async-update +async-channels /log-level:OFF
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