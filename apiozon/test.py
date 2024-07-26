import requests
import json
import datetime
import random
import time
import threading
from bs4 import BeautifulSoup
import json
import re
#from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, NoSuchWindowException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#from seleniumwire import webdriver
from seleniumrequests import Chrome
import os
 # kwork11/chromedriver/chromedriver.exe
def get_user_browser(profile):
    chrome_driver_path = Service('kwork11/chromedriver/chromedriver.exe')
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("start-maximized")
    options.add_argument("--enable-javascript")
    options.add_argument('--enable-aggressive-domstorage-flushing')
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(f"--user-data-dir={os.getcwd()}\\kwork11\\profiles\\users") #e.g. 
    options.add_argument(f'--profile-directory={profile}')
    options.add_argument('--profiling-flush=10')
    options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 6.3; x64) AppleWebKit/600.95 (KHTML, like Gecko) Chrome/120.0.6999.72 Safari/537')
    options.add_argument('content-type=application/json')
    options.add_argument('Accept-Language=ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7')
    options.add_argument('Accept=*/*')
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

def register_user(profile):
    driver = get_user_browser(profile)



    driver.get('https://seller.ozon.ru/')
    time.sleep(3505)
    html_content = driver.page_source
    match = re.search(r'asyncData":"([^"]+)"', html_content)
    if match:
        async_data = match.group(1)
    else:
        print("asyncData не найден.")

    
    
    params_json = {
        "asyncData": async_data,
        }
    params_json = json.dumps(params_json)
    response = driver.execute_script(
        f'''
        var xhr = new XMLHttpRequest();
        var params = {params_json};
        var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-340567-default-1";
        xhr.open('POST', url, false);
        xhr.send(JSON.stringify(params));
        return xhr.responseText;
    ''')
    
    response = json.loads(response)
    authRequestToken = response['state']['submitButton']['data']['authRequestToken']
    csrfToken = response['state']['submitButton']['data']['csrfToken']
    print(authRequestToken)
    print(csrfToken)
    
    params_json = {
        "isVerifiedEmail": False,
        "isSecondFactor": False,
        "isValuableAccount": False,
        "firstOtpSentToEmail": False,
        "activeOtpSentToEmail": False,
        "isRecognized": False,
        "authRequestToken": authRequestToken,
        "isAlphaNumericOtp": False,
        "hideHints": False,
        "csrfToken": csrfToken,
        "isOtpExpired": False,
        "isAdsAllowed": False,
        "isVerifiedEmailError": False,
        "isForceSmsOtp": False,
        "IsEmailRegistrationState": False,
        "isForceFlashCallOtp": False,
        "otpSentToPush": False,
        "otpSentToChainPushNc": False,
        "widgetName": "csma.loginOrRegistration",
        "isSeller": False,
        "isAccountRecoveryAllowed": False,
        "sellerCountry": "",
        "secondFactorCase": "",
        "hasBankAccount": False,
        "countryCode": "RU",
        "phone": "79780638151"
    }
    params_json = json.dumps(params_json)
    
    
    response = driver.execute_script(
        f'''
        var xhr = new XMLHttpRequest();
        var params = {params_json};
        var url = "https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3";
        xhr.open('POST', url, false);
        xhr.send(JSON.stringify(params));
        return xhr.responseText;
    ''')
    print(response)
    response = json.loads(response)
    optId = response['data']['otpId']
    
    
    params_json = {
        "asyncData": async_data,
        "extraBody": {
            "statusCode": "FAST_ENTRY_V3_OTP_REQUIRED",
            "error": "",
            "data": {
            "email": "",
            "emailHint": "",
            "phone": "79780638151",
            "otpId": optId,
            "otpChannel": "CHANNEL_PHONE",
            "otpAddress": "79780638151",
            "otp": "",
            "isCheckAllowed": True,
            "resendAfter": 20,
            "otpLength": 6,
            "flashCallType": True,
            "firstOtpSentToEmail": False,
            "activeOtpSentToEmail": False,
            "IsEmailRegistrationState": False,
            "isExtraOtpRequested": False,
            "extraOtpChannel": "CHANNEL_PHONE",
            "extraOtpAddress": "",
            "extraOtpId": 0,
            "extraIsCheckAllowed": True,
            "ExtraResendAfter": 0,
            "accessToken": "",
            "tokenType": "",
            "expiresIn": 0,
            "refreshToken": "",
            "isRegistration": False,
            "isLongTimeNoSee": False,
            "isValuableAccount": False,
            "hideHints": False,
            "isRecognized": False,
            "isSecondFactor": False,
            "isEmployeeLogin": False,
            "isOtpExpired": False,
            "isAdsAllowed": False,
            "isVerifiedEmailError": False,
            "isForceSmsOtp": False,
            "isForceFlashCallOtp": False,
            "isFlashCallFailed": False,
            "countryCode": "RU",
            "isSeller": False,
            "isAccountRecoveryAllowed": False,
            "sellerCountry": "",
            "secondFactorCase": "UNSPECIFIED",
            "hasBankAccount": False
            }
        }
        }
    params_json = json.dumps(params_json)
    response = driver.execute_script(
        f'''
        var xhr = new XMLHttpRequest();
        var params = {params_json};
        var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-340567-default-1";
        xhr.open('POST', url, false);
        xhr.send(JSON.stringify(params));
        return xhr.responseText;
    ''')
    
    response = json.loads(response)
    authRequestToken = response['state']['backButton']['data']['authRequestToken']
    csrfToken = response['state']['backButton']['data']['csrfToken']
    
    
    time.sleep(3)
    insert_code(driver, authRequestToken, csrfToken, optId, async_data)
    
    
def insert_code(driver, authRequestToken, csrfToken, optId, async_data):
    code = input('Введите код: ')
    time.sleep(3)
    params_json = {
        "phone": "79780638151",
        "isVerifiedEmail": False,
        "isSecondFactor": False,
        "isValuableAccount": False,
        "firstOtpSentToEmail": False,
        "activeOtpSentToEmail": False,
        "isRecognized": False,
        "authRequestToken": authRequestToken,
        "otpId": optId,
        "isAlphaNumericOtp": False,
        "hideHints": False,
        "csrfToken": csrfToken,
        "isOtpExpired": False,
        "isAdsAllowed": False,
        "isVerifiedEmailError": False,
        "isForceSmsOtp": False,
        "IsEmailRegistrationState": False,
        "isForceFlashCallOtp": False,
        "otpSentToPush": False,
        "otpSentToChainPushNc": False,
        "countryCode": "RU",
        "widgetName": "csma.loginOrRegistration",
        "isSeller": False,
        "isAccountRecoveryAllowed": False,
        "sellerCountry": "",
        "secondFactorCase": "",
        "hasBankAccount": False,
        "otp": code
        }
    params_json = json.dumps(params_json)
    
    
    response = driver.execute_script(
        f'''
        var xhr = new XMLHttpRequest();
        var params = {params_json};
        var url = "https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3";
        xhr.open('POST', url, false);
        xhr.send(JSON.stringify(params));
        return xhr.responseText;
    ''')
    response = json.loads(response)
    error = response['error']
    print(response)
    if error == "Неверный код. Попробуйте ещё раз":
        print('Неверный код, попробуйте еще раз')
    email = response['data']['email']
    emailHint = response['data']['emailHint']
    if emailHint == '' and email == '':
        driver.get('https://ozon.ru')
        time.sleep(500)
        driver.quit()
        return
        
    
    params_json = {
        "asyncData": async_data,
        "extraBody": {
            "statusCode": "FAST_ENTRY_V3_EMAIL_SECOND_FACTOR_REQUIRED",
            "error": "",
            "data": {
            "email": email,
            "emailHint": emailHint,
            "phone": "79780638151",
            "otpId": 0,
            "otpChannel": "CHANNEL_PHONE",
            "otpAddress": "79780638151",
            "otp": "",
            "isCheckAllowed": True,
            "resendAfter": 0,
            "firstOtpSentToEmail": False,
            "activeOtpSentToEmail": False,
            "IsEmailRegistrationState": False,
            "isExtraOtpRequested": False,
            "extraOtpChannel": "CHANNEL_PHONE",
            "extraOtpAddress": "",
            "extraOtpId": 0,
            "extraIsCheckAllowed": True,
            "ExtraResendAfter": 0,
            "accessToken": "",
            "tokenType": "",
            "expiresIn": 0,
            "refreshToken": "",
            "isRegistration": False,
            "isLongTimeNoSee": False,
            "isValuableAccount": False,
            "hideHints": False,
            "isRecognized": False,
            "isSecondFactor": True,
            "isEmployeeLogin": False,
            "isOtpExpired": False,
            "isAdsAllowed": True,
            "isVerifiedEmailError": False,
            "isForceSmsOtp": False,
            "isForceFlashCallOtp": False,
            "isFlashCallFailed": False,
            "countryCode": "RU",
            "isSeller": True,
            "isAccountRecoveryAllowed": True,
            "sellerCountry": "",
            "secondFactorCase": "SELLER_DIRECTOR",
            "hasBankAccount": False
            }
        }
        }
    params_json = json.dumps(params_json)
    response = driver.execute_script(
        f'''
        var xhr = new XMLHttpRequest();
        var params = {params_json};
        var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-340567-default-1";
        xhr.open('POST', url, false);
        xhr.send(JSON.stringify(params));
        return xhr.responseText;
    ''')
    
    response = json.loads(response)
    authRequestToken = response['state']['submitButton']['data']['authRequestToken']
    csrfToken = response['state']['submitButton']['data']['csrfToken']
        
        
    time.sleep(3)
    
    params_json = {
        "phone": "79780638151",
        "isVerifiedEmail": False,
        "isSecondFactor": False,
        "isValuableAccount": False,
        "firstOtpSentToEmail": False,
        "activeOtpSentToEmail": False,
        "isRecognized": False,
        "authRequestToken": authRequestToken,
        "isAlphaNumericOtp": False,
        "isExtraOtpRequested": True,
        "hideHints": False,
        "csrfToken": csrfToken,
        "isOtpExpired": False,
        "isAdsAllowed": True,
        "isVerifiedEmailError": False,
        "isForceSmsOtp": False,
        "IsEmailRegistrationState": False,
        "isForceFlashCallOtp": False,
        "otpSentToPush": False,
        "otpSentToChainPushNc": False,
        "countryCode": "RU",
        "widgetName": "csma.loginOrRegistration",
        "isSeller": False,
        "isAccountRecoveryAllowed": False,
        "sellerCountry": "",
        "secondFactorCase": "",
        "hasBankAccount": False
        }
    params_json = json.dumps(params_json)
    
    
    response = driver.execute_script(
        f'''
        var xhr = new XMLHttpRequest();
        var params = {params_json};
        var url = "https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3";
        xhr.open('POST', url, false);
        xhr.send(JSON.stringify(params));
        return xhr.responseText;
    ''')
    print(response)
    response = json.loads(response)
    extraOtpId = response['data']['extraOtpId']
    extraOtpAddress = response['data']['extraOtpAddress']
    
    
    params_json = {
        "asyncData": async_data,
        "extraBody": {
            "statusCode": "FAST_ENTRY_V3_OTP_REQUIRED",
            "error": "",
            "data": {
            "email": "",
            "emailHint": "",
            "phone": "79780638151",
            "otpId": 0,
            "otpChannel": "CHANNEL_PHONE",
            "otpAddress": "79780638151",
            "otp": "",
            "isCheckAllowed": True,
            "resendAfter": 0,
            "otpLength": 6,
            "firstOtpSentToEmail": False,
            "activeOtpSentToEmail": False,
            "IsEmailRegistrationState": False,
            "isExtraOtpRequested": True,
            "extraOtpChannel": "CHANNEL_EMAIL",
            "extraOtpAddress": extraOtpAddress,
            "extraOtpId": extraOtpId,
            "extraIsCheckAllowed": True,
            "ExtraResendAfter": 40,
            "accessToken": "",
            "tokenType": "",
            "expiresIn": 0,
            "refreshToken": "",
            "isRegistration": False,
            "isLongTimeNoSee": False,
            "isValuableAccount": False,
            "hideHints": False,
            "isRecognized": False,
            "isSecondFactor": True,
            "isEmployeeLogin": False,
            "isOtpExpired": False,
            "isAdsAllowed": True,
            "isVerifiedEmailError": False,
            "isForceSmsOtp": False,
            "isForceFlashCallOtp": False,
            "isFlashCallFailed": False,
            "countryCode": "RU",
            "isSeller": True,
            "isAccountRecoveryAllowed": True,
            "sellerCountry": "",
            "secondFactorCase": "SELLER_DIRECTOR",
            "hasBankAccount": False
            }
        }
        }
    params_json = json.dumps(params_json)
    response = driver.execute_script(
        f'''
        var xhr = new XMLHttpRequest();
        var params = {params_json};
        var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1";
        xhr.open('POST', url, false);
        xhr.send(JSON.stringify(params));
        return xhr.responseText;
    ''')
    
    response = json.loads(response)
    authRequestToken = response['state']['submitButton']['data']['authRequestToken']
    csrfToken = response['state']['submitButton']['data']['csrfToken']
    
    insert_code_email(driver, authRequestToken, csrfToken, extraOtpId)
    
    
def insert_code_email(driver, authRequestToken, csrfToken, extraOtpId):
    code = input('Введите код: ')
    time.sleep(3)
    params_json = {
        "phone": "79780638151",
        "isVerifiedEmail": False,
        "isSecondFactor": False,
        "isValuableAccount": False,
        "firstOtpSentToEmail": False,
        "activeOtpSentToEmail": False,
        "isRecognized": False,
        "authRequestToken": authRequestToken,
        "isAlphaNumericOtp": False,
        "isExtraOtpRequested": True,
        "extraOtpId": extraOtpId,
        "hideHints": False,
        "csrfToken": csrfToken,
        "isOtpExpired": False,
        "isAdsAllowed": True,
        "isVerifiedEmailError": False,
        "isForceSmsOtp": False,
        "IsEmailRegistrationState": False,
        "isForceFlashCallOtp": False,
        "otpSentToPush": False,
        "otpSentToChainPushNc": False,
        "countryCode": "RU",
        "widgetName": "csma.loginOrRegistration",
        "isSeller": False,
        "isAccountRecoveryAllowed": False,
        "sellerCountry": "",
        "secondFactorCase": "",
        "hasBankAccount": False,
        "extraOtp": code
        }
    params_json = json.dumps(params_json)
    
    
    response = driver.execute_script(
        f'''
        var xhr = new XMLHttpRequest();
        var params = {params_json};
        var url = "https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3";
        xhr.open('POST', url, false);
        xhr.send(JSON.stringify(params));
        return xhr.responseText;
    ''')
    response = json.loads(response)
    error = response['error']
    print(response)
    if error == "Неверный код. Попробуйте ещё раз":
        print('Неверный код, попробуйте еще раз')
    driver.get('https://ozon.ru')
    time.sleep(500)
    
    




class api_ozon_class:
    
    def __init__(self, timeon):
        self.time = timeon

    
    
    async def cabinets(self):
        pass
    
    
# 1606810
# options.add_argument(f"--user-data-dir={os.getcwd()}\\kwork11\\profiles\\users") #e.g. 