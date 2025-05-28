import os
import time
import argparse
import requests
import webbrowser
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Configuration
DEFAULT_BATCH_SIZE = 5
DEFAULT_DELAY = 5

# Function to validate URL
def validate_url(url):
    if not url.startswith('http'):
        url = 'https://' + url
    try:
        response = requests.head(url, timeout=5)
        status = response.status_code
        return url, status
    except requests.RequestException:
        return url, None

# Function to open URL in browser
def open_url(url):
    webbrowser.open(url)
    time.sleep(1)  # Slight delay between openings

# Function to open in batches
def open_in_batches(subdomains, batch_size, delay):
    for i in tqdm(range(0, len(subdomains), batch_size)):
        batch = subdomains[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            executor.map(open_url, batch)
        time.sleep(delay)  # Delay between batches

# Function to read subdomains from file
def read_subdomains(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        exit(1)
    
    with open(file_path, 'r') as file:
        subdomains = [line.strip() for line in file if line.strip()]
    subdomains = list(set(subdomains))  # Remove duplicates
    return subdomains

# CLI using argparse
def main():
    parser = argparse.ArgumentParser(description="Automated Subdomain Opener")
    parser.add_argument("-f", "--file", type=str, required=True, help="Path to subdomain file")
    parser.add_argument("-b", "--batch", type=int, default=DEFAULT_BATCH_SIZE, help="Number of tabs to open at once")
    parser.add_argument("-d", "--delay", type=int, default=DEFAULT_DELAY, help="Delay between batches (in seconds)")
    parser.add_argument("--proxy", type=str, help="Set HTTP proxy (e.g., http://127.0.0.1:8080)")

    args = parser.parse_args()

    # Load subdomains
    subdomains = read_subdomains(args.file)
    print(f"Loaded {len(subdomains)} subdomains.")

    # Validate URLs
    valid_subdomains = []
    for url in subdomains:
        validated_url, status = validate_url(url)
        if status:
            valid_subdomains.append(validated_url)
            print(f"[+] {validated_url} - {status}")
        else:
            print(f"[-] {validated_url} - Invalid")

    # Open in batches
    if valid_subdomains:
        print("\nOpening in batches...")
        open_in_batches(valid_subdomains, args.batch, args.delay)
    else:
        print("No valid subdomains found.")

if __name__ == "__main__":
    main()
