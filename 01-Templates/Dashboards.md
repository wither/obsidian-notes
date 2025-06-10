# <% tp.file.title %>

## Methodology Overview

Brief description of this attack domain and typical workflow

## Core Techniques

```dataview
LIST FROM #technique AND #MAIN-TAG
SORT file.name
```

## Essential Tools

```dataview
LIST FROM #tool AND #MAIN-TAG
SORT file.name
```

## Recent Activity

```dataview
TABLE file.name as "Note", file.mtime as "Updated"
FROM #MAIN-TAG
SORT file.mtime DESC
LIMIT 10
```

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "06-CTF-Writeups" AND #MAIN-TAG
SORT file.ctime DESC
LIMIT 8
```

## Quick Access

Most important techniques and tools for this domain:

- [[Key-Technique-1]] - Brief description
- [[Key-Technique-2]] - Brief description
- [[Essential-Tool-1]] - Primary use
- [[Essential-Tool-2]] - Secondary use

#<% tp.file.title.toLowerCase().replace(/\s+/g, '-') %> #dashboard #MAIN-TAG