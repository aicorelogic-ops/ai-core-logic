import requests
from .settings import FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID

class FacebookPublisher:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v19.0"
        self.token = FB_PAGE_ACCESS_TOKEN
        self.page_id = FB_PAGE_ID

    def post_content(self, message, link=None):
        """
        Publishes a post to the Facebook Page.
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None

        url = f"{self.base_url}/{self.page_id}/feed"
        payload = {
            "message": message,
            "access_token": self.token
        }
        
        if link:
            payload["link"] = link

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            print(f"✅ Successfully posted to Facebook! Post ID: {data.get('id')}")
            return data.get('id')
        except requests.exceptions.RequestException as e:
            print(f"❌ Error posting to Facebook: {e}")
            if response is not None: # check if response exists first
                 with open("fb_error.txt", "w", encoding="utf-8") as f:
                     f.write(response.text)
                 print(f"Response saved to fb_error.txt")
            return None

if __name__ == "__main__":
    # Test run
    publisher = FacebookPublisher()
    publisher.post_content("Hello World! This is a test post from AI Core Logic Bot. #AI #Automation")
