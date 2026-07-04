import os
import requests

# ==========================
# Configuration
# ==========================
URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    # Replace with your own contact if you publish the app
    "User-Agent": "WikiCLI/1.0 (Developed by @abdulconsole)"
}

# ==========================
# ANSI Colours
# ==========================
RESET = "\033[0m"
BOLD = "\033[1m"

CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
WHITE = "\033[97m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    clear()

    print(f"""{CYAN}{BOLD}
██╗    ██╗██╗██╗  ██╗██╗ ██████╗██╗     ██╗
██║    ██║██║██║ ██╔╝██║██╔════╝██║     ██║
██║ █╗ ██║██║█████╔╝ ██║██║     ██║     ██║
██║███╗██║██║██╔═██╗ ██║██║     ██║     ██║
╚███╔███╔╝██║██║  ██╗██║╚██████╗███████╗██║
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝╚══════╝╚═╝
{RESET}""")

    print(f"{BLUE}{'='*64}{RESET}")
    print(f"{GREEN}{BOLD}          Wikipedia CLI Search Tool{RESET}")
    print(f"{YELLOW}              Developed by @abdulconsole{RESET}")
    print(f"{BLUE}{'='*64}{RESET}\n")


def search(query):
    response = requests.get(
        URL,
        headers=HEADERS,
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 5,
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()["query"]["search"]


def summary(title):
    response = requests.get(
        URL,
        headers=HEADERS,
        params={
            "action": "query",
            "prop": "extracts",
            "titles": title,
            "exintro": True,
            "explaintext": True,
            "format": "json",
        },
        timeout=10,
    )

    response.raise_for_status()

    pages = response.json()["query"]["pages"]
    return next(iter(pages.values()))


def main():
    while True:
        header()

        query = input(f"{CYAN}🔎 Search Wikipedia:{RESET} ").strip()

        if query.lower() in ("exit", "quit", "q"):
            print(f"\n{GREEN}Goodbye 👋{RESET}")
            break

        if not query:
            continue

        try:
            results = search(query)

            if not results:
                input(f"\n{RED}No results found. Press Enter...{RESET}")
                continue

            print(f"\n{GREEN}{BOLD}Top Results{RESET}")
            print(f"{BLUE}{'-'*64}{RESET}")

            for i, result in enumerate(results, 1):
                print(f"{MAGENTA}[{i}]{RESET} {WHITE}{result['title']}{RESET}")

            print(f"{BLUE}{'-'*64}{RESET}")

            choice = input(
                f"\n{CYAN}Choose article (1-{len(results)}) or B to go back:{RESET} "
            ).strip()

            if choice.lower() == "b":
                continue

            index = int(choice) - 1

            if not (0 <= index < len(results)):
                raise ValueError

            page = summary(results[index]["title"])

            clear()

            print(f"{CYAN}{'='*64}{RESET}")
            print(f"{YELLOW}{BOLD}{page['title']}{RESET}")
            print(f"{CYAN}{'='*64}{RESET}\n")

            extract = page.get("extract", "No summary available.")

            print(extract)

            print(f"\n{BLUE}{'='*64}{RESET}")

            input(f"{GREEN}Press Enter to search again...{RESET}")

        except ValueError:
            input(f"\n{RED}Invalid selection. Press Enter...{RESET}")

        except requests.RequestException as e:
            input(f"\n{RED}Network Error: {e}{RESET}\nPress Enter...")

        except KeyboardInterrupt:
            print(f"\n\n{GREEN}Exiting... Goodbye 👋{RESET}")
            break


if __name__ == "__main__":
    main()
