Creating Custom Password Wordlist
```bash
cupp -i
```

Remove Passwords Shorter Than 8
```bash
sed -ri '/^.{,7}$/d' william.txt
```

Remove Passwords With No Special Chars
```bash
sed -ri '/[!-/:-@\[-`\{-~]+/!d' william.txt
```

Remove Passwords With No Numbers
```bash
sed -ri '/[0-9]+/!d' william.txt
```

Generate Usernames List
```bash
./username-anarchy Bill Gates > bill.txt
```

Create Sequence Wordlist
```bash
for i in $(seq 1 1000); do echo $i >> ids.txt; done
```