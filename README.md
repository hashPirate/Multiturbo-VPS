# Multiturbo-VPS
Completely automated Minecraft Turbo designed to be run on a VPS

# Info
This project was incredibly successful and lucrative. The code has not been worked recently but is up to date. I do not snipe anymore so I am publishing my code publicly. You are free to use it as you please without the need to give me credit. I have not made this project easy to use. This is just the raw code.

# Features
- Customizable delays and requests
- Can be run for weeks at a time without any input from the user. Reauthenticates the accounts with custom delays and will post updates to a discord webhook. (I have left my dead discord webhooks in the code. Replace them with your own)
- Multithreaded and can run at a maximum speed of 1000 rq/s although you would need 3000 accounts to avoid a ratelimit.
- Can provide updates to a discord webhook with automatic speed calculation so that you can verify it is running at the desired speed.
- Cycles through various token proxy pairs to avoid a ratelimit and also contains a ratelimit bypass when using giftcode accounts.
- Counts errors and notifies you if there are proxy errors.
- Automatically changes your skin to a desired skin and uses Javascript to claim the namemc page of the name.
- Ensures multithreaded requests are printed on separate lines using thread locks.
# Usage
- Install all the required modules.
- Create an accounts.txt file hosting your accounts in the format email/password. For this to work well you want at least 20. This will only work with giftcode accounts because of the rl bypass.
- Create a proxies.txt file containing your HTTP/HTTPS proxies in the format ip:port:username:password. I've found that webshare proxies work well for this purpose.
- Change delay_between_threads to your desired amount.
- Create a names.txt file to host the desired names to target.
- Replace all discord webhooks with your custom webhooks!



