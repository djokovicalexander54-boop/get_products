import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask
import threading
import os
from google import genai
from openai import OpenAI
from pypdf import PdfReader, PdfWriter
import random
import asyncio
import random
# headers for number : 0911 855 2199
HH_0 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Cookie":"did=669b6986-df43-43a3-8b27-5373c7b3ec87; cdid=16ea83bc-d011-4033-846d-b1b312417809; _gcl_au=1.1.1851772210.1789818076; _ga=GA1.1.936183600.1789818077; city=tehran; referrer=; _vid_t=Wg17lsxe/spNfkU5V7YSZN9ryxO/C2ZGKsmN8zuyGQLPThMndOSBB4ruwmBA6FaBUJhb9C83EHp9WA==; multi-city=tehran%7C; ff=%7B%22f%22%3A%7B%22device_fp_enable%22%3Atrue%2C%22enable-places-selector-online-search-web%22%3Atrue%2C%22chat_message_disabled%22%3Atrue%2C%22web_sentry_sample_rate%22%3A0.2%2C%22web_sentry_traces_sample_rate%22%3A0.01%2C%22is_web_proactive_refresh_enabled%22%3Atrue%2C%22post-stats-batch-event-web-max-batch-size%22%3A%2220%22%2C%22post-stats-batch-event-web-flush-interval-sec%22%3A%2220%22%2C%22divar_default_call_center%22%3A%22neda%22%2C%22is_circle_location_enabled%22%3Atrue%2C%22web_client_exporter_page_load_sample_rate%22%3A0.5%7D%2C%22e%22%3A1790232146947%2C%22r%22%3A1790314946947%7D; resolution_width=875; theme=light; token=; sAccessToken=eyJraWQiOiJkLTE3ODk4Mjg0NzAxNDQiLCJ0eXAiOiJKV1QiLCJ2ZXJzaW9uIjoiNCIsImFsZyI6IlJTMjU2In0.eyJpYXQiOjE3OTAyMzc0NjgsImV4cCI6MTc5MDI0NzgyOSwic3ViIjoiMzVhYzgzNDItNzBjZS00OWExLTk0MWEtYmFmNDQyM2QxYmIyIiwidElkIjoicHVibGljIiwic2Vzc2lvbkhhbmRsZSI6IjZjNzk2ZjY0LTg5NTItNDcyZi05NDAyLTI5MTE1NmU0YWVjNiIsInJlZnJlc2hUb2tlbkhhc2gxIjoiZmEyYjcxZTEzM2JmOTEwNTcxZDI0ZTJmZDVkZjlkMDE4MzY1NzBiMjBjMTQ3NmU3NDdlNDA2YWRkMjE0MTE4NyIsInBhcmVudFJlZnJlc2hUb2tlbkhhc2gxIjpudWxsLCJhbnRpQ3NyZlRva2VuIjpudWxsLCJpc3MiOiJodHRwczovL2FwaS5kaXZhci5pci92OC9hdXRoZW50aWNhdGUiLCJwaG9uZU51bWJlciI6Iis5ODkxMTg1NTIxOTkiLCJzdC1wZXJtIjp7InQiOjE3OTAyMzc0NjgyNzIsInYiOltdfSwic3Qtcm9sZSI6eyJ0IjoxNzkwMjM3NDY4MjcyLCJ2IjpbXX19.PVQ6L6lQIw4z9R65SExFhZ8sSvdpsQJzKG7aZoWvAvhDzB_X4ynC7TK5qu92_JHxn0wtiAXHBO-xLH-uhCQ1VTPw5lj0RyVavNnM7jvT35gPSavNNTOWdK4LSIEw2pymj4zzdgWRrYJPtOrU3FLG8m5EasOfSEnQbGIeDcIaMiolWL7NIqa2yBi6jEuBK8Nmy1iZRe4WzSxwS6_0-JkDGbqW9CWe5LZJYecNo5qJCeM_ADrSl4U4QZxGye1jq8r6WqIdjgWzRx2peDmHkFF6fsWbq-74jz2yCgkPcNUcVRhvm6PZCCiMevV-fLbjqF_IW0ao_yD9rI9ds_HTOkY50A; sFrontToken=eyJ1aWQiOiIzNWFjODM0Mi03MGNlLTQ5YTEtOTQxYS1iYWY0NDIzZDFiYjIiLCJhdGUiOjE3OTAyNDc4MjkwMDAsInVwIjp7ImFudGlDc3JmVG9rZW4iOm51bGwsImV4cCI6MTc5MDI0NzgyOSwiaWF0IjoxNzkwMjM3NDY4LCJpc3MiOiJodHRwczovL2FwaS5kaXZhci5pci92OC9hdXRoZW50aWNhdGUiLCJwYXJlbnRSZWZyZXNoVG9rZW5IYXNoMSI6bnVsbCwicGhvbmVOdW1iZXIiOiIrOTg5MTE4NTUyMTk5IiwicmVmcmVzaFRva2VuSGFzaDEiOiJmYTJiNzFlMTMzYmY5MTA1NzFkMjRlMmZkNWRmOWQwMTgzNjU3MGIyMGMxNDc2ZTc0N2U0MDZhZGQyMTQxMTg3Iiwic2Vzc2lvbkhhbmRsZSI6IjZjNzk2ZjY0LTg5NTItNDcyZi05NDAyLTI5MTE1NmU0YWVjNiIsInN0LXBlcm0iOnsidCI6MTc5MDIzNzQ2ODI3MiwidiI6W119LCJzdC1yb2xlIjp7InQiOjE3OTAyMzc0NjgyNzIsInYiOltdfSwic3ViIjoiMzVhYzgzNDItNzBjZS00OWExLTk0MWEtYmFmNDQyM2QxYmIyIiwidElkIjoicHVibGljIn19; csid=8778a0bb2cc6dedab6; _ga_1G1K17N77F=GS2.1.s1790237288$o27$g1$t1790237485$j26$l0$h0"
}
# headers for number : 0922 054 4571
HH_1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:156.0) Gecko/20100101 Firefox/15",
    "Accept": "*/*",
    "Cookie":"did=7e251f52-f2fd-4fc1-9658-f1dae48402be; cdid=f0a03429-a904-48d4-bbea-a19669cb057b; _gcl_au=1.1.2013526149.1789842491; _ga_1G1K17N77F=GS2.1.s1790238556$o3$g1$t1790238606$j10$l0$h0; _ga=GA1.1.598642937.1789842491; csid=04e608ceb22a28d342; resolution_width=1920; theme=light; ff=%7B%22f%22%3A%7B%22device_fp_enable%22%3Atrue%2C%22enable-places-selector-online-search-web%22%3Atrue%2C%22chat_message_disabled%22%3Atrue%2C%22web_sentry_sample_rate%22%3A0.2%2C%22web_sentry_traces_sample_rate%22%3A0.01%2C%22is_web_p…NoMSI6bnVsbCwicGhvbmVOdW1iZXIiOiIrOTg5MjIwNTQ0NTcxIiwicmVmcmVzaFRva2VuSGFzaDEiOiJhYWE1NTBiNGQ1YjMyZWYzZmY4OWU0NzYyOTYzMDY4Y2RkYzBlOWEwNDM0MDFjMzFhZjI2YmZlZDVmNGI2NjgwIiwic2Vzc2lvbkhhbmRsZSI6ImE2MDI4ZTcyLWU0ZGUtNDdhMC04MTA4LTA1NGU4MDAyOTg5NSIsInN0LXBlcm0iOnsidCI6MTc5MDIzODU4NTM3MiwidiI6W119LCJzdC1yb2xlIjp7InQiOjE3OTAyMzg1ODUzNzIsInYiOltdfSwic3ViIjoiYWYxYjcwZjYtMWFlMS00ZTQ3LWFlYWQtOTMxZmVkYzM5MjM0IiwidElkIjoicHVibGljIn19; _vid_t=CfPgOf5eTt8M82pAuVLPKHamoQJJCtU2D8aAgSjYIcRhbKhOoee0Hv+p3pFNhBwlt+912OZIQFjxGw=="
}
# headers for number : 0936 163 4571
HH_3 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Cookie":""
}
fa_numbers = "۰۱۲۳۴۵۶۷۸۹"
en_numbers = "0123456789"
proxy_list = ["http://109.122.240.157:8118",
        "socks4://81.12.89.74:4153",
        "socks4://85.133.250.27:80",
        "socks4://194.31.108.109:2080",
        "http://194.31.108.109:2080",
        "socks5://87.107.68.231:1081",
        "http://85.9.87.26:8080",
        "http://80.191.46.62:1090",
        "http://89.46.219.133:80",
        "http://81.12.70.98:8080",
        "http://85.133.250.27:80",
        "socks5://62.60.210.173:1080",
        "http://31.14.124.45:8080",
        "http://185.118.153.110:8080",
        "http://81.90.144.170:9000",
        "http://93.118.109.220:8080"]
TOKEN ="8818973935:AAE4Zr7QVS0FjrA09AmEcy-bT1FMqwh7nGg"
bot = Bot(TOKEN)
# ساخت قالب پی دی اف
pdfmetrics.registerFont(TTFont('Vazir', "Vazirmatn-Bold.ttf"))
doc = SimpleDocTemplate("pdf_divar.pdf", pagesize=letter)
styles = getSampleStyleSheet()
fa_style = ParagraphStyle(
    'FarsiStyle',
    parent=styles['Normal'],
    fontName='Vazir',
    fontSize=18,
    leading=20,
    alignment=2
)
fa_style_0 = ParagraphStyle(
    'FarsiStyle_0',
    parent=styles['Normal'],
    fontName='Vazir',
    fontSize=25,
    leading=20,
    alignment=1
)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
API_url = "https://api.divar.ir/v8/postlist/w/search"
# هدر جهت دریافت مشخصات کلی آگهی ها
headers = {
    "Accept": "application/json",
    "Baggage": "sentry-environment=client,sentry-release=the-wall-v14-127-2,sentry-public_key=7e7d19d51ebe4bd5955fda8ab50107b1,sentry-trace_id=c5ef694737a35294a1094db798f8ed1d,sentry-sampled=false,sentry-sample_rand=0.12389261611242897,sentry-sample_rate=0.01"
}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام. در این ربات آزمایشی، آگهی های مربوط به کاریابی و استخدام فروشگاه ها و رستوران ها، از سایت دیوار جمع آوری و برای شما نمایش داده میشوند")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا صبر کنید تا اطلاعات آگهی ها از سایت جمع آوری شود...")
    i=1
    u=0
    t=1
    m=1
    zx=1
    story = [] 
    title_list = []
    with open("title_text.txt", "w", encoding="utf-8") as file:
        while u<=0:
            if t==1:
                play = {"source_view":"CATEGORY","pagination_data":{
                "@type":"type.googleapis.com/post_list.PaginationData","last_post_date":"2026-09-22T17:54:48.708176Z","page":1,"layer_page":1,
                "search_uid":"890682aa-8ab2-472c-bc93-4c771c10dc0b"},
                "search_data":{"form_data":{"data":{"category":{"str":{"value":"shop-restaurant"}}}}},
                "city_ids":["1"]}
                t=2
            else:
                play = {"source_view":"CATEGORY","pagination_data":{
                "@type":"type.googleapis.com/post_list.PaginationData","last_post_date":LPD,"page":P,"layer_page":LP,
                "search_uid":SU},
                "search_data":{"form_data":{"data":{"category":{"str":{"value":"shop-restaurant"}}}}},
                "city_ids":["1"]}        
            site_text = requests.post(API_url, json=play, headers=headers).json()
            data_list = site_text["list_widgets"]
            for data in data_list:
                title = str(data["data"]["action"]["payload"]["web_info"]["title"])
                if title not in title_list:
                    title_list.append(title)
                    token = str(data["data"]["action"]["payload"]["token"])
                    location = str(data["data"]["action"]["payload"]["web_info"]["city_persian"])
                    try:
                        image_link = str(data["data"]["image_url"])
                    except:
                        image_link = "در تیتر آگهی نوشته نشده"
                    advertisement_link = f"https://divar.ir/v/{title}/{token}"
                    try:
                        max_pay = str(data["data"]["top_description_text"])
                    except:
                        max_pay = "در تیتر آگهی نوشته نشده"
                    try:
                        type_pay = str(data["data"]["middle_description_text"])
                    except:
                        type_pay = "در تیتر آگهی نوشته نشده"
                    try:
                        time = str(data["data"]["bottom_description_text"])
                    except:
                        time = "در تیتر آگهی نوشته نشده"
                    # دریافت اطلاعات تماس
                    for prox in proxy_list:
                        try:
                            RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HH_0).json()
                            number_0 = RRR["widget_list"][0]["data"]["value"]
                            tran = str.maketrans(fa_numbers,en_numbers)
                            number = str(number_0).translate(tran)
                            LL =list(number)
                            if len(LL) == 11:
                                number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                            print(number, flush=True)
                            break
                        except Exception as e:
                            await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
                            print("NO HERE.. 1", flush=True)
                            await asyncio.sleep(5)
                            try:
                                RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HH_1).json() 
                                number_0 = RRR["widget_list"][0]["data"]["value"]
                                tran = str.maketrans(fa_numbers,en_numbers)
                                number = str(number_0).translate(tran)
                                LL =list(number)
                                if len(LL) == 11:
                                    number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                print(number, flush=True)
                                break
                            except Exception as e:
                                await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
                                print("NO HERE.. 2", flush=True)
                                await asyncio.sleep(5)
                                try:
                                    RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HH_3).json()
                                    number_0 = RRR["widget_list"][0]["data"]["value"]
                                    tran = str.maketrans(fa_numbers,en_numbers)
                                    number = str(number_0).translate(tran)
                                    LL =list(number)
                                    if len(LL) == 11:
                                        number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                    print(number, flush=True)
                                    break
                                except Exception as e:
                                    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
                                    #  استفاده از پروکسی های چرخشی
                                    print("NO HERE.. 3", flush=True)
                                    await asyncio.sleep(5)
                                    try:
                                        RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HH_0, proxies=prox).json()
                                        number_0 = RRR["widget_list"][0]["data"]["value"]
                                        tran = str.maketrans(fa_numbers,en_numbers)
                                        number = str(number_0).translate(tran)
                                        LL =list(number)
                                        if len(LL) == 11:
                                            number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                        print(number, flush=True)
                                        break
                                    except Exception as e:
                                        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
                                        print("NO HERE.. 4", flush=True)
                                        await asyncio.sleep(5)
                                        try:
                                            RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HH_1, proxies=prox).json() 
                                            number_0 = RRR["widget_list"][0]["data"]["value"]
                                            tran = str.maketrans(fa_numbers,en_numbers)
                                            number = str(number_0).translate(tran)
                                            LL =list(number)
                                            if len(LL) == 11:
                                                number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                            print(number, flush=True)
                                            break
                                        except Exception as e:
                                            await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
                                            print("NO HERE.. 5", flush=True)
                                            await asyncio.sleep(5)
                                            try:
                                                RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HH_3, proxies=prox).json()
                                                number_0 = RRR["widget_list"][0]["data"]["value"]
                                                tran = str.maketrans(fa_numbers,en_numbers)
                                                number = str(number_0).translate(tran)
                                                LL =list(number)
                                                if len(LL) == 11:
                                                    number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                                print(number, flush=True)
                                                break
                                            except Exception as e:
                                                await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
                                                print("we can not!! try again IP", flush=True)
                                                await asyncio.sleep(3)
                                                number = "do not find"
                    #---------------------------------------------------------------
                    try:
                        RR = requests.get(f"https://api.divar.ir/v8/posts-v2/web/{token}", headers=headers).json()
                        text = str(RR["sections"][2]["widgets"][1]["data"]["text"]) # توضیحات آگهی
                    except Exception as e:
                        text ="موردی یافت نشد !!"
                    file.write(f"شماره {m} : {str(title)}, توضیحات : \n {text} \n \n \n \n \n \n  -----------------------------------------------------------------  \n \n \n \n \n")
                    m+=1
                    number_A = Paragraph(get_display(arabic_reshaper.reshape(f"آگهی شماره {i}")), fa_style)
                    i+=1
                    story.append(number_A)
                    story.append(Spacer(1,20))
                    T_title = Paragraph(get_display(arabic_reshaper.reshape(f"عنوان : {title}")), fa_style)
                    story.append(T_title)
                    story.append(Spacer(1,20))
                    image = Paragraph(get_display(arabic_reshaper.reshape(f"<a href='{image_link}'><font color='red'><u>جهت مشاهده عکس آگهی کلیک کنید</u></font></a>")), fa_style)
                    story.append(image)
                    story.append(Spacer(1,20))
                    L_location = Paragraph(get_display(arabic_reshaper.reshape(f"مکان : {location}")), fa_style)
                    story.append(L_location)
                    story.append(Spacer(1,20))
                    P_max_pay = Paragraph(get_display(arabic_reshaper.reshape(f"مبلغ : {max_pay}")), fa_style)
                    story.append(P_max_pay)
                    story.append(Spacer(1,20))
                    TY_type_pay = Paragraph(get_display(arabic_reshaper.reshape(f"نوع پرداخت : {type_pay}")), fa_style)
                    story.append(TY_type_pay)
                    story.append(Spacer(1,20))
                    TT_time = Paragraph(get_display(arabic_reshaper.reshape(f"زمان : {time}")), fa_style)
                    story.append(TT_time)
                    story.append(Spacer(1,20))
                    EXPLAIN = Paragraph(get_display(arabic_reshaper.reshape("توضیحات :")), fa_style)
                    story.append(EXPLAIN)
                    story.append(Spacer(1,20))
                    T_text = Paragraph(get_display(arabic_reshaper.reshape(text)), fa_style)
                    story.append(T_text)
                    story.append(Spacer(1,20))
                    I_phone = Paragraph(get_display(arabic_reshaper.reshape(f"phone number : {number}"), fa_style_0))
                    story.append(I_phone)
                    story.append(Spacer(1,20))
                    link = Paragraph(get_display(arabic_reshaper.reshape(f"<a href='{advertisement_link}'><font color='blue'><u>برای مشاهده جزئیات کامل آگهی در سایت دیوار کلیک کنید</u></font></a>")), fa_style)
                    story.append(link)
                    story.append(Spacer(1,20))
                    story.append(PageBreak())
                if zx==2:
                    u=1
                    break
                else:
                    zx+=1
            print(f"{len(title_list)} --> OK {u}", flush=True)
            LPD = site_text["pagination"]["data"]["last_post_date"]
            P = site_text["pagination"]["data"]["page"]
            LP = site_text["pagination"]["data"]["layer_page"]
            SU = site_text["pagination"]["data"]["search_uid"]
            u+=1
        doc.build(story)
    key_list = []
    DD = "pdf_divar.pdf"
    await context.bot.send_message(chat_id=update.effective_chat.id, text="آگهی ها آماده هست")
    key_list.append([InlineKeyboardButton(text="ارسال PDF تمام آگهی ها", callback_data=f"K${DD}")])
    key_list.append([InlineKeyboardButton(text="استفاده از هوش مصنوعی جهت فیلتر کردن", callback_data=f"M_")])
    reply = InlineKeyboardMarkup(key_list)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="برای مشاهده تمام آگهی های حوزه استخدام و کاریابی فروشگاه ها و رستوران ها، گزینه اول را کلیک کنید \n در غیر این صورت اگر میخواهید فقط آگهی هایی مربوط به استخدام نیرو متخصص رستوران را دریافت کنید، گزینه دوم را کلیک کنید تا هوش مصنوعی فقط آگهی های این حوزه را برای شما بفرستد", reply_markup=reply)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
async def click_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mm = update.callback_query
    await mm.answer()
    data = mm.data
    if data.startswith("K$"):
        pdf = data.split("$")[1]
        with open(pdf, "rb") as pdf_data:
            if pdf_data:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=pdf_data, caption="تمام آگهی های حوزه استخدام و کاریابی فروشگاه ها و رستوران ها")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="pdf یافت نشد !!!")
    # فیلتر کردن آگهی های موردنیاز توسط هوش مصنوعی
    elif data.startswith("M_"):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="استفاده از مدل هوش مصنوعی در ربات تستی، بدلیل کمبود زمان ساخت نمونه تستی، امکان پذیر نیست!!!")
        #text_long = None
        #await context.bot.send_message(chat_id=update.effective_chat.id, text="در حال تلاش برای ارتباط گیری با مدل هوش مصنوعی...")
        #MM = "pdf_divar.pdf"
        # خواندن پی دی اف
        #READ = PdfReader(MM)
        #text_long = ""
        #for page in READ.pages:
        #    text = page.extract_text()
        #    if text:
        #        text_long+= f"{text} \n"
        #if text_long is not None:
        #    explain_user = "سلام. من کارگاه قطعه بندی مرغ (ران رستورانی سایز،فیله مرغ،سینه بدون استخوان، بال بازو،) دارم. لطفا اگهی های مربوط به استخدام نیرو متخصص رستوران مثل سر اشپز کمک اشپز و .. پیدا کن"
        #    sentence = f"لطفا با توجه به این متن : {explain_user}, تمام آگهی های مربوط به این توضیحات را از این متنی که فرستاده میشود پیدا کن. سپس فقط و فقط شماره آگهی آنها رو که در فایل وجود دارد، بصورت یک لیست بده. لطفا سعی کن شماره صفحه آگهی هایی رو پیدا کنی که مطابق با توضیحات یا شباهت زیادی با آن داشته باشند. بقیه آگهی ها رو درنظر نگیر.لطفا هیچ توضیح اضافه ای نده، فقط لیست شماره آگهی ها رو بفرست. متن آگهی ها به این شرح است : {text_long}"
        #    k=1
        #    while k==1:
        #        try:
        #            key = os.getenv("key_gemini")
        #            gemini_ai = genai.Client(api_key=key)
        #            responce = gemini_ai.models.generate_content( 
        #                model = f"gemini-3.5-flash", 
        #                contents=[sentence]
        #            )
        #            await context.bot.send_message(chat_id=update.effective_chat.id, text=str(responce.text))
        #            k=2
        #            break
        #        except Exception as e:
        #            await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
        #            await asyncio.sleep(30)
            # ساخت پی دی اف جدید
            # پاسخ هوش مصنوعی یک لیستی از شماره ها خواهد بود که باید در هنگام ساخت پی دی اف جدید فقط این شماره ها آگهی ها باید وجود داشته باشند
        #    new_list = [1,4,5,7,10] # برای تست این لیست فرضی رو بعنوان پاسخ هوش مصنوعی در نظر میگیریم. در واقع باید داشته باشیم new_list = responce.text
        #    first_pdf = "pdf_divar.pdf" # پی دی اف اولیه
        #    new_pdf = "new_pdf_divar.pdf" # پی دی اف جدید
        #    reader =PdfReader(first_pdf) # خواندن پی دی اف اولیه
        #    writer = PdfWriter() # آماده سازی پی دی اف جدید جهت ساختن
        #    new_list_0 = [q-1 for q in new_list]
        #    for index, page in enumerate(reader.pages):
        #        if index in new_list_0:
        #            writer.add_page(page)
        #    with open(new_pdf, "wb") as f:
        #        writer.write(f)
        #    with open(new_pdf, "rb") as ff:
        #        if ff:
        #            await context.bot.send_document(chat_id=update.effective_chat.id, document=ff, caption="آگهی های فیلتر شده توسط هوش مصنوعی")
        #        else:
        #            await context.bot.send_message(chat_id=update.effective_chat.id, text="pdf یافت نشد !!!!")
        #else:
        #    await context.bot.send_message(chat_id=update.effective_chat.id, text="متن pdf خوانده نشد..")
appp = Flask(__name__)
@appp.route("/")
def home():
    return "running..."
def help():
    port = int(os.environ.get("PORT", 5000))
    appp.run(host='0.0.0.0', port=port)
if __name__ == '__main__':
    threading.Thread(target=help, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(click_data))
    print("yes", flush=True)
    app.run_polling()
# https://api.divar.ir/v8/postcontact/web/contact_info_v2/gauq5_if
# https://api.divar.ir/v8/postcontact/web/contact_info_v2/gag-GubZ
