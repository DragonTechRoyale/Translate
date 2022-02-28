import csv
import platform
import urllib.request
import os
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from py_console import console


class Translate():
    __TRANSLATE_MAX = 2000 # max characters I can supply to google translate through the url
    __TRANSLATED_TEXT_XPATH = "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[6]/div/div[1]/span[1]/span/span"
    __GECKODRIVER_PATH = './geckodriver'
    browser = None


    def __init__(self, hide_window=True):
        if hide_window:
            os.environ['MOZ_HEADLESS'] = '1'  # hides the Firefox window
        if not os.path.isfile('./geckodriver'):
            console.warn("Warning: geckodriver is not in directory: downloading to this directory")
            download_link = ""
            match platform.system():  # TODO: add Windows support 
                case 'Darwin':
                    match platform.machine():
                        case 'x86_64':
                            download_link = "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-macos.tar.gz"
                        case 'arm64':
                            download_link = "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-macos-aarch64.tar.gz"
                case 'Linux':
                    match platform.machine():
                        case 'x86_64':
                            download_link = "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz"
                        case 'i386':
                            download_link = "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz"
            if download_link == "":
                console.error("Can't download geckodriver, try to install from this link: https://github.com/mozilla/geckodriver/releases\n Aborting...")
                return
            if platform.system() == 'Darwin' or platform.system() == 'Linux':
                os.system(f"""
                          wget {download_link} 
                          tar -xf {download_link.split('/')[-1]}
                          rm {download_link.split('/')[-1]}
                          """)
        self.browser = webdriver.Firefox(executable_path=self.__GECKODRIVER_PATH) # Create a Firefox browser instance
                

    def translate_codes(self, lang_name):
        csvfile = open('codes.csv', newline='')
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Language Name"] == lang_name:
                code = row["Code"]
                csvfile.close()
                return code
        csvfile.close()
        return None


    def translate(self, TL, NL, word):
        if self.browser == None:
            console.error("translate() - browser = None")
            return
        # Load the google trasnlate page
        translation_url = f"https://translate.google.com/?sl={self.translate_codes(TL)}&tl={self.translate_codes(NL)}&text={word}%0A&op=translate"
        try:
            self.browser.get(translation_url)
            self.browser.implicitly_wait(2) # gives an implicit wait for 0.5 seconds
            translated_text_element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, self.__TRANSLATED_TEXT_XPATH)))
            traslated_word = translated_text_element.text
            return traslated_word
        except Exception as e:
            console.log(f"translate() - exception:\n{e}")
            return None # return None to signal the next function to stop the translation process


    def translate_max(self):
        return self.__TRANSLATE_MAXs
    
    
    def translated_text_xpath(self):
        return self.__TRANSLATED_TEXT_XPATH
    
    
    def exit(self):
        self.browser.close()
    
