import sys
import os
import asyncio
import aiohttp
import secrets
import string
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv())
token = os.environ.get("AUTH_TOKEN")

# Configurations #
l = 4  # Generated usernames length (Default: 4)
t = 1  # Delay between requests (Default: 1 Second)

print(
    """
 █▀▀▄  ▀  █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄    █▀▀█ █  █ █▀▀ █▀▀ █ █ █▀▀ █▀▀█ 
 █  █ ▀█▀ ▀▀█ █   █  █ █▄▄▀ █  █ ▀▀ █    █▀▀█ █▀▀ █   █▀▄ █▀▀ █▄▄▀ 
 █▄▄▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀ ▀▀ ▀▀▀     █▄▄█ ▀  ▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀▀▀ ▀ ▀▀
"""
)
print("this was made by 8ua and edited by dickgirl")
try:
    i = int(input("▾▾▾ Options ▾▾▾\n\n1. Generate & check random usernames\n2. Read usernames from file\n\n▸ "))
    print()
except ValueError:
    print("You dummy >:(")
    sys.exit()

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")


async def check_username(username):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.patch(
                'https://discord.com/api/v9/users/@me',
                headers={
                    'Authorization': token
                },
                json={
                    "username": username,
                    "password": ""
                },
            ) as response:
                if response.status == 401:
                    print("Unauthorized, Please add your Discord token into your '.env' file.")
                    await asyncio.sleep(10)
                elif response.status == 429:
                    print("Rate limited. Waiting...")
                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        await asyncio.sleep(int(retry_after))
                elif response.headers.get('Server') == 'cloudflare': 
                    print("Waiting for 5 minutes due to Cloudflare.")
                    await asyncio.sleep(300)
                else:
                    data = await response.json()
                    if "USERNAME_ALREADY_TAKEN" in data.get("message", ""):
                        print(f"Username taken: {username}")
                    else:
                        print(f"Username available: {username}")
                        return username
        except Exception as e:
            print(f"Error occurred for username {username}: {e}")
    return None


async def generate_and_check_usernames():
    output_file = f"{output_dir}/available_username_data_{timestamp}.txt"
    with open(output_file, "w") as f:
        while True:
            username = ''.join(secrets.choice(string.ascii_lowercase + string.digits + "_.")
                               for _ in range(l))
            result = await check_username(username)
            if result:
                f.write(result + "\n")
            await asyncio.sleep(t)


async def read_usernames_from_file():
    list_dir = "lists"
    os.makedirs(list_dir, exist_ok=True)

    files = os.listdir(list_dir)
    txt_files = [f for f in files if f.endswith(".txt")]

    if not txt_files:
        print("No text files found in the 'lists' directory.")
        return

    print("Available text files in 'lists' directory:")
    for i, filename in enumerate(txt_files):
        print(f"{i + 1}. {filename}")

    try:
        selection = int(input("Select a text file to read usernames from (enter the corresponding number): "))
        if selection < 1 or selection > len(txt_files):
            print("Invalid selection.")
            return

        selected_file = txt_files[selection - 1]
        file_path = os.path.join(list_dir, selected_file)

        output_file = f"{output_dir}/available_username_data_{timestamp}.txt"
        with open(file_path, "r") as userlist, open(output_file, "w") as f:
            tasks = []
            async with aiohttp.ClientSession() as session:
                for user in userlist:
                    task = asyncio.create_task(check_username(user.strip()))
                    tasks.append(task)
                    await asyncio.sleep(t)

                results = await asyncio.gather(*tasks)
                for result in results:
                    if result:
                        f.write(result + "\n")

    except ValueError:
        print("Invalid input.")


async def main():
    if i == 1:
        await generate_and_check_usernames()
    elif i == 2:
        await read_usernames_from_file()
    else:
        print("No")


if __name__ == "__main__":
    asyncio.run(main())
