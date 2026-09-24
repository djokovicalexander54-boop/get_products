import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from playwright.async_api import async_playwright
import asyncio
import random
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask
from flask import request
import threading
import os
import time as ww
from playwright_stealth import Stealth
# headers for number : 0911 855 2199
HH_0 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Baggage":"sentry-environment=client,sentry-release=the-wall-v14-133-9,sentry-public_key=7e7d19d51ebe4bd5955fda8ab50107b1,sentry-trace_id=26b71fc9f0d5534432ce468685a5b541,sentry-sampled=false,sentry-sample_rand=0.1081174376713877,sentry-sample_rate=0.01",
    "Cookie":"did=669b6986-df43-43a3-8b27-5373c7b3ec87; cdid=16ea83bc-d011-4033-846d-b1b312417809; _gcl_au=1.1.1851772210.1789818076; _ga=GA1.1.936183600.1789818077; city=tehran; referrer=; _vid_t=Wg17lsxe/spNfkU5V7YSZN9ryxO/C2ZGKsmN8zuyGQLPThMndOSBB4ruwmBA6FaBUJhb9C83EHp9WA==; multi-city=tehran%7C; theme=light; token=; csid=8778a0bb2cc6dedab6; _ga_1G1K17N77F=GS2.1.s1790255049$o29$g0$t1790255049$j60$l0$h0; sAccessToken=eyJraWQiOiJkLTE3ODk4Mjg0NzAxNDQiLCJ0eXAiOiJKV1QiLCJ2ZXJzaW9uIjoiNCIsImFsZyI6IlJTMjU2In0.eyJpYXQiOjE3OTAyNTUwNTAsImV4cCI6MTc5MDI2NTYxNiwic3ViIjoiMzVhYzgzNDItNzBjZS00OWExLTk0MWEtYmFmNDQyM2QxYmIyIiwidElkIjoicHVibGljIiwic2Vzc2lvbkhhbmRsZSI6IjZjNzk2ZjY0LTg5NTItNDcyZi05NDAyLTI5MTE1NmU0YWVjNiIsInJlZnJlc2hUb2tlbkhhc2gxIjoiYTc3ZjEwNzcxODYxZmMyOTRjYmVkZThjMTAyZTI0NTExODdlMjc5MGMyMzZmMDBiODdlZWVmNzgxNThmZmI3NiIsInBhcmVudFJlZnJlc2hUb2tlbkhhc2gxIjoiZmEyYjcxZTEzM2JmOTEwNTcxZDI0ZTJmZDVkZjlkMDE4MzY1NzBiMjBjMTQ3NmU3NDdlNDA2YWRkMjE0MTE4NyIsImFudGlDc3JmVG9rZW4iOm51bGwsImlzcyI6Imh0dHBzOi8vYXBpLmRpdmFyLmlyL3Y4L2F1dGhlbnRpY2F0ZSIsInBob25lTnVtYmVyIjoiKzk4OTExODU1MjE5OSIsInN0LXBlcm0iOnsidCI6MTc5MDI1NTA1MCwidiI6W119LCJzdC1yb2xlIjp7InQiOjE3OTAyNTUwNTAsInYiOltdfX0.XMkou4fH1BFFppIdfn89Qm4RS-cQbGvlkJ5UUjms-FOU4Ry5VbDnpRMkCmUqWUMSs42OoPWOzumYehd6VZOYv_KNNsn4qBopUN2m7EeaBlTY_yNd2nHMRw_bZsW6URHxunrjx7OkQqdsrTXaMJPCQWxylz2013HAsO8Ge-n5a0qObWFcnU8d-NFgDO61rZZqYRx5BHjeJSk6dNZlrsqZM9LkMFLDeYmzkYF9i_W7OL3Bgvylxp9-gXZBgPhi7Am55pHk_r372u00CuyzjAWezPmkPczB1zQLN7PWVAhfmSsK1j9l2RF-zjEN8fumzmhEm7RetcFtxnoJnK3r1Vh-BQ; sFrontToken=eyJ1aWQiOiIzNWFjODM0Mi03MGNlLTQ5YTEtOTQxYS1iYWY0NDIzZDFiYjIiLCJhdGUiOjE3OTAyNjU2MTYwMDAsInVwIjp7ImFudGlDc3JmVG9rZW4iOm51bGwsImV4cCI6MTc5MDI2NTYxNiwiaWF0IjoxNzkwMjU1MDUwLCJpc3MiOiJodHRwczovL2FwaS5kaXZhci5pci92OC9hdXRoZW50aWNhdGUiLCJwYXJlbnRSZWZyZXNoVG9rZW5IYXNoMSI6ImZhMmI3MWUxMzNiZjkxMDU3MWQyNGUyZmQ1ZGY5ZDAxODM2NTcwYjIwYzE0NzZlNzQ3ZTQwNmFkZDIxNDExODciLCJwaG9uZU51bWJlciI6Iis5ODkxMTg1NTIxOTkiLCJyZWZyZXNoVG9rZW5IYXNoMSI6ImE3N2YxMDc3MTg2MWZjMjk0Y2JlZGU4YzEwMmUyNDUxMTg3ZTI3OTBjMjM2ZjAwYjg3ZWVlZjc4MTU4ZmZiNzYiLCJzZXNzaW9uSGFuZGxlIjoiNmM3OTZmNjQtODk1Mi00NzJmLTk0MDItMjkxMTU2ZTRhZWM2Iiwic3QtcGVybSI6eyJ0IjoxNzkwMjU1MDUwLCJ2IjpbXX0sInN0LXJvbGUiOnsidCI6MTc5MDI1NTA1MCwidiI6W119LCJzdWIiOiIzNWFjODM0Mi03MGNlLTQ5YTEtOTQxYS1iYWY0NDIzZDFiYjIiLCJ0SWQiOiJwdWJsaWMifX0=; ff=%7B%22f%22%3A%7B%22device_fp_enable%22%3Atrue%2C%22enable-places-selector-online-search-web%22%3Atrue%2C%22chat_message_disabled%22%3Atrue%2C%22web_sentry_sample_rate%22%3A0.2%2C%22web_sentry_traces_sample_rate%22%3A0.01%2C%22is_web_proactive_refresh_enabled%22%3Atrue%2C%22post-stats-batch-event-web-max-batch-size%22%3A%2220%22%2C%22post-stats-batch-event-web-flush-interval-sec%22%3A%2220%22%2C%22divar_default_call_center%22%3A%22neda%22%2C%22is_circle_location_enabled%22%3Atrue%2C%22web_client_exporter_page_load_sample_rate%22%3A0.5%7D%2C%22e%22%3A1790258651062%2C%22r%22%3A1790341451062%7D; resolution_width=875"
}
# headers for number : 0922 054 4571
HH_1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:156.0) Gecko/20100101 Firefox/15",
    "Accept": "application/json",
    "baggage": "sentry-environment=client,sentry-release=release-the-wall-matching-24b9aaf0,sentry-public_key=7e7d19d51ebe4bd5955fda8ab50107b1,sentry-trace_id=cc59bfad3ea8eb0118fc1f202d9c7032,sentry-sampled=false,sentry-sample_rand=0.41833166717781656,sentry-sample_rate=0.01",
    "Cookie":"did=7e251f52-f2fd-4fc1-9658-f1dae48402be; cdid=f0a03429-a904-48d4-bbea-a19669cb057b; _gcl_au=1.1.2013526149.1789842491; _ga_1G1K17N77F=GS2.1.s1790254680$o4$g1$t1790255197$j60$l0$h0; _ga=GA1.1.598642937.1789842491; csid=04e608ceb22a28d342; resolution_width=1920; theme=light; ff=%7B%22f%22%3A%7B%22device_fp_enable%22%3Atrue%2C%22enable_shopping_journey%22%3Atrue%2C%22enable-places-selector-online-search-web%22%3Atrue%2C%22chat_message_disabled%22%3Atrue%2C%22web_sentry_sample_rate%22%3A0.2%2C%22web_sentry_tra…ZiZmVkNWY0YjY2ODAiLCJwaG9uZU51bWJlciI6Iis5ODkyMjA1NDQ1NzEiLCJyZWZyZXNoVG9rZW5IYXNoMSI6ImQyMzMxYjRlZmVhNTFhOGFjM2FjY2Q4MWI5NWYxYmExZWViYjQyMDFlMTU4ZWYzZTUzMWEwNTViZWYyMTg3MzIiLCJzZXNzaW9uSGFuZGxlIjoiYTYwMjhlNzItZTRkZS00N2EwLTgxMDgtMDU0ZTgwMDI5ODk1Iiwic3QtcGVybSI6eyJ0IjoxNzkwMjU1MTE3LCJ2IjpbXX0sInN0LXJvbGUiOnsidCI6MTc5MDI1NTExNywidiI6W119LCJzdWIiOiJhZjFiNzBmNi0xYWUxLTRlNDctYWVhZC05MzFmZWRjMzkyMzQiLCJ0SWQiOiJwdWJsaWMifX0=; _vid_t=CfPgOf5eTt8M82pAuVLPKHamoQJJCtU2D8aAgSjYIcRhbKhOoee0Hv+p3pFNhBwlt+912OZIQFjxGw=="
}
# headers for number : 0936 163 4571
HH_2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0",
    "Accept": "application/json",
    "Baggage": "sentry-environment=client,sentry-release=the-wall-v14-133-9,sentry-public_key=7e7d19d51ebe4bd5955fda8ab50107b1,sentry-trace_id=71e32b2217c17fe5b85167f259e84ce7,sentry-sampled=false,sentry-sample_rand=0.8462494725920517,sentry-sample_rate=0.01",
    "Cookie":"did=f21ed8e5-2be7-45d0-9c60-9e01e5a4d94a; cdid=55b7b597-e939-43c2-8791-7c94c67374f1; ff=%7B%22f%22%3A%7B%22device_fp_enable%22%3Atrue%2C%22enable-places-selector-online-search-web%22%3Atrue%2C%22chat_message_disabled%22%3Atrue%2C%22web_sentry_sample_rate%22%3A0.2%2C%22web_sentry_traces_sample_rate%22%3A0.01%2C%22is_web_proactive_refresh_enabled%22%3Atrue%2C%22post-stats-batch-event-web-max-batch-size%22%3A%2220%22%2C%22post-stats-batch-event-web-flush-interval-sec%22%3A%2220%22%2C%22divar_default_call_center%22%3A%22neda%22%2C%22web_client_exporter_page_load_sample_rate%22%3A0.5%7D%2C%22e%22%3A1790257737748%2C%22r%22%3A1790340537748%7D; referrer=; theme=light; _gcl_au=1.1.342277005.1790254139; _ga=GA1.1.1892709986.1790254140; sAccessToken=eyJraWQiOiJkLTE3ODk4Mjg0NzAxNDQiLCJ0eXAiOiJKV1QiLCJ2ZXJzaW9uIjoiNCIsImFsZyI6IlJTMjU2In0.eyJpYXQiOjE3OTAyNTQxNjcsImV4cCI6MTc5MDI2NDY0MSwic3ViIjoiOWFmMDI0ODItMDNmYy00NjAxLWJlMTMtM2Y0YmZhOGRiN2U1IiwidElkIjoicHVibGljIiwic2Vzc2lvbkhhbmRsZSI6Ijg5NTVlYTA3LTA3YWItNDgxYS1hNDEzLTgzMWIzZTViY2Y5NyIsInJlZnJlc2hUb2tlbkhhc2gxIjoiYjM5MjE0ZDVhMjBlNDA1ODNkNjEzNzJhNjM3Mzc1NDE0OTdmOTNlOTczMDQ0OGUwZDlkMDQ5ZTYyMDM4YWE3ZCIsInBhcmVudFJlZnJlc2hUb2tlbkhhc2gxIjpudWxsLCJhbnRpQ3NyZlRva2VuIjpudWxsLCJpc3MiOiJodHRwczovL2FwaS5kaXZhci5pci92OC9hdXRoZW50aWNhdGUiLCJwaG9uZU51bWJlciI6Iis5ODkzNjE2MzQ1NzEiLCJzdC1wZXJtIjp7InQiOjE3OTAyNTQxNjc5NzIsInYiOltdfSwic3Qtcm9sZSI6eyJ0IjoxNzkwMjU0MTY3OTcxLCJ2IjpbXX19.egPpoBjxrAXYVUuLFT3fF8KCe_aiGBgcLwIaENdOZWWcE4jhaRkwWfeC7yebdVxRIrc4DCAE6-R0MvApH5P90jKeNse3X_m93IhYoz9T3dkMuZG-TNT9WeLrKMb0XFFvpJj7IDy5kdx_J8tdCY70Aq4p-UnRhd6wRTKd9r_oMEWUHVfs8GzJsFckwczJyBvn6upaiqsmqcwxWUcSbd-tGEJCOcz4HCqqQnXM47k21LiUqEsIseXrzcr-SCf7ZXVTXaMeDxenecFGZpt3TqzfQ7a-Tt_kAftj6WJrHYAxMRfAsHxPrMEck0ZtCZqDzcdAswwqweY8wiNb8llkrfIXkQ; sFrontToken=eyJ1aWQiOiI5YWYwMjQ4Mi0wM2ZjLTQ2MDEtYmUxMy0zZjRiZmE4ZGI3ZTUiLCJhdGUiOjE3OTAyNjQ2NDEwMDAsInVwIjp7ImFudGlDc3JmVG9rZW4iOm51bGwsImV4cCI6MTc5MDI2NDY0MSwiaWF0IjoxNzkwMjU0MTY3LCJpc3MiOiJodHRwczovL2FwaS5kaXZhci5pci92OC9hdXRoZW50aWNhdGUiLCJwYXJlbnRSZWZyZXNoVG9rZW5IYXNoMSI6bnVsbCwicGhvbmVOdW1iZXIiOiIrOTg5MzYxNjM0NTcxIiwicmVmcmVzaFRva2VuSGFzaDEiOiJiMzkyMTRkNWEyMGU0MDU4M2Q2MTM3MmE2MzczNzU0MTQ5N2Y5M2U5NzMwNDQ4ZTBkOWQwNDllNjIwMzhhYTdkIiwic2Vzc2lvbkhhbmRsZSI6Ijg5NTVlYTA3LTA3YWItNDgxYS1hNDEzLTgzMWIzZTViY2Y5NyIsInN0LXBlcm0iOnsidCI6MTc5MDI1NDE2Nzk3MiwidiI6W119LCJzdC1yb2xlIjp7InQiOjE3OTAyNTQxNjc5NzEsInYiOltdfSwic3ViIjoiOWFmMDI0ODItMDNmYy00NjAxLWJlMTMtM2Y0YmZhOGRiN2U1IiwidElkIjoicHVibGljIn19; _vid_t=KuHD6TMzskqJax+H+Fl/XPcsE/jAGfW4QDuNuL9AdNn9/1C10iHLP9fNIJw8ADrUGgCZelBlaNF2qg==; multi-city=tehran%7C; city=tehran; csid=a5d0fc0d25d3b3ddd9; resolution_width=934; _ga_1G1K17N77F=GS2.1.s1790254139$o1$g1$t1790254277$j60$l0$h0"
}
#-----
HH_list = [HH_0,HH_1,HH_2]
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
#-----
fa_numbers = "۰۱۲۳۴۵۶۷۸۹"
en_numbers = "0123456789"
# ساخت قالب پی دی اف
pdfmetrics.registerFont(TTFont('Vazir', r"C:\Users\Karino\Desktop\Vazirmatn-Bold.ttf"))
doc = SimpleDocTemplate(r"C:\Users\Karino\Desktop\pdf_divar.pdf", pagesize=letter)
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
headers = {
    "Accept": "application/json",
    "Baggage": "sentry-environment=client,sentry-release=the-wall-v14-127-2,sentry-public_key=7e7d19d51ebe4bd5955fda8ab50107b1,sentry-trace_id=c5ef694737a35294a1094db798f8ed1d,sentry-sampled=false,sentry-sample_rand=0.12389261611242897,sentry-sample_rate=0.01"
}
i=1
u=0
t=1
m=1
zx=0
kk=1
story = [] 
title_list = []
qq_0=1
qq_1=1
qq_2=1
with open(r"C:\Users\Karino\Desktop\title_text.txt", "w", encoding="utf-8") as file:
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
                #-------------
                # دریافت اطلاعات تماس
                try:
                    k=1
                    q=1
                    HEAD = HH_list[0]
                    while k==1:
                        RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HEAD)
                        print(f"{RRR.status_code}-->{kk}", flush=True)
                        kk+=1
                        code = RRR.json()
                        try:
                            number_0 = code["widget_list"][0]["data"]["value"]
                        except:
                            number_0 = 50
                        if number_0!=50:
                            tran = str.maketrans(fa_numbers,en_numbers)
                            number = str(number_0).translate(tran)
                            LL =list(number)
                            if len(LL) == 11:
                                number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                            print(number, flush=True)
                            k=2
                            ww.sleep(5)
                        else:
                            if q==1:
                                if qq_0!=20:
                                    HEAD = HH_list[1]
                                    ww.sleep(5)
                                    q+=1
                            elif q==2:
                                if qq_1!=20:
                                    HEAD = HH_list[2]
                                    ww.sleep(5)
                                    q+=1
                            elif q==3:
                                for prox in proxy_list:
                                    RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HEAD, proxies=prox)
                                    print(f"{RRR.status_code}-->{kk} $$$ {prox}")
                                    kk+=1
                                    code = RRR.json()
                                    try:
                                        number_0 = code["widget_list"][0]["data"]["value"]
                                    except:
                                        number_0 = 60
                                    if number_0!=60:
                                        tran = str.maketrans(fa_numbers,en_numbers)
                                        number = str(number_0).translate(tran)
                                        LL =list(number)
                                        if len(LL) == 11:
                                            number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                        print(number, flush=True)
                                        k=2
                                        ww.sleep(5)
                                        break
                                    else:
                                        if q==1:
                                            if qq_0!=20:
                                                HEAD = HH_list[1]
                                                ww.sleep(5)
                                                q+=1
                                        elif q==2:
                                            if qq_1!=20:
                                                HEAD = HH_list[2]
                                                ww.sleep(5)
                                                q+=1
                                        else:
                                            number = "can not be find"
                                            print(number, flush=True)
                except Exception as e:
                    # شناسایی ربات شماره 911 855 2199
                    try:
                        k=1
                        q=1
                        HEAD = HH_list[1]
                        while k==1:
                            RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HEAD)
                            print(f"{RRR.status_code}-->{kk}")
                            kk+=1
                            code = RRR.json()
                            try:
                                number_0 = code["widget_list"][0]["data"]["value"]
                            except:
                                number_0 = 70
                            if number_0!=70:
                                tran = str.maketrans(fa_numbers,en_numbers)
                                number = str(number_0).translate(tran)
                                LL =list(number)
                                if len(LL) == 11:
                                    number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                print(number, flush=True)
                                k=2
                                ww.sleep(5)
                            else:
                                if q==1:
                                    if qq_0!=20:
                                        HEAD = HH_list[2]
                                        ww.sleep(5)
                                        q+=1
                                elif q==3:
                                    for prox in proxy_list:
                                        RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HEAD, proxies=prox)
                                        print(f"{RRR.status_code}-->{kk} $$$ {prox}")
                                        kk+=1
                                        code = RRR.json()
                                        try:
                                            number_0 = code["widget_list"][0]["data"]["value"]
                                        except:
                                            number_0 = 80
                                        if number_0!=80:
                                            tran = str.maketrans(fa_numbers,en_numbers)
                                            number = str(number_0).translate(tran)
                                            LL =list(number)
                                            if len(LL) == 11:
                                                number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                            print(number, flush=True)
                                            k=2
                                            ww.sleep(5)
                                            break
                                        else:
                                            if q==1:
                                                if qq_0!=20:
                                                    HEAD = HH_list[2]
                                                    ww.sleep(5)
                                                    q+=1
                                            else:
                                                number = "can not be find"
                                                print(number, flush=True)
                    except Exception as e:
                        # شناسایی ریات شماره 922 054 4571
                        try:
                            k=1
                            q=1
                            HEAD = HH_list[2]
                            while k==1:
                                RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HEAD)
                                print(f"{RRR.status_code}-->{kk}")
                                kk+=1
                                code = RRR.json()
                                try:
                                    number_0 = code["widget_list"][0]["data"]["value"]
                                except:
                                    number_0 = 90
                                if number_0!=90:
                                    tran = str.maketrans(fa_numbers,en_numbers)
                                    number = str(number_0).translate(tran)
                                    LL =list(number)
                                    if len(LL) == 11:
                                        number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                    print(number, flush=True)
                                    k=2
                                    ww.sleep(5)
                                else:
                                    for prox in proxy_list:
                                        RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HEAD, proxies=prox)
                                        print(f"{RRR.status_code}-->{kk} $$$ {prox}")
                                        kk+=1
                                        code = RRR.json()
                                        try:
                                            number_0 = code["widget_list"][0]["data"]["value"]
                                        except:
                                            number_0 = 100
                                        if number_0!=100:
                                            tran = str.maketrans(fa_numbers,en_numbers)
                                            number = str(number_0).translate(tran)
                                            LL =list(number)
                                            if len(LL) == 11:
                                                number = f"{LL[0]}{LL[1]}{LL[2]}{LL[3]}     {LL[4]}{LL[5]}{LL[6]}     {LL[7]}{LL[8]}{LL[9]}{LL[10]}"
                                            print(number, flush=True)
                                            k=2
                                            ww.sleep(5)
                                            break
                                        else:
                                            number = "can not be find"
                                            print(number, flush=True)
                        except Exception as e:
                            # شناسایی ربات شماره 936 163 4571
                            number = "can not be find"
                            print(number, flush=True)
                #-------------
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
                if zx==50:
                    u=1
                    break
                else:
                    zx+=1
        print(f"{len(title_list)} --> OK {u}")
        LPD = site_text["pagination"]["data"]["last_post_date"]
        P = site_text["pagination"]["data"]["page"]
        LP = site_text["pagination"]["data"]["layer_page"]
        SU = site_text["pagination"]["data"]["search_uid"]
        u+=1
    doc.build(story)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# فیلتر کردن آگهی های موردنیاز توسط هوش مصنوعی
