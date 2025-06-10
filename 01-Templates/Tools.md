# <% tp.file.title %>

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

Brief description of this category

command syntax ^<% tp.file.title.toLowerCase() %>-category1

### Category 2

Brief description of this category

command syntax ^<% tp.file.title.toLowerCase() %>-category2

### Category 3

Brief description of this category

command syntax ^<% tp.file.title.toLowerCase() %>-category3

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
FROM "06-CTF-Writeups" AND #<% tp.file.title.toLowerCase() %>
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#<% tp.file.title.toLowerCase() %> #tool