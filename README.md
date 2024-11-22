# LaunchMyNFT Automation Tool

An automation tool for minting NFTs on launchmynft.io using multiple Solana wallets.

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Phantom wallet private keys
- Windows or MacOS

## Setup Instructions

### 1. Create Virtual Environment

bash
Create a new virtual environment
python -m venv venv
Activate virtual environment
On Windows:
venv\Scripts\activate
On Mac/Linux:
source venv/bin/activate

### 2. Install Dependencies

`pip install selenium`
`pip install webdriver_manager`
`pip install requests`

### 3. Get Phantom Extension File

1. Install Phantom extension in Chrome
2. Go to `chrome://extensions/`
3. Enable "Developer mode" (top right)
4. Locate Phantom extension
5. Note the extension ID
6. Visit: `chrome://extensions/?id=<extension_id>`
7. Download and save as `Phantom.crx` in your project directory

### 4. Configure Wallet Settings

Create a `config.json` file in the project directory:

```json
{
    "launchpadLink": "https://www.launchmynft.io/collections/your-collection-link",
    "wallets": [
        {
            "name": "Wallet 1",
            "privateKey": "your-private-key-here"
        },
        {
            "name": "Wallet 2",
            "privateKey": "your-second-private-key-here"
        }
    ]
}
```

### 5. Project Structure

Ensure your project directory looks like this:
```
project-directory/
├── venv/
├── main.py
├── launchmy.py
├── config.json
└── Phantom.crx
```

## Usage

1. Activate your virtual environment (if not already activated)
2. Run the script:
```bash
python main.py
```

The script will:
- Process each wallet sequentially
- Initialize Phantom wallet with the provided private key
- Connect to the launchpad
- Attempt to mint NFTs

## Configuration Options

### Wallet Configuration
- `name`: Identifier for the wallet (for logging purposes)
- `privateKey`: Your Solana wallet's private key

### Chrome Options
In `launchmy.py`, you can modify Chrome options:
- `options.add_argument("--disable-gpu")`: Disables GPU hardware acceleration
- `options.add_experimental_option("detach", True)`: Keeps windows open after mint (commented by default)

## Troubleshooting

1. **ChromeDriver Issues**
   - The script automatically downloads the appropriate ChromeDriver
   - If you encounter errors, try deleting the cached ChromeDriver and let it download again

2. **Phantom Extension Issues**
   - Ensure `Phantom.crx` is in the correct location
   - Verify the extension file is not corrupted

3. **SSL Errors**
   ```bash
   pip install certifi
   ```

## Security Notes

- Never share your private keys
- Store your `config.json` securely
- Don't commit sensitive information to version control

## Disclaimer

This tool is for educational purposes only. Be aware that:
- Automated minting might be against some platforms' terms of service
- Use at your own risk
- Always verify transactions before confirming
