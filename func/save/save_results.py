from datetime import datetime


def save_results(credentials, output_file):
    with open(output_file, 'w') as f:
        f.write(f"WordPress Security Test Results - {datetime.now()}\n")
        f.write("-" * 50 + "\n")
        for username, password in credentials:
            f.write(f"Username: {username}\nPassword: {password}\n")
            f.write("-" * 50 + "\n")