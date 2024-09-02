import speech_recognition as sr
import pyttsx3
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Set up the Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service('G:\\chromedriver-win64\\chromedriver.exe')  # Update this to your WebDriver path
driver = webdriver.Chrome(service=service, options=chrome_options)

# Dictionary to keep track of opened tabs
opened_tabs = {}

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    global opened_tabs
    command = command.lower()

    if "open google" in command:
        if "google" not in opened_tabs:
            url = "https://google.com"
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url)
            opened_tabs["google"] = driver.current_window_handle
            speak("Opening Google")
            print("Taking you to Google")

    elif "open youtube" in command:
        if "youtube" not in opened_tabs:
            url = "https://youtube.com"
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url)
            opened_tabs["youtube"] = driver.current_window_handle
            speak("Opening YouTube")
            print("Taking you to YouTube")

    elif "search for" in command:
        search_query = command.split("search for", 1)[1].strip()
        if "on youtube" in command:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(f"https://www.youtube.com/results?search_query={search_query}")
            speak(f"Searching for {search_query} on YouTube")
            print(f"Searching for {search_query} on YouTube")
        elif "on google" in command:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(f"https://www.google.com/search?q={search_query}")
            speak(f"Searching for {search_query} on Google")
            print(f"Searching for {search_query} on Google")

    elif "close" in command:
        for site_name, tab_handle in opened_tabs.items():
            if f"close {site_name}" in command:
                driver.switch_to.window(tab_handle)
                driver.close()
                opened_tabs.pop(site_name)
                speak(f"Closing {site_name.capitalize()}")
                print(f"Closing {site_name.capitalize()}")
                break

    elif command.lower().startswith("play"):
        song_name = command.lower().replace("play", "").strip()
        if song_name:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(f"https://www.youtube.com/results?search_query={song_name}")
            time.sleep(2)  # Wait for the search results to load
            first_video = driver.find_element("id", "video-title")
            first_video.click()
            speak(f"Playing {song_name} on YouTube")
            print(f"Playing {song_name} on YouTube")

if __name__ == "__main__":
    speak("Initializing Delta...")

    while True:
        print("Call me Delta, your virtual assistant!...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

            command = recognizer.recognize_google(audio).lower()
            if "delta" in command:
                speak("Yes sir, how may I help you?")

                while True:
                    with sr.Microphone() as source:
                        print("Delta is active. Listening for your command....")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

                    try:
                        command = recognizer.recognize_google(audio).lower()
                        print(f"Heard command: {command}")

                        if "delta exit" in command:
                            speak("Deactivating Delta. Goodbye.")
                            print("Deactivating Delta...")
                            driver.quit()  # Close the browser
                            break

                        processCommand(command)

                    except sr.UnknownValueError:
                        print("Sorry, I didn't catch that. Please try again.")
                        speak("Sorry, I didn't catch that. Please try again.")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
                        speak("There seems to be an issue with the speech recognition service.")

        except sr.UnknownValueError:
            print("Delta could not understand your voice")
        except sr.RequestError as e:
            print(f"Delta error; {e}")
        except sr.WaitTimeoutError:
            print("Listening timed out waiting for you to speak.")
            speak("I didn't hear anything. Please try again.")
