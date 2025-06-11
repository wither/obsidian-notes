# <% tp.file.title %>

**Platform:** PLATFORM  
**Start Date:** <% tp.date.now("DD/MM/YYYY") %>  
**Completion Date:** TBD  
**Total Machines:** X  
**Network Complexity:** Beginner/Intermediate/Advanced

## Network Summary

Brief description of the network scenario and learning objectives

## Current Status

- **Machines Compromised:** 0/X
- **Current Position:** External
- **Next Targets:** Initial reconnaissance
- **Stuck On:** N/A

## Network Topology

```mermaid
graph TD
    A[External] --> B[Target Network]
    B --> C[Unknown Internal]
```

## Compromise Chain

1. **External → ???:** Working on initial access

## Credentials Discovered

|Username|Password|Hash|Domain|Access Level|Source|
|---|---|---|---|---|---|
|||||||

## Key Network Techniques

_To be documented as network is explored_

## Machines Overview

```dataview
TABLE file.name as "Machine", 
  choice(contains(file.content, "✅ Compromised"), "✅", choice(contains(file.content, "🎯 Targeting"), "🎯", "❓")) as "Status",
  choice(contains(file.tags, "windows"), "🪟", choice(contains(file.tags, "linux"), "🐧", "❓")) as "OS"
FROM "<% tp.file.folder() %>/Machines"
SORT file.name
```

## Learning Outcomes

_To be updated as network progresses_

- **Network-specific skills:**
- **Tool combinations:**
- **Methodology insights:**

## Quick Links

- **Network Map:** [[01-Network-Map]]
- **Credentials:** [[02-Credential-Tracker]]
- **Machines Folder:** [[<% tp.file.folder() %>/Machines]]

#<% tp.file.title.toLowerCase().replace(/\s+/g, '-') %> #network #PLATFORM