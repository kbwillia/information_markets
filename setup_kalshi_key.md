# Setting Up Kalshi Private Key

You have two options for storing your Kalshi private key:

## Option 1: Save to a File (Recommended - More Secure)

1. **Download your private key from Kalshi:**
   - Go to https://kalshi.com/account/profile
   - Download your RSA private key (it will be a `.pem` file)

2. **Save the key file:**
   - Create a `keys` directory in your project (or use any secure location)
   - Save the downloaded file as `kalshi_private_key.pem` (or any name you prefer)
   - **Important:** Add `keys/` to your `.gitignore` to avoid committing the key!

3. **Update your `.env` file:**
   ```env
   KALSHI_API_KEY=your-api-key-id-here
   KALSHI_PRIVATE_KEY_PATH=keys/kalshi_private_key.pem
   KALSHI_BASE_URL=https://api.elections.kalshi.com/trade-api/v2
   ```

## Option 2: Store in .env File (Easier - Less Secure)

1. **Copy your private key content:**
   - Open the `.pem` file in a text editor
   - Copy the entire content (including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`)

2. **Update your `.env` file:**
   ```env
   KALSHI_API_KEY=your-api-key-id-here
   KALSHI_PRIVATE_KEY_PEM="-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----"
   KALSHI_BASE_URL=https://api.elections.kalshi.com/trade-api/v2
   ```
   
   **Note:** You may need to replace actual newlines with `\n` or keep it as a multi-line string in the .env file.

## Security Recommendations

- **Never commit your private key to git!**
- Add `keys/` and `.env` to your `.gitignore`
- Use Option 1 (file) for production
- Option 2 is fine for local development

## Testing

After setting up, run:
```bash
python test_api_keys.py
```

