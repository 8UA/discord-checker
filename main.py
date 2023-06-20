import sys
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
token = os.environ.get("AUTH_TOKEN")

import requests
import secrets
import string
from time import sleep

        # Configurations #
l = 4   # Generated usernames lenght (Default: 4)
t = 1   # Delay between requests (Default: 1 Second)

print("""
 █▀▀▄  ▀  █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄    █▀▀█ █  █ █▀▀ █▀▀ █ █ █▀▀ █▀▀█ 
 █  █ ▀█▀ ▀▀█ █   █  █ █▄▄▀ █  █ ▀▀ █    █▀▀█ █▀▀ █   █▀▄ █▀▀ █▄▄▀ 
 █▄▄▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀ ▀▀ ▀▀▀     █▄▄█ ▀  ▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀▀▀ ▀ ▀▀
""")

try:
    i = int(input('▾▾▾ Options ▾▾▾\n\n1. Generate & check random usernames\n2. Read usernames from file\n\n▸ '))
    print()
except ValueError:
    print("You dummy >:(")
    sys.exit()

if i == 1:
    while True:
        try:
            s = ''.join(secrets.choice(string.ascii_lowercase + string.digits + "_.")
                for i in range(l))
                
            r = requests.patch(
                'https://discord.com/api/v9/users/@me',
                headers={
                        'Authorization': f'{token}'
                    },
                json={
                        "username": f"{s}",
                        "password": ""
                    },
                )
            
            if r.status_code == 401:
                print("Unauthorized, Please add your Discord token into your '.env' file.")
                sleep(10)
            else:
                print(f"Generated Username: {s}\n{r.content,}\n")
            sleep(t)

        except KeyboardInterrupt:
            print("Bye :)")
            sys.exit()

elif i == 2:
    with open('list.txt', 'r') as userlist:
        for user in userlist:
            try:
                r = requests.patch(
                    'https://discord.com/api/v9/users/@me',
                    headers={
                            'Authorization': f'{token}'
                        },
                    json={
                            "username": f"{user}",
                            "password": ""
                        },
                    )

                if r.status_code == 401:
                    print("Unauthorized, Please add your Discord token into your '.env' file.")
                    sleep(10)
                else:
                    print(f"Name from list: {user}{r.content,}\n")            
                    sleep(t)
                    
            except KeyboardInterrupt:
                print("Bye :)")
                sys.exit()

elif i > 2:
    print("No")
    sys.exit()