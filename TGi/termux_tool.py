import sys, os, json, time, asyncio
from telethon import TelegramClient, functions
class Colors:
    G, R, Y, C, B, E = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[94m', '\033[0m'
async def lookup(c, u):
    try:
        e = await c.get_entity(int(u) if u.isdigit() else u)
        f = await c(functions.users.GetFullUserRequest(id=e))
        print(f"\n{Colors.G}[DATA FOUND]{Colors.E}\nID: {e.id}\nUser: @{e.username}\nName: {e.first_name} {e.last_name or ''}\nBio: {f.full_user.about or 'N/A'}")
    except Exception as err: print(f"{Colors.R}[!] Error: {str(err)}{Colors.E}")
async def main():
    os.system('clear')
    print(f"{Colors.C}TeleSight OSINT v1.0{Colors.E}")
    aid, ah = input("API ID: "), input("API Hash: ")
    client = TelegramClient('TGi_session', aid, ah)
    await client.start()
    t = input("\nTarget UID/User: ")
    await lookup(client, t)
if __name__ == '__main__': asyncio.run(main())
