
import requests
import os
from .settings import FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID

class FacebookPublisher:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v19.0"
        self.token = FB_PAGE_ACCESS_TOKEN
        self.page_id = FB_PAGE_ID

    def post_content(self, message, link=None):
        """
        Publishes a post to the Facebook Page feed.
        If a link is provided, it becomes a 'link post'.
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
            print(f"Successfully posted to Facebook! Post ID: {data.get('id')}")
            return data.get('id')
        except requests.exceptions.RequestException as e:
            self._handle_error(e, response if 'response' in locals() else None)
            return None

    def post_photo(self, photo_url, message):
        """
        Publishes a photo post to the Facebook Page.
        This is typically more 'attention-grabbing' than a standard link post.
        
        Includes retry logic for AI-generated images that may take time to render.
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None

        url = f"{self.base_url}/{self.page_id}/photos"
        
        # Pre-check: Verify image URL is accessible (important for AI-generated images)
        import time
        max_retries = 3
        retry_delay = 5  # seconds
        
        # Combine verification and download to ensure we have valid content
        image_content = None
        for attempt in range(max_retries):
            try:
                print(f"Downloading image (attempt {attempt + 1}/{max_retries})...")
                content = self._download_image_content(photo_url)
                
                if content and len(content) > 1000:
                    print(f"✅ Image downloaded successfully ({len(content)} bytes).")
                    image_content = content
                    break
                else:
                    print(f"⚠️ Image download failed or too small (<1KB). Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
            except Exception as e:
                print(f"❌ Image download error: {e}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
        
        if not image_content:
            print("❌ Failed to retrieve valid image content after retries.")
            return None
        
        # 2. Now post to Facebook using BINARY UPLOAD
        try:
            print("Retrieving image for binary upload...")
            
            # Handle local file case if needed (though we passed URL mostly)
            if not image_content:
                if photo_url.startswith("file://"):
                   # ... local file logic ...
                   pass 
            
            # Since we likely have image_content from above loop:
            if not image_content: 
                 # Fallback for file:// or if logic above failed silently
                 if photo_url.startswith("file://"):
                    local_path = photo_url.replace("file://", "")
                    if os.name == 'nt':
                        local_path = local_path.lstrip('/')
                    with open(local_path, "rb") as f:
                        image_content = f.read()
                 else:
                    # Should have been caught above, but just in case
                    return None

            
            content_size = len(image_content)
            print(f"Image Size: {content_size} bytes.")
            
            if content_size < 1000:
                print(f"WARNING: Image too small! Content preview: {str(image_content[:200])}")
            
            # 2. Prepare multipart upload
            files = {
                'source': ('image.jpg', image_content, 'image/jpeg')
            }
            
            # Send token in query params to avoid multipart confusion
            params = {
                "access_token": self.token
            }
            
            data = {
                "caption": message,
                "published": "true"
            }

            print("Uploading binary image data to Facebook (Token in Params)...")
            response = requests.post(url, files=files, data=data, params=params, timeout=60)
            
            # Check for specific subcode errors
            if response.status_code >= 400:
                print(f"Facebook API Error Response: {response.text}")
                
            response.raise_for_status()
            data = response.json()
            print(f"Successfully posted photo to Facebook! ID: {data.get('id')}")
            return data.get('id')
            
        except requests.exceptions.RequestException as e:
            self._handle_error(e, response if 'response' in locals() else None)
            return None
    
    def post_video(self, video_path, caption):
        """
        Post a video to Facebook Page (simpler than Reels API).
        Works for any video format including vertical 9:16 reels.
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None
        
        url = f"{self.base_url}/{self.page_id}/videos"
        
        try:
            import os
            video_size = os.path.getsize(video_path)
            print(f"Uploading video to Facebook...")
            print(f"   Video size: {video_size:,} bytes")
            
            with open(video_path, 'rb') as video_file:
                files = {'file': video_file}
                data = {
                    'description': caption,
                    'access_token': self.token
                }
                
                response = requests.post(url, files=files, data=data, timeout=120)
                response.raise_for_status()
                
                video_data = response.json()
                print(f"Successfully posted video!")
                print(f"Video ID: {video_data.get('id')}")
                return video_data.get('id')
                    
        except Exception as e:
            print(f"Video upload error: {e}")
            if 'response' in locals():
                self._handle_error(e, response)
            return None
    
    def post_reel(self, video_path, caption):
        """
        Post a video as a Reel to Facebook Page using 3-phase upload.
        Video should be vertical format (9:16), 15-90 seconds.
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None
        
        try:
            import os
            video_size = os.path.getsize(video_path)
            
            print(f"Uploading reel to Facebook (3-phase upload)...")
            print(f"   Video size: {video_size:,} bytes")
            
            # PHASE 1: Initialize upload session
            print("   Phase 1: Initializing upload session...")
            init_url = f"{self.base_url}/{self.page_id}/video_reels"
            init_data = {
                'upload_phase': 'start',
                'file_size': video_size,
                'access_token': self.token
            }
            
            init_response = requests.post(init_url, data=init_data)
            init_response.raise_for_status()
            init_result = init_response.json()
            
            video_id = init_result.get('video_id')
            upload_session_id = init_result.get('upload_session_id')
            
            if not video_id or not upload_session_id:
                print(f"Failed to initialize upload: {init_result}")
                return None
            
            print(f"   Session ID: {upload_session_id}")
            
            # PHASE 2: Upload video file
            print("   Phase 2: Uploading video file...")
            upload_url = f"{self.base_url}/{self.page_id}/video_reels"
            
            with open(video_path, 'rb') as video_file:
                upload_data = {
                    'upload_phase': 'transfer',
                    'upload_session_id': upload_session_id,
                    'access_token': self.token
                }
                upload_files = {'video_file_chunk': video_file}
                
                upload_response = requests.post(upload_url, data=upload_data, files=upload_files)
                upload_response.raise_for_status()
                upload_result = upload_response.json()
            
            print(f"   Video uploaded")
            
            # PHASE 3: Finalize and publish
            print("   Phase 3: Publishing reel...")
            finish_url = f"{self.base_url}/{self.page_id}/video_reels"
            finish_data = {
                'upload_phase': 'finish',
                'upload_session_id': upload_session_id,
                'description': caption,
                'access_token': self.token
            }
            
            finish_response = requests.post(finish_url, data=finish_data)
            finish_response.raise_for_status()
            finish_result = finish_response.json()
            
            if finish_result.get('success'):
                print(f"Successfully posted Reel!")
                print(f"Reel ID: {video_id}")
                return video_id
            else:
                print(f"Failed to finalize: {finish_result}")
                return None
                    
        except Exception as e:
            print(f"Reel upload error: {e}")
            if 'init_response' in locals():
                self._handle_error(e, init_response)
            elif 'upload_response' in locals():
                self._handle_error(e, upload_response)
            elif 'finish_response' in locals():
                self._handle_error(e, finish_response)
            return None

    def _handle_error(self, exception, response):
        print(f"Error posting to Facebook: {exception}")
        if response is not None:
            with open("fb_error.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Response saved to fb_error.txt")
            
    def _download_image_content(self, url):
        """
        Robustly downloads image content, handling redirects and headers.
        """
        print(f"Downloading image from: {url}")
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            })
            
            response = session.get(url, stream=True, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            content = b""
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    content += chunk
                    
            if len(content) == 0:
                print("WARNING: Downloaded content is empty.")
                return None
                
            return content
        except Exception as e:
            print(f"Download invalid: {e}")
            return None

if __name__ == "__main__":
    # Test run
    publisher = FacebookPublisher()
    # publisher.post_content("Hello World! This is a test post from AI Core Logic Bot. #AI #Automation")

