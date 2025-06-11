# curl

_What this tool does and when I reach for it_

## Primary Use Cases

Main things I use this tool for

## Command Patterns

### Category 1

All subdomains for a given domain.
```bash
curl -s https://sonar.omnisint.io/subdomains/{domain} \| jq -r '.[]' \| sort -u
```

All TLDs found for a given domain.
```bash
curl -s https://sonar.omnisint.io/tlds/{domain} \| jq -r '.[]' \| sort -u
```

All results across all TLDs for a given domain.
```bash
curl -s https://sonar.omnisint.io/all/{domain} \| jq -r '.[]' \| sort -u
```

Reverse DNS lookup on IP address.
```bash
curl -s https://sonar.omnisint.io/reverse/{ip} \| jq -r '.[]' \| sort -u
```

Reverse DNS lookup of a CIDR range.
```bash
curl -s https://sonar.omnisint.io/reverse/{ip}/{mask} \| jq -r '.[]' \| sort -u
```

Certificate Transparency.
```bash
curl -s "https://crt.sh/?q=${TARGET}&output=json" \| jq -r '.[] \| "\(.name_value)\n\(.common_name)"' \| sort -u
```
^curl-category3

SSL certificate checks can be skipped using the cURL `-k` flag.
Example:
```shell
curl -k https://google.com/
```

Download a file
```bash
curl -o path url
```
^simple-download

Download and execute file in memory.
```bash
curl -o path url | bash
```

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
FROM "06-CTF-Writeups" AND #curl
SORT file.ctime DESC
LIMIT 5
```

## Quick Links

- [[Primary-Technique]] - Main technique this supports
- [[Secondary-Technique]] - Other technique this supports

#curl #tool