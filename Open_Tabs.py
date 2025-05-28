import webbrowser
import time

# Read subdomains from a file
file_path = 'subdomains.txt'  # File containing list of subdomains

# Number of tabs to open at once
BATCH_SIZE = 5

# Read subdomains
with open(file_path, 'r') as f:
    subdomains = [line.strip() for line in f.readlines() if line.strip()]

# Open subdomains in batches
def open_in_batches(subdomains, batch_size):
    for i in range(0, len(subdomains), batch_size):
        batch = subdomains[i:i + batch_size]
        print(f"Opening batch: {batch}")
        for url in batch:
            if not url.startswith('http'):
                url = 'https://' + url
            webbrowser.open(url)
        time.sleep(5)  # Add delay to avoid overloading the browser

# Execute
open_in_batches(subdomains, BATCH_SIZE)