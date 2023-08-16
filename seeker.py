import os, time, random, requests, subprocess, webbrowser, psutil
from googlesearch import search
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup

# COLOURS FOR TEXT

class colour:
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    White = "\u001b[37m"

os.system("clear")
print(colour.Magenta + "\033[1m▒▒▒▒▒ SEEKER ▒▒▒▒▒\033[0m")
print()

# USER AGENTS FOR TOR

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.47",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36 Edge/15.14977",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.47",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36 Edge/15.14977",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/100.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
]

# FUNCTIONS

def save_to_file(strings, filename):
        with open(filename, 'a') as file:
            for s in strings:
                file.write(s + '\n')

def tor_path_txt():
    with open('tor_path.txt', 'r') as file:
        return file.read().strip()

def start_tor_browser():
    tor_browser_path = tor_path_txt()
    # subprocess.run(['xdg-open', tor_browser_path], shell=True)
    webbrowser.open(tor_browser_path)

def stop_tor_browser():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if "tor-browser" in proc.info['name']:
            try:
                os.kill(proc.info['pid'], signal.SIGTERM)
            except:
                pass

def restart_tor():
    subprocess.run(["sudo", "service", "tor", "restart"])

def renew_tor_ip():
    TOR_CONTROL_PORT = 9051
    with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    time.sleep(random.uniform(1, 2))

def input_name():
    firstname = input("\033[1mFirst name: \033[0m")
    lastname = input("\033[1mLast name: \033[0m")
    domain = input("\033[1mDomain: \033[0m")
    restart_tor()
    search_email_variants(firstname, lastname, domain)
    restart_tor()

def search_duckduckgo(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": random.choice(user_agents)}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    search_results = []
    for result in soup.select(".result__url"):
        search_results.append(result.text)
    return search_results

def search_email(email):
    try:
        request = f'"{email}"'
        renew_tor_ip()
        search_result = search_duckduckgo(request)
        result_qty = len(search_result)
        print(f"\033[1mTotal results for {email}\033[0m: {result_qty}")
        # save_to_file([f"Result for {email}:", ""] + search_result + [""], "search_log.txt")
        if result_qty > 0:
            save_to_file([f"Result for {email}:"], "search_log.txt")
            for result in search_result:
                save_to_file([result], "search_log.txt")
            save_to_file([], "search_log.txt")
        time.sleep(random.uniform(3, 4))
    except Exception as e:
        print(f"An error occurred while searching for {email}: {e}")

def search_email_variants(firstname, lastname, domain):
    email_variants = [

    # REGULAR

        f"{firstname}.{lastname}@{domain}", #firstname.lastname@test.com
        f"{firstname[0]}.{lastname}@{domain}", #f.lastname@test.com
        f"{firstname}.{lastname[0]}@{domain}", #firstname.l@test.com

        f"{firstname}-{lastname}@{domain}", #firstname-lastname@test.com
        f"{firstname[0]}-{lastname}@{domain}", #f-lastname@test.com
        f"{firstname}-{lastname[0]}@{domain}", #firstname-l@test.com

        f"{firstname}_{lastname}@{domain}", #firstname_lastname@test.com
        f"{firstname[0]}_{lastname}@{domain}", #f_lastname@test.com
        f"{firstname}_{lastname[0]}@{domain}", #firstname_l@test.com

        f"{firstname}{lastname}@{domain}", #firstnamelastname@test.com
        f"{firstname[0]}{lastname}@{domain}", #flastname@test.com
        f"{firstname}{lastname[0]}@{domain}", #fistnamel@test.com

        f"{lastname}.{firstname}@{domain}", #lastname.firstname@test.com
        f"{lastname[0]}.{firstname}@{domain}", #l.firstname@test.com
        f"{lastname}.{firstname[0]}@{domain}", #lastname.f@test.com

        f"{lastname}-{firstname}@{domain}", #lastname-firstname@test.com
        f"{lastname[0]}-{firstname}@{domain}", #l-firstname@test.com
        f"{lastname}-{firstname[0]}@{domain}", #lastname-f@test.com

        f"{lastname}_{firstname}@{domain}", #lastname_firstname@test.com
        f"{lastname[0]}_{firstname}@{domain}", #l_firstname@test.com
        f"{lastname}_{firstname[0]}@{domain}", #lastname_f@test.com

        f"{lastname}{firstname}@{domain}", #lastnamefirstname@test.com
        f"{lastname[0]}{firstname}@{domain}", #lfirstname@test.com
        f"{lastname}{firstname[0]}@{domain}", #lastnamef@test.com

        f"{firstname}@{domain}", #firstname@test.com
        f"{lastname}@{domain}", #lastname@test.com

    # DOUBLE LAST CHARACTER

        f"{firstname}{firstname[-1]}.{lastname}@{domain}", #firstnamee.lastname@test.com
        f"{firstname}.{lastname}{lastname[-1]}@{domain}", #firstname.lastnamee@test.com
        f"{firstname}{firstname[-1]}.{lastname}{lastname[-1]}@{domain}", #firstnamee.lastname@test.com
        f"{firstname}{firstname[-1]}.{lastname[0]}@{domain}", #firstnamee.l@test.com

        f"{firstname}{firstname[-1]}-{lastname}@{domain}", #firstnamee-lastname@test.com
        f"{firstname}-{lastname}{lastname[-1]}@{domain}", #firstname-lastnamee@test.com
        f"{firstname}{firstname[-1]}-{lastname}{lastname[-1]}@{domain}", #firstnamee-lastname@test.com
        f"{firstname}{firstname[-1]}-{lastname[0]}@{domain}", #firstnamee-l@test.com

        f"{firstname}{firstname[-1]}_{lastname}@{domain}", #firstnamee_lastname@test.com
        f"{firstname}_{lastname}{lastname[-1]}@{domain}", #firstname_lastnamee@test.com
        f"{firstname}{firstname[-1]}_{lastname}{lastname[-1]}@{domain}", #firstnamee_lastname@test.com
        f"{firstname}{firstname[-1]}_{lastname[0]}@{domain}", #firstnamee_l@test.com

        f"{firstname}{firstname[-1]}{lastname}@{domain}", #firstnameelastname@test.com
        f"{firstname}{lastname}{lastname[-1]}@{domain}", #firstnamelastnamee@test.com
        f"{firstname}{firstname[-1]}{lastname}{lastname[-1]}@{domain}", #firstnameelastnamee@test.com
        f"{firstname}{firstname[-1]}{lastname[0]}@{domain}", #fistnameel@test.com

        f"{lastname}.{firstname}{firstname[-1]}@{domain}", #lastname.firstnamee@test.com
        f"{lastname}{lastname[-1]}.{firstname}@{domain}", #lastnamee.firstname@test.com
        f"{lastname}{lastname[-1]}.{firstname}{firstname[-1]}@{domain}", #lastnamee.firstnamee@test.com
        f"{lastname}{lastname[-1]}.{firstname[0]}@{domain}", #lastnamee.f@test.com

        f"{lastname}-{firstname}{firstname[-1]}@{domain}", #lastname-firstnamee@test.com
        f"{lastname}{lastname[-1]}-{firstname}@{domain}", #lastnamee-firstname@test.com
        f"{lastname}{lastname[-1]}-{firstname}{firstname[-1]}@{domain}", #lastnamee-firstnamee@test.com
        f"{lastname[0]}-{firstname}{firstname[-1]}@{domain}", #l-firstnamee@test.com

        f"{lastname}_{firstname}{firstname[-1]}@{domain}", #lastname_firstnamee@test.com
        f"{lastname}{lastname[-1]}_{firstname}@{domain}", #lastnamee_firstname@test.com
        f"{lastname}{lastname[-1]}_{firstname}{firstname[-1]}@{domain}", #lastnamee_firstnamee@test.com
        f"{lastname[0]}_{firstname}{firstname[-1]}@{domain}", #l_firstname@test.com

        f"{lastname}{firstname}{firstname[-1]}@{domain}", #lastnamefirstnamee@test.com
        f"{lastname}{lastname[-1]}{firstname}@{domain}", #lastnameefirstname@test.com
        f"{lastname}{lastname[-1]}{firstname}{firstname[-1]}@{domain}", #lastnameefirstnamee@test.com
        f"{lastname[0]}{firstname}{firstname[-1]}@{domain}", #lfirstnamee@test.com

        f"{firstname}{firstname[-1]}@{domain}", #firstnamee@test.com
        f"{lastname}{lastname[-1]}@{domain}", #lastnamee@test.com

    # FIRST CHARACTER ONLY

        f"{firstname[0]}.{lastname[0]}@{domain}", #f.l@test.com
        f"{lastname[0]}.{firstname[0]}@{domain}", #l.f@test.com

        f"{firstname[0]}-{lastname[0]}@{domain}", #f-l@test.com
        f"{lastname[0]}-{firstname[0]}@{domain}", #l-f@test.com

        f"{firstname[0]}_{lastname[0]}@{domain}", #f_l@test.com
        f"{lastname[0]}_{firstname[0]}@{domain}", #l_f@test.com

        f"{firstname[0]}{lastname[0]}@{domain}", #fl@test.com
        f"{lastname[0]}{firstname[0]}@{domain}", #lf@test.com

        f"{firstname[0]}@{domain}", #f@test.com
        f"{lastname[0]}@{domain}", #l@test.com

    # DOMAIN ONLY

        f"@{domain}" #@test.com
    ]
    for email in email_variants:
        search_email(email)

# MAIN MENU

def main_menu():
    print(colour.Yellow + "\033[1mMain menu:\033[0m")
    print(colour.Yellow + "\033[1m[1] - Email finder\033[0m")
    print(colour.Yellow + "\033[1m[0] - Exit\033[0m")
    print()
    print(colour.Yellow + "\033[1m[i] - Instructions\033[0m")
    print()

    choise = input(colour.Yellow + "\033[1m=> \033[0m")

    if choise == "1":
        start_tor_browser()
        input_name()
        stop_tor_browser()
        main_menu()

    if choise == "0":
        print("\033[1mGoodbye!\033[0m")
        exit()

    if choise == "i":
        print("\033[1m!THE PROGRAM IS UNDER DEVELOPMENT!\033[0m")
        print("\033[1mBoolean search for your target's mail.\033[0m")
        print("\033[1mBefore usage wait until Tor browser is started and connected.\033[0m")
        print("\033[1mLinks will be saved to 'search_log.txt'.\033[0m")
        print("\033[1mEnter " + colour.Yellow + "'M'" + colour.White + " to return to main menu.\033[0m")
        key = input(colour.Yellow + "\033[1m=> \033[0m")
        if key == "m":
            main_menu()

    else:
        main_menu()

# STARTING SCRIPT

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        main_menu()
    finally:
        if "controller" in locals():
            controller.close()