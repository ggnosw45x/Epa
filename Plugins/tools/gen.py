import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re
from pyrogram.types import CallbackQuery
from datetime import datetime
from Plugins.db_lock import db_lock
from Plugins.Func import connect_to_db
from func_bin import get_bin_info
from func_gen import cc_gen


@Client.on_message(filters.command("gen", prefixes=['.','/','!','?'], case_sensitive=False) & filters.text & ~filters.regex(r'^/gen regen$'))
def gen_handler(client, message):
    tiempo = time.time()
    user_id = message.from_user.id
    with db_lock:
        conn = connect_to_db()
        cursor = conn.cursor()
    cursor.execute('SELECT rango, creditos, antispam, dias FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    if not user_data:
                  return message.reply(f"<b>You are not registered. Please use /register to sign up.</b> <a href='https://imgur.com/ihpUqrG.jpg'>&#8203;</a>")
    

    if user_data[0] in ["Baneado", "baneado"]:
        return message.reply(f"<b>You are not allowed to use the bot.❌\nReason: Baneado. </b>")
            
            
    username = message.from_user.username

    try:
            country = message.text.split()[1]
    except IndexError:
            message.reply("<b>Error, ejemplo: /rnd  <code>MX - CA - ES - US - FR - UK</code></b>")
            return

    global input

    if message.reply_to_message:
            input = re.findall(r'[0-9x]+', message.reply_to_message.text)
    else:
            input = re.findall(r'[0-9x]+', message.text)

    if not input:
        message.reply("USE BIEN LA HERRAMIENTA /gen 4556747")
        return
    
    
    bin_lasted = message.text[len('/gen '):] 
    
    
    user_id = message.from_user.id
    cursor.execute("UPDATE users SET bin_lasted = ? WHERE user_id = ?", (bin_lasted, user_id))
    conn.commit()
     

    #-----------FUNCION GNERADOR----------#
    if len(input)==1:
        cc = input[0]
        mes = 'x'
        ano = 'x'
        cvv = 'x'
    elif len(input)==2:
        cc = input[0]
        mes = input[1][0:2]
        ano = 'x'
        cvv = 'x'
    elif len(input)==3:
        cc = input[0]
        mes = input[1][0:2]
        ano = input[2]
        cvv = 'x'
    elif len(input)==4:
        cc = input[0]
        mes = input[1][0:2]
        ano = input[2]
        cvv = input[3]
    else:
        cc = input[0]
        mes = input[1][0:2]
        ano = input[2]
        cvv = input[3]                

    if len(input[0]) < 6: return message.reply('<b>Invalid Bin ⚠️</b>',quote=True)
            
    
    cc1,cc2,cc3,cc4,cc5,cc6,cc7,cc8,cc9,cc10 = cc_gen(cc,mes,ano,cvv)

    
    extra = str(cc) + 'xxxxxxxxxxxxxxxxxxxxxxx'
    if mes == 'x':
        mes_2 = 'rnd'
    else:
        mes_2 = mes
    if ano == 'x':
            ano_2 = 'rnd'
    else:
        ano_2 = ano
    if cvv == 'x':
        cvv_2 = 'rnd'
    else:
        cvv_2 = cvv

    x = get_bin_info(cc[0:6])
    
    buttons = InlineKeyboardMarkup(
             [
                [
                    InlineKeyboardButton(text='REGEN', callback_data=f'gen_callback')
                ]
             ]
        )

 
    #--------PLANTILLA--------#

    message.reply(f"""
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] 𝑲𝒖𝒓𝒂𝒎𝒂 𝑪𝒉𝒌
━━━━━━━━━━━━━                                                  
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] BIN: <code>{cc[0:6]}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] INFO: <code>{x.get("vendor")} / {x.get("type")} / {x.get("level")}</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] BANK: <code>{x.get("bank_name")} {x.get("flag")}</code>
━━━━━━━━━━━━━
<code>{cc1}</code><code>{cc2}</code><code>{cc3}</code><code>{cc4}</code><code>{cc5}</code><code>{cc6}</code><code>{cc7}</code><code>{cc8}</code><code>{cc9}</code><code>{cc10}</code>━━━━━━━━━━━━━
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] MONTO: <code>10</code>
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] CHK BY: @{username} [{user_data[0]}]
[<a href="https://t.me/RefeDarwinScrapper">✯</a>] OWNER BOT: @luisabinader1 </b>
""", reply_markup=buttons, disable_web_page_preview=True)
   

