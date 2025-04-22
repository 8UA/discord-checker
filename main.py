import sys
import os
import requests
import secrets
import string
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from time import sleep

load_dotenv(find_dotenv())
TOKEN = os.environ.get("AUTH_TOKEN")

OUTPUT_DIR = "output"
LIST_DIR = "lists"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LIST_DIR, exist_ok=True)

print(
"""
 █▀▀▄  ▀  █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄    █▀▀█ █  █ █▀▀ █▀▀ █ █ █▀▀ █▀▀█ 
 █  █ ▀█▀ ▀▀█ █   █  █ █▄▄▀ █  █ ▀▀ █    █▀▀█ █▀▀ █   █▀▄ █▀▀ █▄▄▀ 
 █▄▄▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀ ▀▀ ▀▀▀     █▄▄█ ▀  ▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀▀▀ ▀ ▀▀
"""
)


def check_username(username):
    try:
        r = requests.post(
            "https://discord.com/api/v9/users/@me/pomelo-attempt",
            headers={
                "Authorization": TOKEN,
                "content-type": "application/json"
            },
            json={"username": username},
            timeout=10
        )

        if r.status_code == 401:
            print("Unauthorized. Add your pomelo auth token to .env file.")
            sleep(10)
            sys.exit(1)
        
        data = r.json()
        if data.get("taken") is True:
            print(f"Username taken: {username}")
            return None
        else:
            print(f"Username available: {username}")
            return username
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {username} - {e}")
    except Exception as e:
        print(f"Error: {username} - {e}")
    
    return None


def generate_username(length):
    chars = string.ascii_lowercase + string.digits + "_."
    return ''.join(secrets.choice(chars) for _ in range(length))


def get_delay():
    try:
        delay = float(input("Delay between requests in seconds: "))
        return delay
    except ValueError:
        print("Invalid input. Using default: 1s")
        return 1.0


def generate_and_check_usernames():
    try:
        username_length = int(input("Username length (2-32): "))
        if username_length < 2 or username_length > 32:
            print("Invalid length. Using default: 4")
            username_length = 4
    except ValueError:
        print("Invalid input. Using default: 4")
        username_length = 4
    
    delay = get_delay()
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"{OUTPUT_DIR}/available_generated_{timestamp}.txt"
    checked = set()
    
    print(f"\nChecking usernames ({username_length} chars)")
    print(f"Delay: {delay}s between requests")
    print(f"Saving to: {output_file}")
    
    try:
        with open(output_file, "w") as f:
            while True:
                username = generate_username(username_length)
                if username not in checked:
                    checked.add(username)
                    result = check_username(username)
                    if result:
                        f.write(f"{result}\n")
                        f.flush()
                    sleep(delay)
    
    except KeyboardInterrupt:
        print("\nStopped.")


def read_usernames_from_file():
    txt_files = [f for f in os.listdir(LIST_DIR) if f.endswith(".txt")]

    if not txt_files:
        print(f"No .txt files found in '{LIST_DIR}' directory.")
        return

    print("Available files:")
    for i, filename in enumerate(txt_files):
        print(f"{i + 1}. {filename}")

    try:
        selection = int(input("\nSelect file: "))
        if selection < 1 or selection > len(txt_files):
            print("Invalid selection.")
            return

        selected_file = txt_files[selection - 1]
        file_path = os.path.join(LIST_DIR, selected_file)
        
        delay = get_delay()
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = f"{OUTPUT_DIR}/available_from_file_{timestamp}.txt"
        
        available = 0
        total = 0
        
        print(f"\nDelay: {delay}s between requests")
        print(f"Saving to: {output_file}")
        
        with open(file_path, "r") as in_file, open(output_file, "w") as out_file:
            for line in in_file:
                username = line.strip()
                if not username:
                    continue
                    
                total += 1
                result = check_username(username)
                if result:
                    out_file.write(f"{result}\n")
                    out_file.flush()
                    available += 1
                
                sleep(delay)
        
        print(f"\nFound {available} available usernames out of {total}")
        print(f"Results saved to {output_file}")

    except ValueError:
        print("Invalid input. Enter a number.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    if not TOKEN:
        print("Token not found!")
        print("Create a .env file with your pomelo auth token.")
        sleep(10)
        sys.exit(1)
    
    try:
        print("▾▾▾ Options ▾▾▾\n")
        print("1. Generate & check random usernames")
        print("2. Read usernames from file\n")
        opt = int(input("▸ "))
        print()
    except ValueError:
        print("Invalid option.")
        sys.exit(1)
    
    if opt == 1:
        generate_and_check_usernames()
    elif opt == 2:
        read_usernames_from_file()
    else:
        print("Invalid option.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye :(")
        sys.exit(0)