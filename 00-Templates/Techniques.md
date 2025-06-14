# <% tp.file.title %>

## Table of Contents
```table-of-contents
exclude: /Table of Contents/i
minLevel: 2
style: nestedList
hideWhenEmpty: true
```
## Overview

What this technique is and when I need it

## Key Concepts

Important things to understand about this technique

## Theme

### Tool / Protocol

#### Method: Method

**Step 1:** Step
link



## Related Techniques

- [[Similar-Technique]] 

## CTF Examples

```dataview
TABLE file.name as "Box", choice(contains(file.tags, "easy"), "🟢", choice(contains(file.tags, "medium"), "🟡", "🔴")) as "Diff"
FROM "05-Boxes" AND #<% tp.file.title.toLowerCase().replace(/\s+/g, '-') %>
SORT file.ctime DESC
LIMIT 5
```

## Learning Resources

- 

#<% tp.file.title.toLowerCase().replace(/\s+/g, '-') %> #technique