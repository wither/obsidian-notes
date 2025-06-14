# perl

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Create a webserver
```bash
perl -MIO::Socket::INET -e '$s=IO::Socket::INET->new(LocalPort=>8000,Listen=>1,Reuse=>1);while($c=$s->accept){<$c>=~/GET\s+(\S+)/;$f=".$1";open F,"<",$f and print $c <F>;close F;close $c}'
```
^create-webserver

Download a file
```bash
perl -e 'use LWP::Simple; getstore("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh");'
```
^download-remote-file

## Personal Notes

- Things I learned from experience
- Common mistakes I made
- Environment-specific quirks

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #perl
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#perl #tool