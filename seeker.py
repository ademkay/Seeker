import os, time, random, requests, smtplib, socket, re
from googlesearch import search
from email_variants import gen_email_variants
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import pdb
#os.system("sudo systemctl restart postfix") #for your own SMTP server

# COLOURS FOR TEXT:

class colour:
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    White = "\u001b[37m"
    Red = "\u001b[31m"

os.system('cls' if os.name == 'nt' else 'clear')
print(colour.Magenta + "\033[1m▒▒▒▒▒ SEEKER ▒▒▒▒▒\033[0m")
print()

# FUNCTIONS:

def input_name():
    firstname = input("\033[1mFirst name: \033[0m")
    lastname = input("\033[1mLast name: \033[0m")
    domain = input("\033[1mDomain: \033[0m")
    return firstname, lastname, domain

def save_to_file(strings, filename):
    with open(filename, 'a') as file:
        for s in strings:
            file.write(s + '\n')

# SEARCH

def search_google(query):
    url_list = []
    for result in search(query):
        url_list.append(result)
    return url_list

def domain_parser(query):
    soup = BeautifulSoup(query.content, "html.parser")
    single_url_mail_list = [] # addresses from single URL
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b'
    for link in soup.find_all("a"):
        text = link.get_text()
        matches = re.findall(email_regex, text)
        for match in matches:
            single_url_mail_list.append(match)
    return single_url_mail_list

def search_email(domain):
    try:
        public_domains = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "zoho.com", "zohomail.eu","protonmail.com","proton.me","icloud.com","mail.com","mail.ru","yandex.ru","ukr.net"]
        if domain in public_domains:
            print("lol okay good luck with it")
            return
        else:
            request = f'"{domain}"'
            url_list = search_google(request)
            print ("\033[1mURLs: \033[0m", end="\n\n")
            save_to_file([f"Results for {domain}:"], "search_log.txt")
            save_to_file(["URLs:"], "search_log.txt")
            for num, result in enumerate(url_list, start=1):
                print(f"\033[1m{num}.\033[0m {result}")
                save_to_file([f"{num}. {result}"], "search_log.txt")
            print()
            print("\033[1mGetting e-mails. Please wait...\033[0m", end="\n\n")
            unfiltered_general_mail_list = [] # addresses from all URLs
            for result in url_list:
                single_url_mail_list = domain_parser(requests.get(result))
                unfiltered_general_mail_list.extend(single_url_mail_list)
            unique_only_general_list = list(set(unfiltered_general_mail_list)) # only unique addresses from all URLs
            print("\033[1mMails:\033[0m", end="\n\n")
            save_to_file(["Mails:"], "search_log.txt")
            for num, result in enumerate(unique_only_general_list, start=1): # final output, printing unique mail list
                print(f"\033[1m{num}. \033[0m {result}")
                save_to_file([f"{num}. {result}"], "search_log.txt")
            print()
            save_to_file("\n", "search_log.txt")

    except Exception as e:
        print(f"Error for {domain}: {e}")

# VALIDATE

smtplib.SMTP.debuglevel = 0

def validate_email_variants(firstname, lastname, domain):
    try:
        email_variants = gen_email_variants(firstname, lastname, domain)
        for email in email_variants:
            if validate_email(email):
                print(email + colour.Green + "\033[1m is valid.\033[0m")
            else:
                print(email + colour.Red + "\033[1m is not valid.\033[0m")
    except Exception as e:
        print(f"Error: {e}")

def validate_single_email(email):
    try:
        if validate_email(email):
            print(email + colour.Green + "\033[1m is valid.\033[0m")
        else:
            print(email + colour.Red + "\033[1m is not valid.\033[0m")
    except Exception as e:
        print(f"Error: {e}")

def validate_email(email):
    try:
        sender = open("sender.txt").readline().strip()
        password = open("password.txt").readline().strip()
        smtp_server = open("smtp_server.txt").readline().strip()
        recipient = email
        port = 587
        msg = MIMEText("test")
        msg["Subject"] = "test"
        msg["From"] = sender
        msg["To"] = recipient
        try:
            with smtplib.SMTP(smtp_server, port) as server: #"localhost" for your own server | smtp_server, port for existing one
                server.starttls()
                server.login(sender, password)
                response_code, _ = server.sendmail(sender, [recipient], msg.as_string())
                if response_code == 250:
                    return True
                if response_code != 250:
                    print("Response code is not 250")
                print(f"Connection to {smtp_server}:{port} closed")
                server.quit()
        except smtplib.SMTPException as smtp_exc:
            print(f"SMTP Exception: {smtp_exc}")
        except socket.error as socket_err:
            print(f"Socket Error during connection: {socket_err}")
        except Exception as e:
            print(f"Error: {e}")
    except IOError as io_err:
        print(f"IO Error: {io_err}")
    except Exception as e:
        print(f"Error: {e}")

# MAIN MENU:

def main_menu():
    print(colour.Yellow + "\033[1mMain menu:\033[0m")
    print(colour.Yellow + "\033[1m[1] - Email list based on domain (Search engine parsing)\033[0m")
    print(colour.Yellow + "\033[1m[2] - Email validation based on name and domain (SMTP validation)\033[0m")
    print(colour.Yellow + "\033[1m[3] - Single email validation (SMTP validation)\033[0m")
    print(colour.Yellow + "\033[1m[0] - Exit\033[0m")
    print()
    print(colour.Yellow + "\033[1m[i] - Instructions\033[0m")
    print()

    choise = input(colour.Yellow + "\033[1m=> \033[0m")

    if choise == "1":
        domain = input("\033[1mEnter domain (like example.com): \033[0m")
        search_email(domain)
        main_menu()

    if choise == "2":
        print("\033[1mOption wasn't tested properly because of public SMTP server's restrictions\033[0m")
        firstname, lastname, domain = input_name()
        validate_email_variants(firstname, lastname, domain)
        main_menu()

    if choise == "3":
        print("\033[1mOption wasn't tested properly because of public SMTP server's restrictions\033[0m")
        email = input("\033[1mEnter email (name@example.com): \033[0m")
        validate_single_email(email)
        main_menu()

    if choise == "0":
        print("\033[1mGoodbye!\033[0m")
        exit()

    if choise == "i":
        print("\033[1m!THE PROGRAM IS UNDER DEVELOPMENT!\033[0m")
        print("\033[1mBoolean search for your target's mail.\033[0m")
        print("\033[1mSMTP server verification for your target's mail.\033[0m")
        print("\033[1mFor options " + colour.Yellow + "'2'" + colour.White + " and " + colour.Yellow + "'3'" + colour.White + ": please enter your (sender's) email to " + colour.Yellow + "'sender.txt'" + colour.White + ", password to " + colour.Yellow + "'password.txt'" + colour.White + ", sender's SMTP server address to " + colour.Yellow + "'smtp_server.txt'\033[0m")
        print("\033[1mEnter " + colour.Yellow + "'M'" + colour.White + " to return to main menu.\033[0m")
        key = input(colour.Yellow + "\033[1m=> \033[0m")
        if key == "m":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colour.Magenta + "\033[1m▒▒▒▒▒ SEEKER ▒▒▒▒▒\033[0m")
            print()
            main_menu()

    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colour.Magenta + "\033[1m▒▒▒▒▒ SEEKER ▒▒▒▒▒\033[0m")
        print()
        main_menu()

# STARTING SCRIPT:

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        main_menu()