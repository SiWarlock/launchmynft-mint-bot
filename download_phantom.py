import requests

def download_phantom():
    # Updated URL with newer Chrome version
    url = "https://clients2.google.com/service/update2/crx?response=redirect&acceptformat=crx2,crx3&prodversion=112.0.5615.49&x=id%3Dbfnaelmomeimhlpmgjnjophhpkkoljpa%26installsource%3Dondemand%26uc"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
    
    print("Downloading Phantom extension...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open("Phantom.crx", "wb") as f:
            f.write(response.content)
        print("Successfully downloaded Phantom.crx")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

if __name__ == "__main__":
    download_phantom() 