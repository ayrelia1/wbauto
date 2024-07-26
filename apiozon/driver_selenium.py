#from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, NoSuchWindowException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
#from seleniumwire import webdriver
#import undetected_chromedriver as uc
from seleniumrequests import Chrome
from webdriver_manager.chrome import ChromeDriverManager
import os
import xvfbwrapper
vdisplay = xvfbwrapper.Xvfb(width=1920, height=1080)
vdisplay.start()

def get_user_browser(profile):
    chrome_driver_path = Service('chromedriver/chromedriver')
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--start-maximized")
    options.add_argument("--enable-javascript")
    options.add_argument('--enable-aggressive-domstorage-flushing')
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(f"--user-data-dir=profiles/users") #e.g. 
    options.add_argument(f'--profile-directory={profile}')
    #options.add_argument(f'--profile-directory={profile}')
    #options.add_argument("--headless=new")
    options.add_argument('--profiling-flush=10')
    options.add_argument('--User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    options.add_argument("--no-sandbox")
    driver = Chrome(service=chrome_driver_path, options=options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
        '''
    })
    return driver


# def get_user_browser(profile):
#     chrome_driver_path = Service('chromedriver/chromdriver')
#     options = ChromeOptions()
    
#     options.add_argument("--start-maximized")
#     options.add_argument("--enable-javascript")
#     options.add_argument('--enable-aggressive-domstorage-flushing')
#     options.add_argument('--allow-profiles-outside-user-dir')
#     options.add_argument('--enable-profile-shortcut-manager')
#     options.add_argument(f"--user-data-dir=profiles/users") #e.g. 
#     options.add_argument(f'--profile-directory={profile}')
#     options.add_argument('--profiling-flush=10')
#     #options.add_argument(f'--disable-gpu')
#     #options.add_argument('--headless=new')
#     #options.add_argument("--disable-extensions")
#     #options.add_argument('--disable-application-cache')
#     options.add_argument("--no-sandbox")
#     #options.add_argument("--disable-setuid-sandbox")
#     #options.add_argument(f'--disable-dev-shm-usage')
#     options.add_argument('--User-Agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')
#     driver = uc.Chrome(driver_executable_path='chromedriver/chromedriver', options=options)

    
    
#     return driver