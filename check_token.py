import requests
from news_bot.settings import FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID

def check_token():
    with open("token_check_result.txt", "w", encoding="utf-8") as f:
        f.write("🔍 Checking Credentials...\n")

        # 1. Check Token Type
        url = f"https://graph.facebook.com/me?access_token={FB_PAGE_ACCESS_TOKEN}"
        try:
            resp = requests.get(url)
            data = resp.json()
        except Exception as e:
            f.write(f"❌ Connection Error: {e}\n")
            return

        if "error" in data:
            f.write(f"❌ Token Error: {data['error']['message']}\n")
            return

        f.write(f"✅ Token Identity: {data.get('name')} (ID: {data.get('id')})\n")
        
        if "category" in data:
            f.write("   Type: PAGE (Correct)\n")
        else:
            f.write("   Type: USER (Incorrect - You need a Page Token!)\n")

        # 2. Check Page ID target
        f.write(f"\nTarget Page ID from .env: {FB_PAGE_ID}\n")
        if data.get('id') == FB_PAGE_ID:
            f.write("✅ Token matches Page ID.\n")
        else:
            f.write("⚠️ Token ID does NOT match .env Page ID.\n")
            f.write(f"   (If Token is User, this is expected. If Token is Page, they must match).\n")

if __name__ == "__main__":
    check_token()
