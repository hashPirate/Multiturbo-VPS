from discord_webhook import DiscordWebhook
from itertools import cycle
import time
import msmcauth
import requests
from datetime import datetime
from time import sleep
import asyncio
import sys
import os
from threading import Lock
import socks
import threading
import json

from colorama import Fore, init

init(autoreset=True)
print_lock = Lock()
num_names = 0
count = 0
webflag = False
authstatus = False
session = requests.Session()
checktime = time.time()
calcspeed = 5000 #THIS NEEDS TO BE DIVISIBLE BY NUMBER OF PROXIES
errorcount = 0
tokencount = 0


class MicrosoftAccount:
    def __init__(self, token: str, email: str, target: str, proxy: dict) -> None:
        self.token = token
        self.email = email
        self.target = target
        self.bearer = self.token
        self.proxy = proxy
    
        
        self.lock = threading.Lock()


    def turbo(self, lock):
     global count, num_names,session, errorcount, webflag
   
    # rest of the code

     with lock:
        proxy = next(proxy_iter)
        #  self.bearer = next(token_iter).split(": ")[0] #newest line can delete this but it keeps accounts in line from repeating!!!!!
        
     try:
        self.payload = {
        "profileName": self.target,
}
            
        
        
       # self.URL = "https://minecraftapi-bef7bxczg0amd8ef.z01.azurefd.net/minecraft/profile//"
        self.URL = "https://minecraftapi-bef7bxczg0amd8ef.z01.azurefd.net/minecraft/profile//"
            
        self.HEADERS = {
          "Accept": "application/json",
          "Authorization": f"Bearer {self.bearer}",
          "Content-Type": "application/json"
          
}




        
        session.proxies = {
            'http': f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}",
            'https': f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
        }
        b4timestamp = datetime.now().strftime("%H:%M:%S.%f")
        with open(f"timestamps.txt", "a") as file:
              #  file.write(f"{b4timestamp} - {self.email} - {self.target}\n")
                file.write(f"{b4timestamp}\n")
        response = session.post(self.URL, json=self.payload, headers=self.HEADERS)
        
        if response.status_code == 400:
            availability = response.json().get("details", {}).get("status", "") if response.status_code != 404 else "Not Found"
            timestamp = datetime.now().strftime("%H:%M:%S.%f")
            if availability == "ALREADY_REGISTERED":
                safe_print(f"{Fore.RED}{self.email} is already registered hahahahahahahahaha")
                errorcount = errorcount + 1
            elif availability == "NOT_ENTITLED":
                safe_print(f"{Fore.RED}{self.email} NOT ENTITLED NOOOOO")
                errorcount = errorcount + 1
            with lock:
             safe_print(f"{Fore.CYAN}[Task {count}] {timestamp}|[{response.status_code}][{availability}] [{num_names}] for {self.target}")
        elif response.status_code == 200:
            with lock:
             safe_print(f"{Fore.GREEN}[+] Successfully claimed {self.target} on {self.email}")
             
            change_skin(self.bearer)
            webhook_url = "https://discord.com/api/webhooks/1217162209030049924/bPIxlhjKAWrHipn9Zh6eH0Ccd5AdzKCKm1aBcmejbFib_zE7mDU2hmdaQNsynjyxGNmC"  # Replace with your webhook URL
            send_discord_webhook(webhook_url, f"@everyone Successfully claimed {self.target} on {self.email}")
            with open(f"{self.target}.txt", "w") as file:
                file.write(f"Email: {self.email}\nToken: {self.token}")
            claim_namemc(f"{self.email}")    
        elif response.status_code == 429:
           
            timestamp = datetime.now().strftime("%H:%M:%S.%f")
            with lock:
             safe_print(f"{Fore.YELLOW}[Task {count}] {timestamp}|[{response.status_code}] Rate limited. Retrying with a different proxy and token. {self.email}")
             errorcount += 1
              
        elif response.status_code == 401 and webflag == False:
            with lock:
                send_discord_webhook("https://discord.com/api/webhooks/1217162209030049924/bPIxlhjKAWrHipn9Zh6eH0Ccd5AdzKCKm1aBcmejbFib_zE7mDU2hmdaQNsynjyxGNmC", "@everyone invalid bearer!")
                webflag = True
                errorcount += 1
        elif response.status_code == 503:
            error = response.json().get("error", "") if response.status_code != 404 else "Not Found"
            timestamp = datetime.now().strftime("%H:%M:%S.%f")
            jsonresponse = json.dumps(response.json(), indent=4)
            with lock:
             safe_print(f"{Fore.CYAN}[Task {count}] {timestamp}|[{response.status_code}][{error}] [{num_names}] for {self.target} and {self.email}\n{jsonresponse}")
            errorcount = errorcount + 1
        
        else:
            
            availability = response.json().get("details", {}).get("status", "") if response.status_code != 404 else "Not Found"
            timestamp = datetime.now().strftime("%H:%M:%S.%f")
            with lock:
             safe_print(f"{Fore.CYAN}[Task {count}] {timestamp}|[{response.status_code}][{availability}] [{num_names}] for {self.target}")


        
     except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        errorcount += 1
       

def change_skin(token: str):
    url = "https://api.minecraftservices.com/minecraft/profile/skins"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": "https://textures.minecraft.net/texture/5282f5f07c4a81f659cf5f8cbcb0944c1afc8a410697c9a50f44368b20faac5a",
        "variant": "CLASSIC"
    }
    response = requests.post(url, headers=headers, json=payload)

def claim_namemc(email: str):
    with open("accounts.txt", "r") as f, open("nametoclaim.txt", "w") as output:
        for line in f:
            if email in str(line):
                account = line.strip().split("/")
                output.write(f"{account[0]}/{account[1]}\n")
                break

    if os.path.exists("nametoclaim.txt"):
        os.system("node claimnamemc.js")    


def set_window_title(title):
    if sys.platform.startswith("win"):
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        sys.stdout.write("\x1b]2;{}\x07".format(title))
        sys.stdout.flush()


def send_discord_webhook(webhook_url: str, message: str):
    webhook = DiscordWebhook(url=webhook_url, content=message)
    try:
        webhook.execute()
    except Exception as e:
        print(f"Error sending Discord webhook: {e}")


def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)
def load_proxies(filename):
    with open(filename, 'r') as f:
        raw_proxies = f.read().splitlines()
    parsed_proxies = []
    for proxy in raw_proxies:
        ip, port, username, password = proxy.split(':')
        parsed_proxies.append({
            'proxy_type': socks.HTTP,
            'host': ip,
            'port': int(port),
            'user': username,
            'pass': password
        })
    return parsed_proxies

def load_names(filename):
    with open(filename, 'r') as f:
        names = f.read().splitlines()
    return names



def process_names(names, accounts):
    global count, calcspeed, checktime, errorcount, tokencount
    name_iter = cycle(names)
    lock = Lock()
    delay_between_threads = 1

   # delay_between_threads = 0.0301  # Delay in seconds between starting threads

    timer = threading.Timer(0, lambda: None)  

    for account in accounts:
        account.target = next(name_iter)
        t = threading.Thread(target=account.turbo, args=(lock,))
        
       
        timer.cancel()  
        t.start()  
        timer = threading.Timer(delay_between_threads, t.start) 
        time.sleep(delay_between_threads)
        
        count += 1

    timer.cancel()  # Make sure the final timer gets canceled

        
        
       


    if(count%calcspeed==0):
        timetaken = time.time() - checktime
        rawspeed = calcspeed/timetaken
        speed = (calcspeed-errorcount)/timetaken
        checktime = time.time()
        send_discord_webhook("https://discord.com/api/webhooks/1217161572867379420/syH5GFsDh0IIfXlJx0PHQPXH42Z76m6EOE-_VHdlXuGiWPzgBS6ungYf5jXFYg7uW13c", f"Multiturbo is targeting {', '.join(names)} and reached {count} with {errorcount} errors({(errorcount/calcspeed*100):.3f}%)! Raw speed between {count-calcspeed} and {count} is {rawspeed:.3f}({(rawspeed/(len(names))):.3f}) and the real speed is {speed:.3f}({(speed/(len(names))):.3f}) claims/sec")
        errorcount = 0
        with open("timestamps.txt", "w") as file:
            pass
       
           
def auth_accounts():
    global authstatus, auth_time, tokens, token_iter
    print("Starting auth_accounts()")
    authstatus = True
    account_file = "accounts.txt"
    input_file = "input2.txt"
    with open(account_file, 'r') as source, open(input_file, 'w') as destination:
     contents = source.read()
     destination.write(contents)
    with open("tokens2go.txt", 'w') as file:
     file.truncate()
    ratelimit_file = "ratelimit.txt"
    with open(ratelimit_file, 'w') as file:
     file.truncate()
    print("REACHED THISSSSSSSSS")
    authenticate_accounts()
    while os.path.getsize(ratelimit_file) != 0:
     with open(ratelimit_file, 'r') as source, open(input_file, 'w') as destination:
      contents = source.read()
      destination.write(contents)
     with open(ratelimit_file, 'w') as file:
      file.truncate()
     authenticate_accounts()
    with open("tokens2go.txt", "r") as f:
        number_lines = sum(1 for line in f)
    send_discord_webhook("https://discord.com/api/webhooks/1217161338564902922/ERYAdjqmRa7SJV2ZLWaagCbznPNp9pjWDM6rCJg9hmV-gFuxdhHMH1Z1PsdinNPDYuYM", f"Finished Authentication process with {number_lines} tokens")

    with open("tokens2go.txt", 'r') as source, open("tokens.txt", 'w') as destination:
     contents = source.read()
     destination.write(contents)
    authstatus = False
    auth_time = int(time.time())
    with open(f"authtime.txt", "w") as file:
        file.write(f"{auth_time}\n")
    tokens = load_tokens("tokens.txt")
    token_iter = cycle(tokens)



def authenticate_accounts():
 input_file = "input2.txt"
 output_file = "tokens2.txt"
 with open(output_file, 'w') as file:
    file.truncate()
 ratelimit_file = "ratelimit.txt"
 nonpremium_file = "nonpremium.txt"
 count = 0
 successcount = 0
 ratelimits = 0
 with open(input_file, "r") as f:
        numberof_lines = sum(1 for line in f)
 
        send_discord_webhook("https://discord.com/api/webhooks/1217161338564902922/ERYAdjqmRa7SJV2ZLWaagCbznPNp9pjWDM6rCJg9hmV-gFuxdhHMH1Z1PsdinNPDYuYM", f"Authenticating {numberof_lines} accounts...")

 try:
    with open(input_file, "r") as file:
        with open(output_file, "a") as f:
            for line in file:
                credentials = line.strip().split("/")
                if len(credentials) != 2:
                    send_discord_webhook("https://discord.com/api/webhooks/1217161338564902922/ERYAdjqmRa7SJV2ZLWaagCbznPNp9pjWDM6rCJg9hmV-gFuxdhHMH1Z1PsdinNPDYuYM", f"Invalid credentials format: {line}")
                    continue

                email = credentials[0]
                password = credentials[1]

                try:
                    login = msmcauth.login(email, password)
                    bearer_token = login.access_token
                    send_discord_webhook("https://discord.com/api/webhooks/1217161338564902922/ERYAdjqmRa7SJV2ZLWaagCbznPNp9pjWDM6rCJg9hmV-gFuxdhHMH1Z1PsdinNPDYuYM", f"[{count}] Successfully logged into {email}")
                    successcount += 1
                    f.write(f"{bearer_token}: {email}\n")
                    count += 1
                    time.sleep(7)
                    continue
                except Exception as e:
                    
                    send_discord_webhook("https://discord.com/api/webhooks/1217161338564902922/ERYAdjqmRa7SJV2ZLWaagCbznPNp9pjWDM6rCJg9hmV-gFuxdhHMH1Z1PsdinNPDYuYM", f"[{count}] Failed logged into {email}: {str(e)}")
                    
                    count +=1
                    if(str(e) == "LoginWithXbox Authentication failed."):
                       with open(ratelimit_file, "a") as errorfile:
                        errorfile.write(f"{email}/{password}\n")
                        ratelimits +=1
                       time.sleep(10) 
                    elif(str(e) == "Account is not premium."):
                       with open(nonpremium_file, "a") as nonpremiumfile:
                        nonpremiumfile.write(f"{email}\n")    
                    elif(str(e) == "Provided credentials was invalid."):
                       continue
                    else:
                     with open("othererrors.txt", "a") as othererrorsfile:
                        othererrorsfile.write(f"{email}/{password}\n")   
                        continue                   

                    time.sleep(10)   
                    continue

 
    send_discord_webhook("https://discord.com/api/webhooks/1217161338564902922/ERYAdjqmRa7SJV2ZLWaagCbznPNp9pjWDM6rCJg9hmV-gFuxdhHMH1Z1PsdinNPDYuYM", f"{successcount} session tokens saved in tokens2.txt with {ratelimits} ratelimits.")
 except FileNotFoundError:
    
    send_discord_webhook("https://discord.com/api/webhooks/1217161338564902922/ERYAdjqmRa7SJV2ZLWaagCbznPNp9pjWDM6rCJg9hmV-gFuxdhHMH1Z1PsdinNPDYuYM", f"Input file '{input_file}' not found.")
 except Exception as e:
      
    send_discord_webhook("https://discord.com/api/webhooks/1217161338564902922/ERYAdjqmRa7SJV2ZLWaagCbznPNp9pjWDM6rCJg9hmV-gFuxdhHMH1Z1PsdinNPDYuYM", f"An error occurred: {str(e)}")
 destination_file = 'tokens2go.txt'

 with open(output_file, 'r') as source, open(destination_file, 'a') as destination:
    contents = source.read()
    destination.write(contents)



def load_tokens(filename):
    with open(filename, 'r') as f:
        raw_tokens = f.read().splitlines()
    return raw_tokens


def main():
    global accounts, proxy_iter, token_iter, sockets_available, num_names, tokencount, auth_time, authstatus, tokens
    accounts = []
    proxies = load_proxies("proxies.txt")
    tokens = load_tokens("tokens.txt")
    tokencount = len(tokens)
    proxy_iter = cycle(proxies)
    token_iter = cycle(tokens)  
    sockets_available = len(proxies)
    names = load_names("names.txt")
    webhook_url = "https://discord.com/api/webhooks/1217161572867379420/syH5GFsDh0IIfXlJx0PHQPXH42Z76m6EOE-_VHdlXuGiWPzgBS6ungYf5jXFYg7uW13c"  
    send_discord_webhook(webhook_url, f"Sniper started. Targeting the following names: {', '.join(names)}")
    num_names = len(names)
    startmin = datetime.now().strftime("%H:%M:%S")
    set_window_title(f"Multiturbo - Tokens: {len(tokens)}, Proxies: {len(proxies)}. Sniper started at {startmin}")

    if len(tokens) == 0:
        print(f"No valid tokens found in tokens.txt.")
        return
    print(f"""{Fore.MAGENTA}

  _____    ___    ____    _   _   _____   _   _   ____    ____     ___  
 |  ___|  / _ \  / ___|  | | | | |_   _| | | | | |  _ \  | __ )   / _ \ 
 | |_    | | | | \___ \  | |_| |   | |   | | | | | |_) | |  _ \  | | | |
 |  _|   | |_| |  ___) | |  _  |   | |   | |_| | |  _ <  | |_) | | |_| |
 |_|      \___/  |____/  |_| |_|   |_|    \___/  |_| \_\ |____/   \___/ 
                                                                        


""")

    print(f"{Fore.GREEN}Loaded {len(tokens)} Minecraft tokens.")
    auth_time_input = input("Enter the last Authtime or enter n(current time) or a(autocalculate): ")
    if auth_time_input.lower() == 'n':
        auth_time = time.time()
        print(f"Authtime = {auth_time}")
    elif auth_time_input.lower() == 'a':
        with open('authtime.txt', 'r') as file:
         auth_time = int(file.readline())
         print(f"Authtime = {auth_time}")

    else:
        auth_time = int(auth_time_input)
        print(f"Authenticating at specified time and targeting {', '.join(names)}")
    
    while True:
        if (time.time() > (auth_time + int(79200))) and not(authstatus):
           print("STARTED AUTHENTICATION PROCESS------------------------------------------------")
           auth_thread = threading.Thread(target=auth_accounts)
           auth_thread.start()
   

        
        
        for token, proxy in zip(token_iter, proxies):  
            
             bearer, email = token.split(': ')
             account = MicrosoftAccount(bearer, email, "", proxy)  
             accounts.append(account)

       
        process_names(names, accounts)
        print("Cycle finished running. Starting new cycle.")
        accounts = []  # clear accs for next cycle




if __name__ == "__main__":
    main()