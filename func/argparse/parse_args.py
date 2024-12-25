import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Advanced WordPress Security Testing Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    required = parser.add_argument_group('Required Arguments')
    required.add_argument(
        "-wu", "--usernames", required=True, 
        help="Path to the file containing usernames to be tested.\nExample: 'usernames.txt'"
    )
    required.add_argument(
        "-wp", "--passwords", required=True, 
        help="Path to the file containing passwords to be tested.\nExample: 'passwords.txt'"
    )
    required.add_argument(
        "-u", "--url", required=True, 
        help="Target WordPress URL for security testing.\nExample: 'http://example.com/wp-login.php'"
    )
    
    auth = parser.add_argument_group('Authentication Options')
    auth.add_argument(
        "-m", "--mode", type=int, choices=[1, 2, 3, 4], default=1, 
        help="""Testing mode:
        1 = User-first (test each username with all passwords)
        2 = Pass-first (test each password with all usernames)
        3 = Alternating (test username and password alternately)
        4 = Random (random username-password combinations)""")
    auth.add_argument(
        "--custom-login-path", 
        help="Custom WordPress login path.\nExample: 'http://example.com/custom-login.php'"
    )
    auth.add_argument(
        "--xmlrpc", action="store_true", 
        help="Use XML-RPC interface for login attempts instead of the default login form."
    )
    auth.add_argument(
        "--timeout", type=float, default=10.0, 
        help="Request timeout in seconds. Adjust if facing slow server responses.\nDefault: 10 seconds"
    )
    
    # Performance options
    performance = parser.add_argument_group('Performance Options')
    performance.add_argument(
        "-t", "--threads", type=int, default=5, 
        help="Number of concurrent threads for performing login attempts.\nDefault: 5 threads"
    )
    performance.add_argument(
        "--delay", type=float, default=0, 
        help="Delay between requests in seconds to avoid triggering security mechanisms.\nDefault: 0 seconds"
    )
    performance.add_argument(
        "--batch-size", type=int, default=100, 
        help="Number of requests per batch to be sent concurrently.\nDefault: 100"
    )
    performance.add_argument(
        "--max-retries", type=int, default=3, 
        help="Maximum number of retry attempts per failed request.\nDefault: 3 retries"
    )
    
    # Output options
    output = parser.add_argument_group('Output Options')
    output.add_argument(
        "--output", 
        help="Path to the output file where valid credentials will be saved.\nExample: 'found_credentials.txt'"
    )
    output.add_argument(
        "--log-file", default="wp_security_test.log", 
        help="Log file path to record test execution details.\nDefault: 'wp_security_test.log'"
    )
    output.add_argument(
        "--debug", action="store_true",
        help="Enable debug mode for detailed logging. Overrides log level to DEBUG."
    )
    output.add_argument(
        "-v", "--verbose", action="store_true", 
        help="Enable verbose output for detailed information on each login attempt."
    )
    output.add_argument(
        "--silent", action="store_true", 
        help="Silent mode: Only display valid credentials found, suppress all other output."
    )
    
    # Advanced options
    advanced = parser.add_argument_group('Advanced Options')
    advanced.add_argument(
        "--user-agent", 
        help="Custom User-Agent string to use during the tests.\nExample: 'Mozilla/5.0...'"
    )
    advanced.add_argument(
        "--proxy", 
        help="Proxy URL (e.g., socks5://127.0.0.1:9050) to route requests through."
    )
    advanced.add_argument(
        "--verify-ssl", action="store_true", 
        help="Verify SSL certificates when making requests (useful for secure connections)."
    )
    advanced.add_argument(
        "--force-ssl", action="store_true", 
        help="Force HTTPS connection even if the server does not support SSL."
    )
    advanced.add_argument(
        "--random-agent", action="store_true", 
        help="Use a random User-Agent string for each request to avoid detection."
    )
    advanced.add_argument(
        "--exit-on-found", action="store_true", 
        help="Exit the tool immediately after the first valid credential is found."
    )
    
    return parser.parse_args()