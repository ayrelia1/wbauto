
import requests
import json
import datetime
import random
from config import bot, Message
import time
import threading
from bs4 import BeautifulSoup
import json
import re
from markup import *
from apiozon.driver_selenium import get_user_browser
from seleniumrequests import Chrome


def _get_json_from_html(text_content: str, find: str):
    
    html_content = text_content.replace('\\\\"', '"').replace('}"', '}').replace('"{', '{').replace("'", '')

    pattern = re.compile(rf'window\.{find}\s*=\s*(.*?)}};\s*')

    match = pattern.search(html_content)
    if match:
        json_data = match.group(1) + '}'
        return json.loads(json_data)
    else:
        return {}

class auth:
    def register_user(profile, phone, id_session_phone, id_session_email):
        driver = get_user_browser(profile)
        time.sleep(0.3)  
        driver.get('https://seller.ozon.ru/app/registration/signin?auth=1')
        time.sleep(5)
        
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
            var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1";
            xhr.open('POST', url, false);
            xhr.send(JSON.stringify(params));
            return xhr.responseText;
        ''')
        
        response = json.loads(response)
        authRequestToken = response['state']['submitButton']['data']['authRequestToken']
        csrfToken = response['state']['submitButton']['data']['csrfToken']
        print(authRequestToken)
        print(csrfToken)
        time.sleep(0.3)  
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
            "phone": phone
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
        statusCode = response['statusCode']
        time.sleep(0.2)  
        
        params_json = {
            "asyncData": async_data,
            "extraBody": {
                "statusCode": "FAST_ENTRY_V3_OTP_REQUIRED",
                "error": "",
                "data": {
                "email": "",
                "emailHint": "",
                "phone": phone,
                "otpId": optId,
                "otpChannel": "CHANNEL_PHONE",
                "otpAddress": phone,
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
            var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1";
            xhr.open('POST', url, false);
            xhr.send(JSON.stringify(params));
            return xhr.responseText;
        ''')
        
        response = json.loads(response)
        authRequestToken = response['state']['backButton']['data']['authRequestToken']
        csrfToken = response['state']['backButton']['data']['csrfToken']
        
        
        time.sleep(2)
        
        auth.insert_code(driver, authRequestToken, csrfToken, optId, async_data, phone, id_session_phone, id_session_email, statusCode)
        
        
    def insert_code(driver: Chrome, authRequestToken, csrfToken, optId, async_data, phone, id_session_phone, id_session_email, statusCode):
        counter = 0
        while True:
            code = databasework.check_code_db(id_session_phone)
            if counter == 150: 
                #await bot.send_message(chat_id=, message_id=, text=)
                print('er phone')
                driver.quit()
                return
            if code != None:
                code = code['code']
                break
            time.sleep(1)
            counter += 1
        params_json = {
            "phone": phone,
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
        if error == "Неверный код. Попробуйте ещё раз" or statusCode != 'FAST_ENTRY_V3_OTP_REQUIRED':
            print('Неверный код, попробуйте еще раз')
            result = 'error'
            databasework.update_status_register_db(result, id_session_phone)
            driver.quit()
            return
        email = response['data']['email']
        emailHint = response['data']['emailHint']
        if emailHint == '' and email == '':
            driver.get('https://ozon.ru')
            time.sleep(2)
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
                "phone": phone,
                "otpId": 0,
                "otpChannel": "CHANNEL_PHONE",
                "otpAddress": phone,
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
            var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1";
            xhr.open('POST', url, false);
            xhr.send(JSON.stringify(params));
            return xhr.responseText;
        ''')
        
        response = json.loads(response)
        authRequestToken = response['state']['submitButton']['data']['authRequestToken']
        csrfToken = response['state']['submitButton']['data']['csrfToken']
            
            
        time.sleep(2)
        
        params_json = {
            "phone": phone,
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
        time.sleep(0.1)  
        
        params_json = {
            "asyncData": async_data,
            "extraBody": {
                "statusCode": "FAST_ENTRY_V3_OTP_REQUIRED",
                "error": "",
                "data": {
                "email": "",
                "emailHint": "",
                "phone": phone,
                "otpId": 0,
                "otpChannel": "CHANNEL_PHONE",
                "otpAddress": phone,
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
        time.sleep(0.2) 
        
        auth.insert_code_email(driver, authRequestToken, csrfToken, extraOtpId, phone, id_session_phone, id_session_email)
        
        
    def insert_code_email(driver: Chrome, authRequestToken, csrfToken, extraOtpId, phone, id_session_phone, id_session_email):
        counter = 0
        while True:
            code = databasework.check_code_db(id_session_email)
            if counter == 150: 
                #await bot.send_message(chat_id=, message_id=, text=)
                print('error')
                driver.quit()
                return
            if code != None:
                code = code['code']
                break
            time.sleep(1)
            counter += 1
        
        
        params_json = {
            "phone": phone,
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
            print('Неверный код. Попробуйте еще раз')
            result = 'error'
            databasework.update_status_register_db(result, id_session_phone)
            driver.quit()
            return 'Вы ввели неверный код! Попробуйте авторизоваться еще раз'
        driver.get('https://ozon.ru')
        driver.quit()



"""
import requests
import json
import datetime
import random
from config import bot, Message
import time
import threading
from bs4 import BeautifulSoup
import json
import re
from markup import *
from apiozon.driver_selenium import get_user_browser
from seleniumrequests import Chrome


def _get_json_from_html(text_content: str, find: str):
    
    html_content = text_content.replace('\\\\"', '"').replace('}"', '}').replace('"{', '{').replace("'", '')

    pattern = re.compile(rf'window\.{find}\s*=\s*(.*?)}};\s*')

    match = pattern.search(html_content)
    if match:
        json_data = match.group(1) + '}'
        return json.loads(json_data)
    else:
        return {}



class auth:
    
    def request(url: str, method: str, driver, json_data: dict = None):
        #json_data_str = json.dumps(json_data) if json_data else '{}'

        script = f'''
            let url = "{url}"
            let method = "{method}"
            let options = {{
                method: method,
            }};

            if ("POST" === method) {{
                options.body = JSON.stringify({json_data});
            }}

            let response = await fetch(url, options);

            return await response.text();
        '''

        resp = driver.execute_script(script)
        if json_data is not None:
            resp = json.loads(resp)

        return resp
    
    
    def register_user(profile, phone, id_session_phone, id_session_email):
        driver = get_user_browser(profile)

        time.sleep(1)
        driver.get('https://seller.ozon.ru/app/registration/signin?auth=1')
        time.sleep(1)
        
        html_content = driver.page_source
        match = re.search(r'asyncData":"([^"]+)"', html_content)
        if match:
            async_data = match.group(1)
        else:
            print("asyncData не найден.")
  
        # request_token = {
        #     'return_url': 'https://seller.ozon.ru/app/registration/signin?auth=1',
        #     'webhook_url': 'https://seller.ozon.ru/app/registration/signin?auth=1'
        # }
        # request_token = json.dumps(request_token)

        # driver.get('https://seller.ozon.ru/app/registration/signin?auth=1')
        # print(driver.page_source)
        # time.sleep(5)

        # #method='POST'
        # response = auth.request(url='https://seller.ozon.ru/api/ozon-id/request-token', method='POST', driver=driver, json_data=request_token)
        
        
        # driver.get('https://www.ozon.ru')
        # time.sleep(1)
        # driver.get('https://www.ozon.ru')
        # time.sleep(1)
        
        
        # time.sleep(1)
        # response = json.loads(response)
        # token = response['result']['token']
        # # response = driver.execute_script(
        # #     f'''
        # #     var xhr = new XMLHttpRequest();
        # #     var url = "https://www.ozon.ru/ozonid?token={token}";
        # #     xhr.open('GET', url, false);
        # #     xhr.send();
        # #     return xhr.responseText;
        # # ''')

        # response = auth.request(url=f'https://www.ozon.ru/ozonid?token={token}', method='GET', driver=driver)

        # html_content = response
        # async_data = _get_json_from_html(html_content, '__NUXT__.state')['layout'][0]['placeholders'][0]['widgets'][0]['asyncData']
        # print(async_data)
        # time.sleep(1)
        
        params_json = {
            "asyncData": async_data,
            }
        
        params_json = json.dumps(params_json)
        # response = driver.execute_script(
        #     f'''
        #     var xhr = new XMLHttpRequest();
        #     var params = {params_json};
        #     var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1";
        #     xhr.open('POST', url, false);
        #     xhr.send(JSON.stringify(params));
        #     return xhr.responseText;
        # ''')
        
        response = auth.request(url=f'https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1', method='POST', driver=driver, json_data=params_json)
        print(response)
        response = json.loads(response)
        authRequestToken = response['state']['submitButton']['data']['authRequestToken']
        csrfToken = response['state']['submitButton']['data']['csrfToken']
        print(authRequestToken)
        print(csrfToken)
        time.sleep(0.3)  
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
            "phone": phone
        }
        params_json = json.dumps(params_json)
        
        
        # response = driver.execute_script(
        #     f'''
        #     var xhr = new XMLHttpRequest();
        #     var params = {params_json};
        #     var url = "https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3";
        #     xhr.open('POST', url, false);
        #     xhr.send(JSON.stringify(params));
        #     return xhr.responseText;
        # ''')
        
        response = auth.request(url=f'https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3', method='POST', driver=driver, json_data=params_json)
        
        print(response)
        response = json.loads(response)
        optId = response['data']['otpId']
        statusCode = response['statusCode']
        time.sleep(0.2)  
        
        params_json = {
            "asyncData": async_data,
            "extraBody": {
                "statusCode": "FAST_ENTRY_V3_OTP_REQUIRED",
                "error": "",
                "data": {
                "email": "",
                "emailHint": "",
                "phone": phone,
                "otpId": optId,
                "otpChannel": "CHANNEL_PHONE",
                "otpAddress": phone,
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
        # response = driver.execute_script(
        #     f'''
        #     var xhr = new XMLHttpRequest();
        #     var params = {params_json};
        #     var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1";
        #     xhr.open('POST', url, false);
        #     xhr.send(JSON.stringify(params));
        #     return xhr.responseText;
        # ''')
        response = auth.request(url=f'https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1', method='POST', driver=driver, json_data=params_json)
        
        response = json.loads(response)
        authRequestToken = response['state']['backButton']['data']['authRequestToken']
        csrfToken = response['state']['backButton']['data']['csrfToken']
        
        
        time.sleep(2)
        
        auth.insert_code(driver, authRequestToken, csrfToken, optId, async_data, phone, id_session_phone, id_session_email, statusCode)
        
        
    def insert_code(driver: Chrome, authRequestToken, csrfToken, optId, async_data, phone, id_session_phone, id_session_email, statusCode):
        counter = 0
        while True:
            code = databasework.check_code_db(id_session_phone)
            if counter == 150: 
                #await bot.send_message(chat_id=, message_id=, text=)
                print('er phone')
                driver.quit()
                return
            if code != None:
                code = code['code']
                break
            time.sleep(1)
            counter += 1
        params_json = {
            "phone": phone,
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
        
        
        # response = driver.execute_script(
        #     f'''
        #     var xhr = new XMLHttpRequest();
        #     var params = {params_json};
        #     var url = "https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3";
        #     xhr.open('POST', url, false);
        #     xhr.send(JSON.stringify(params));
        #     return xhr.responseText;
        # ''')
        
        response = auth.request(url=f'https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3', method='POST', driver=driver, json_data=params_json)
        
        response = json.loads(response)
        error = response['error']
        print(response)
        if error == "Неверный код. Попробуйте ещё раз" or statusCode != 'FAST_ENTRY_V3_OTP_REQUIRED':
            print('Неверный код, попробуйте еще раз')
            result = 'error'
            databasework.update_status_register_db(result, id_session_phone)
            driver.quit()
            return
        email = response['data']['email']
        emailHint = response['data']['emailHint']
        if emailHint == '' and email == '':
            driver.get('https://ozon.ru')
            time.sleep(2)
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
                "phone": phone,
                "otpId": 0,
                "otpChannel": "CHANNEL_PHONE",
                "otpAddress": phone,
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
        # response = driver.execute_script(
        #     f'''
        #     var xhr = new XMLHttpRequest();
        #     var params = {params_json};
        #     var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1";
        #     xhr.open('POST', url, false);
        #     xhr.send(JSON.stringify(params));
        #     return xhr.responseText;
        # ''')
        response = auth.request(url=f'https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1', method='POST', driver=driver, json_data=params_json)
        
        response = json.loads(response)
        authRequestToken = response['state']['submitButton']['data']['authRequestToken']
        csrfToken = response['state']['submitButton']['data']['csrfToken']
            
            
        time.sleep(2)
        
        params_json = {
            "phone": phone,
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
        
        
        # response = driver.execute_script(
        #     f'''
        #     var xhr = new XMLHttpRequest();
        #     var params = {params_json};
        #     var url = "https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3";
        #     xhr.open('POST', url, false);
        #     xhr.send(JSON.stringify(params));
        #     return xhr.responseText;
        # ''')
        
        response = auth.request(url=f'https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3', method='POST', driver=driver, json_data=params_json)
        print(response)
        response = json.loads(response)
        extraOtpId = response['data']['extraOtpId']
        extraOtpAddress = response['data']['extraOtpAddress']
        time.sleep(0.1)  
        
        params_json = {
            "asyncData": async_data,
            "extraBody": {
                "statusCode": "FAST_ENTRY_V3_OTP_REQUIRED",
                "error": "",
                "data": {
                "email": "",
                "emailHint": "",
                "phone": phone,
                "otpId": 0,
                "otpChannel": "CHANNEL_PHONE",
                "otpAddress": phone,
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
        # response = driver.execute_script(
        #     f'''
        #     var xhr = new XMLHttpRequest();
        #     var params = {params_json};
        #     var url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1";
        #     xhr.open('POST', url, false);
        #     xhr.send(JSON.stringify(params));
        #     return xhr.responseText;
        # ''')
        
        response = auth.request(url=f'https://www.ozon.ru/api/composer-api.bx/widget/json/v2?widgetStateId=loginOrRegistration-312980-default-1', method='POST', driver=driver, json_data=params_json)
        
        response = json.loads(response)
        authRequestToken = response['state']['submitButton']['data']['authRequestToken']
        csrfToken = response['state']['submitButton']['data']['csrfToken']
        time.sleep(0.2) 
        
        auth.insert_code_email(driver, authRequestToken, csrfToken, extraOtpId, phone, id_session_phone, id_session_email)
        
        
    def insert_code_email(driver: Chrome, authRequestToken, csrfToken, extraOtpId, phone, id_session_phone, id_session_email):
        counter = 0
        while True:
            code = databasework.check_code_db(id_session_email)
            if counter == 150: 
                #await bot.send_message(chat_id=, message_id=, text=)
                print('error')
                driver.quit()
                return
            if code != None:
                code = code['code']
                break
            time.sleep(1)
            counter += 1
        
        
        params_json = {
            "phone": phone,
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
        
        
        # response = driver.execute_script(
        #     f'''
        #     var xhr = new XMLHttpRequest();
        #     var params = {params_json};
        #     var url = "https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3";
        #     xhr.open('POST', url, false);
        #     xhr.send(JSON.stringify(params));
        #     return xhr.responseText;
        # ''')
        
        response = auth.request(url=f'https://www.ozon.ru/api/composer-api.bx/_action/fastEntryV3', method='POST', driver=driver, json_data=params_json)
        
        response = json.loads(response)
        error = response['error']
        print(response)
        if error == "Неверный код. Попробуйте ещё раз":
            print('Неверный код. Попробуйте еще раз')
            result = 'error'
            databasework.update_status_register_db(result, id_session_phone)
            driver.quit()
            return 'Вы ввели неверный код! Попробуйте авторизоваться еще раз'
        driver.get('https://ozon.ru')
        driver.quit()



"""