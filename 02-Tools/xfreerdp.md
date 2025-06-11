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