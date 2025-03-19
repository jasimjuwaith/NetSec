import requests
import json
import pandas as pd
import threading
import time

ABUSEIPDB_API_KEY = "YOUR_OSINT_API_KEY"
CACHE_FILE = "data/osint_cache.json"

# Load existing OSINT cache (if available)
try:
    with open(CACHE_FILE, "r") as file:
        osint_cache = json.load(file)
except FileNotFoundError:
    osint_cache = {}

def check_ip_reputation(ip):
    """Queries AbuseIPDB for IP reputation. Uses caching to reduce API calls."""
    if ip in osint_cache:  
        return osint_cache[ip]  # Return cached result

    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
    headers = {"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=2)  # Set timeout to avoid delays
        data = response.json()
        risk_score = data.get("data", {}).get("abuseConfidenceScore", 0)  # 0 if safe

        osint_cache[ip] = risk_score  # Store in cache
        return risk_score

    except:
        return 0  # Default to 0 (safe) if API fails

def save_cache():
    """Saves OSINT cache to disk periodically to avoid repeated API queries."""
    with open(CACHE_FILE, "w") as file:
        json.dump(osint_cache, file)

def process_ip_list(ip_list):
    """Processes a list of IPs using multi-threading."""
    threads = []
    results = {}

    def worker(ip):
        results[ip] = check_ip_reputation(ip)

    for ip in ip_list:
        thread = threading.Thread(target=worker, args=(ip,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    save_cache()  # Save updated cache to disk
    return results

# Example: Processing IPs in real-time
real_time_ips = ["185.220.101.20", "104.28.10.1", "8.8.8.8"]
osint_results = process_ip_list(real_time_ips)

print("OSINT Lookup Results:", osint_results)
