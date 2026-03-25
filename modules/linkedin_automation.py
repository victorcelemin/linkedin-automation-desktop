"""
LinkedIn Automation Module - Selenium-based LinkedIn automation
"""

import time
import random
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Warning: Selenium not installed. Install with: pip install selenium")


class LinkedInAutomation:
    """LinkedIn automation with human-like behavior"""
    
    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password
        self.driver = None
        self.wait = None
        self.is_logged_in = False
        
        # Human behavior settings
        self.min_delay = 2
        self.max_delay = 15
        self.typing_speed_min = 50
        self.typing_speed_max = 200
    
    def open_browser(self):
        """Open browser with Selenium"""
        if not SELENIUM_AVAILABLE:
            raise Exception("Selenium no está instalado. Ejecuta: pip install selenium")
        
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
        
        # Execute CDP to hide webdriver
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
        
        # Open LinkedIn
        self.driver.get("https://www.linkedin.com")
        time.sleep(2)
        
        return True
    
    def login(self, email=None, password=None):
        """Login to LinkedIn"""
        # Update credentials if provided
        if email:
            self.email = email
        if password:
            self.password = password
            
        # Validate credentials
        if not self.email or not self.password:
            raise ValueError("Email and password are required for login")
        
        try:
            if not self.driver:
                self.open_browser()
            
            # Click sign in
            try:
                sign_in_btn = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
                )
                self._human_click(sign_in_btn)
            except:
                self.driver.get("https://www.linkedin.com/login")
            
            time.sleep(self._human_delay())
            
            # Enter email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            self._human_type(email_field, self.email)
            
            time.sleep(self._human_delay())
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            self._human_type(password_field, self.password)
            
            time.sleep(self._human_delay())
            
            # Click login
            login_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            self._human_click(login_btn)
            
            # Wait for login
            time.sleep(5)
            
            # Check if logged in
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                self.is_logged_in = True
                return True
            
            # Check for security verification
            if "checkpoint" in self.driver.current_url:
                print("LinkedIn requires security verification. Please verify manually.")
                input("Press Enter after verification...")
                self.is_logged_in = True
                return True
            
            return False
            
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def publish_post(self, content, image_url=None):
        """Publish a post to LinkedIn"""
        try:
            if not self.is_logged_in:
                if not self.login():
                    return False
            
            # Navigate to home
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(self._human_delay())
            
            # Scroll a bit (human behavior)
            self._human_scroll()
            
            # Click "Start a post"
            start_post_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//button[contains(@class, 'share-box') or contains(text(), 'Start a post')]"))
            )
            self._human_click(start_post_btn)
            
            time.sleep(self._human_delay())
            
            # Type content
            post_editor = self.wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//div[@contenteditable='true' or @role='textbox']"))
            )
            self._human_type(post_editor, content)
            
            time.sleep(self._human_delay())
            
            # Add image if provided
            if image_url:
                self._add_image(image_url)
            
            # Click post button
            post_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//button[contains(text(), 'Post') and not(contains(text(), 'Start'))]"))
            )
            self._human_click(post_btn)
            
            # Wait and stay on page
            time.sleep(random.randint(5, 15))
            
            return True
            
        except Exception as e:
            print(f"Publish error: {e}")
            return False
    
    def _add_image(self, image_url):
        """Add image to post"""
        try:
            # Click add media button
            add_media_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//button[contains(@aria-label, 'Add') or contains(text(), 'Add media')]"))
            )
            self._human_click(add_media_btn)
            
            time.sleep(self._human_delay())
            
            # Note: Image upload requires file dialog handling
            # This is a simplified version
            print(f"Would upload image from: {image_url}")
            
        except Exception as e:
            print(f"Image add error: {e}")
    
    def _human_click(self, element):
        """Perform human-like click"""
        try:
            actions = ActionChains(self.driver)
            
            # Random offset
            x_offset = random.randint(-5, 5)
            y_offset = random.randint(-5, 5)
            
            # Sometimes move mouse before clicking
            if random.random() < 0.7:
                actions.move_to_element(element, x_offset, y_offset)
                actions.pause(random.uniform(0.1, 0.5))
                actions.click()
                actions.perform()
            else:
                element.click()
                
        except:
            element.click()
    
    def _human_type(self, element, text):
        """Type text with human-like speed"""
        element.clear()
        
        for char in text:
            element.send_keys(char)
            
            # Random typing delay
            delay = random.randint(self.typing_speed_min, self.typing_speed_max) / 1000
            time.sleep(delay)
            
            # Occasional pause (thinking)
            if random.random() < 0.03:
                time.sleep(random.uniform(0.5, 1.5))
            
            # Rare typo simulation
            if random.random() < 0.01:
                wrong_char = chr(ord(char) + 1) if ord(char) < 122 else char
                element.send_keys(wrong_char)
                time.sleep(0.1)
                element.send_keys(Keys.BACK_SPACE)
                time.sleep(0.1)
    
    def _human_scroll(self):
        """Perform human-like scroll"""
        scroll_amount = random.randint(100, 500)
        self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(0.5, 2))
        
        # Sometimes scroll back
        if random.random() < 0.3:
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount // 2});")
    
    def _human_delay(self):
        """Get random human-like delay"""
        return random.uniform(self.min_delay, self.max_delay)
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.is_logged_in = False