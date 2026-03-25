"""
Image Handler Module - Image search and management
"""

import random
import requests
import os


class ImageHandler:
    """Handle image search and download"""
    
    def __init__(self):
        self.unsplash_api_key = os.getenv('UNSPLASH_API_KEY', '')
        self.pexels_api_key = os.getenv('PEXELS_API_KEY', '')
        
        # Fallback images (free stock photos)
        self.fallback_images = [
            "https://picsum.photos/800/600?random=1",
            "https://picsum.photos/800/600?random=2",
            "https://picsum.photos/800/600?random=3",
            "https://picsum.photos/800/600?random=4",
            "https://picsum.photos/800/600?random=5",
            "https://picsum.photos/800/600?random=6",
            "https://picsum.photos/800/600?random=7",
            "https://picsum.photos/800/600?random=8",
            "https://picsum.photos/800/600?random=9",
            "https://picsum.photos/800/600?random=10"
        ]
    
    def search_image(self, query):
        """Search for an image based on query"""
        try:
            # Try Unsplash first
            if self.unsplash_api_key:
                return self._search_unsplash(query)
            
            # Try Pexels
            if self.pexels_api_key:
                return self._search_pexels(query)
            
            # Fallback to random image
            return self._get_fallback_image()
            
        except Exception as e:
            print(f"Error searching image: {e}")
            return self._get_fallback_image()
    
    def _search_unsplash(self, query):
        """Search Unsplash for images"""
        url = "https://api.unsplash.com/search/photos"
        headers = {
            "Authorization": f"Client-ID {self.unsplash_api_key}"
        }
        params = {
            "query": query,
            "per_page": 5,
            "orientation": "landscape"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                image = random.choice(data['results'][:5])
                return image['urls']['regular']
        
        return self._get_fallback_image()
    
    def _search_pexels(self, query):
        """Search Pexels for images"""
        url = "https://api.pexels.com/v1/search"
        headers = {
            "Authorization": self.pexels_api_key
        }
        params = {
            "query": query,
            "per_page": 5,
            "orientation": "landscape"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('photos'):
                image = random.choice(data['photos'][:5])
                return image['src']['large']
        
        return self._get_fallback_image()
    
    def _get_fallback_image(self):
        """Get a random fallback image"""
        return random.choice(self.fallback_images)
    
    def download_image(self, url, save_path='assets/images'):
        """Download image to local storage"""
        try:
            os.makedirs(save_path, exist_ok=True)
            
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                filename = f"image_{int(datetime.now().timestamp())}.jpg"
                filepath = os.path.join(save_path, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                
                return filepath
        except Exception as e:
            print(f"Error downloading image: {e}")
        
        return None