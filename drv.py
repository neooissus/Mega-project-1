from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Update this path to where you placed chromedriver
service = Service('G:\\chromedriver-win64\\chromedriver.exe')  # For Windows

driver = webdriver.Chrome(service=service, options=chrome_options)
