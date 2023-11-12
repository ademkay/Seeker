import os
import re
import requests
# import smtplib
# import socket
import sys
# from email.mime.text import MIMEText

# from email_variants import gen_email_variants
# from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from googlesearch import search

# from email_variants import gen_email_variants


# import pdb
# os.system("sudo systemctl restart postfix") # for your own SMTP server

# COLOURS FOR TEXT:

class Colour:
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    White = "\u001b[37m"
    Red = "\u001b[31m"


def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colour.Magenta + "\033[1m▒▒▒▒▒ SEEKER ▒▒▒▒▒\033[0m")
    print()


# FUNCTIONS:

'''def input_name():
    firstname = input("\033[1mFirst name: \033[0m")
    lastname = input("\033[1mLast name: \033[0m")
    domain = input("\033[1mDomain: \033[0m")
    return firstname, lastname, domain'''


def save_to_file(strings, filename):
    with open(filename, 'a') as file:
        for s in strings:
            file.write(s + '\n')


# SEARCH:

def search_google(query):
    with open("search_mode.txt", 'r') as file:
        search_mode = file.readline()

    if search_mode == "no_g_api":  # usual Google search
        url_list = []
        print("\033[1mGetting URLs...\033[0m", end="\n\n")
        for result in search(query):
            url_list.append(result)
        return url_list

    if search_mode == "g_api":  # search with Google API. Fewer restrictions but tied to your account (will find same results on any OS)
        with open("google_api/google_api_key.txt", "r", encoding="utf-8") as file:
            api_key = file.read()
        with open("google_api/google_se_id.txt", "r", encoding="utf-8") as file:
            search_engine_id = file.read()
        search_url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': query
        }
        response = requests.get(search_url, params=params)

        # results
        url_list = []
        print("\033[1mGetting URLs...\033[0m", end="\n\n")
        if response.status_code == 200:
            data = response.json()
            links = [item.get("link") for item in data.get('items', [])]
            for link in links:
                url_list.append(link)
        else:
            print(f"error sending request: {response.status_code}")
        return url_list


def email_parser(query):
    soup = BeautifulSoup(query.content, "html5lib")
    email_list = []  # addresses from single URL
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b'
    for link in soup.find_all():
        text = link.get_text()
        matches = re.findall(email_regex, text)
        for match in matches:
            img_regex_list = [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.png\b',
                              r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.jpg\b',
                              r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.jpeg\b',
                              r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.bmp\b',
                              r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.tga\b',
                              r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.svg\b']
            wrong_matches = [re.search(regex, text) for regex in img_regex_list]
            wrong_matches = [match.group() for match in wrong_matches if match]
            if match not in wrong_matches:
                email_list.append((match, query.url))
    return email_list


def search_email(keyword):
    try:
        public_domains = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "zoho.com", "zohomail.eu",
                          "protonmail.com", "proton.me", "icloud.com", "mail.com", "mail.ru", "yandex.ru", "ukr.net"]
        if keyword in public_domains:
            print("lol okay good luck with it")
            return
        else:
            request = f'"{keyword}"'

            url_list = search_google(request)

            print("\033[1mURLs: \033[0m", end="\n\n")
            save_to_file([f"Results for {keyword}:"], "search_log.txt")  # saving everything into .txt log
            save_to_file(["URLs:"], "search_log.txt")
            for num, result in enumerate(url_list, start=1):
                print(f"\033[1m{num}.\033[0m {result}")
                save_to_file([f"{num}. {result}"], "search_log.txt")
            print()
            print("\033[1mGetting e-mails. Please wait...\033[0m", end="\n\n")
            emails_with_sources = {}
            for result in url_list:
                try:
                    email_data = email_parser(requests.get(result))
                    for email, source in email_data:
                        if email in emails_with_sources:
                            if source not in emails_with_sources[email]:
                                emails_with_sources[email].append(source)
                        else:
                            emails_with_sources[email] = [source]
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching URL {result}: {e}")
                    # pass
            print("\033[1mMails:\033[0m", end="\n\n")
            save_to_file(["Mails:"], "search_log.txt")
            if emails_with_sources:
                for num, (email, sources) in enumerate(emails_with_sources.items(), start=1):
                    email_sources_str = ', '.join(sources)
                    print(f"\033[1m{num}. \033[0m {email} (Source(s): {email_sources_str} )")
                    save_to_file([f"{num}. {email} (Source(s): {email_sources_str} )"], "search_log.txt")
            else:
                print("No email addresses found for this request.")
                save_to_file(["No email addresses found for this request."], "search_log.txt")
            print()
            print("\033[1mSearch finished, check 'search_log.txt'\033[0m", end="\n\n")
            save_to_file("\n", "search_log.txt")
    except Exception as e:
        print(f"Error for {keyword}: {e}")


# VALIDATE:

'''smtplib.SMTP.debuglevel = 0


def validate_email_variants(firstname, lastname, domain):
    try:
        email_variants = gen_email_variants(firstname, lastname, domain)
        for email in email_variants:  # going through different variants of name and surname composing
            if validate_email(email):
                print(email + Colour.Green + "\033[1m is valid.\033[0m")
            else:
                print(email + Colour.Red + "\033[1m is not valid.\033[0m")
    except Exception as e:
        print(f"Error: {e}")


def validate_single_email(email):
    try:
        if validate_email(email):
            print(email + Colour.Green + "\033[1m is valid.\033[0m")
        else:
            print(email + Colour.Red + "\033[1m is not valid.\033[0m")
    except Exception as e:
        print(f"Error: {e}")


def validate_email(email):  # key email validation function
    try:
        sender = open("smtp/sender.txt").readline().strip()
        password = open("smtp/password.txt").readline().strip()
        smtp_server = open("smtp/smtp_server.txt").readline().strip()
        recipient = email
        port = 587
        msg = MIMEText("test")  # creating a test message
        msg["Subject"] = "test"
        msg["From"] = sender
        msg["To"] = recipient
        try:
            with smtplib.SMTP(smtp_server,
                              port) as server:  # "localhost" for your own server | smtp_server, port for existing one
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
        print(f"Error: {e}")'''


# MAIN MENU:

def main_menu():
    try:
        print(Colour.Yellow + "\033[1mMain menu:\033[0m")
        print(Colour.Yellow + "\033[1m[1] - Email list based on keyword (Search engine parsing)\033[0m")
        # print(Colour.Yellow + "\033[1m[2] - Email validation based on name and domain (SMTP validation)\033[0m")
        # print(Colour.Yellow + "\033[1m[3] - Single email validation (SMTP validation)\033[0m")
        print(Colour.Yellow + "\033[1m[0] - Exit\033[0m")
        print()
        print(Colour.Yellow + "\033[1m[s] - Switch email search mode\033[0m")
        print(Colour.Yellow + "\033[1m[i] - Instructions\033[0m")
        print()

        choice = input(Colour.Yellow + "\033[1m=> \033[0m")

        if choice == "1":
            keyword = input("\033[1mEnter keyword (for example 'example.com'): \033[0m")
            search_email(keyword)
            main_menu()

        '''elif choice == "2":
            print("\033[1mOption wasn't tested properly because of public SMTP server's restrictions\033[0m")
            firstname, lastname, domain = input_name()
            validate_email_variants(firstname, lastname, domain)
            main_menu()

        elif choice == "3":
            print("\033[1mOption wasn't tested properly because of public SMTP server's restrictions\033[0m")
            email = input("\033[1mEnter email (name@example.com): \033[0m")
            validate_single_email(email)
            main_menu()'''

        if choice == "0":
            print("\033[1mGoodbye!\033[0m")
            sys.exit()

        elif choice == "s":
            print("\033[1mSelect search mode:\033[0m")
            print(Colour.Yellow + "\033[1m'1'" + Colour.White + " - Usual Google search\033[0m")
            print(
                Colour.Yellow + "\033[1m'2'" + Colour.White + "- Google API search (if you have API key and SE "
                                                              "ID)\033[0m")
            print(Colour.Yellow + "\033[1m'Enter'" + Colour.White + " to return to main menu.\033[0m")
            key = input(Colour.Yellow + "\033[1m=> \033[0m")
            if key == "1":
                with open("search_mode.txt", 'w') as file:
                    file.write('no_g_api')
                logo()
                print("\033[1mUsual Google search selected.\033[0m")
                main_menu()
            if key == "2":
                with open("search_mode.txt", 'w') as file:
                    file.write('g_api')
                logo()
                print("\033[1mGoogle API search selected.\033[0m")
                main_menu()
            else:
                logo()
                main_menu()

        elif choice == "i":
            print("\033[1mBoolean search for your target's mail.\033[0m")
            '''print("\033[1mSMTP server verification for your target's mail.\033[0m")
            print(
                "\033[1mFor options " + Colour.Yellow + "'2'" + Colour.White + " and " + Colour.Yellow + "'3'" + Colour.White + ": please enter your (sender's) email to " + Colour.Yellow + "'sender.txt'" + Colour.White + ", password to " + Colour.Yellow + "'password.txt'" + Colour.White + ", sender's SMTP server address to " + Colour.Yellow + "'smtp_server.txt'\033[0m")'''
            print(Colour.Yellow + "\033[1m'Enter'" + Colour.White + " to return to main menu.\033[0m")
            input(Colour.Yellow + "\033[1m=> \033[0m")
            logo()
            main_menu()

        else:
            logo()
            main_menu()
    except KeyboardInterrupt:
        logo()
        print("Script interrupted by user.")
        main_menu()


# STARTING SCRIPT:

if __name__ == "__main__":
    logo()
    main_menu()
