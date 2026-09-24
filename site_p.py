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
    fontSize=18,
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
                    # اطلاعات تماس
                    HH = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
                        "Accept": "application/json",
                        "Cookie": "did=669b6986-df43-43a3-8b27-5373c7b3ec87; cdid=16ea83bc-d011-4033-846d-b1b312417809; _gcl_au=1.1.1851772210.1789818076; theme=light; _ga=GA1.1.936183600.1789818077; city=tehran; referrer=; _vid_t=Wg17lsxe/spNfkU5V7YSZN9ryxO/C2ZGKsmN8zuyGQLPThMndOSBB4ruwmBA6FaBUJhb9C83EHp9WA==; csid=f9052dd026834078e2; multi-city=tehran%7C; sAccessToken=eyJraWQiOiJkLTE3ODk4Mjg0NzAxNDQiLCJ0eXAiOiJKV1QiLCJ2ZXJzaW9uIjoiNCIsImFsZyI6IlJTMjU2In0.eyJpYXQiOjE3OTAyMjg1NDYsImV4cCI6MTc5MDIzODgzMiwic3ViIjoiOWFmMDI0ODItMDNmYy00NjAxLWJlMTMtM2Y0YmZhOGRiN2U1IiwidElkIjoicHVibGljIiwic2Vzc2lvbkhhbmRsZSI6IjA2YWY0NTEzLTZiOTctNGFjZS05MTRlLTEyZDk5M2U2NjA4MyIsInJlZnJlc2hUb2tlbkhhc2gxIjoiMmYzYjRhZTJhNWU5YjhmMGNkNjI4ZmVhYzdlM2Y5YjEzYzNlOTZlNjc0ODE0ZGQwZjFhNzE4ZTE5NTRhZWUzNiIsInBhcmVudFJlZnJlc2hUb2tlbkhhc2gxIjoiZjVhNWRlMzc3MWExYThiMDkzNjk2M2QxZGYyYzYxYTk5ZTZiNTVkY2IxYjkwM2I5ZGNkMWQ1ZWYzMzgyODhmYSIsImFudGlDc3JmVG9rZW4iOm51bGwsImlzcyI6Imh0dHBzOi8vYXBpLmRpdmFyLmlyL3Y4L2F1dGhlbnRpY2F0ZSIsInBob25lTnVtYmVyIjoiKzk4OTM2MTYzNDU3MSIsInN0LXBlcm0iOnsidCI6MTc5MDIyODU0NiwidiI6W119LCJzdC1yb2xlIjp7InQiOjE3OTAyMjg1NDYsInYiOltdfX0.u9vDVE_LqT7VgDFML3-J-NnAl9TzwFa98VT8OEkm6s0W3a_dwDCRM5s_b5cuS-iYDnCc1QXl2QT0WkzhaehZe0-y9CWc35DUCvxC05LtbGxDggTHYoEtWW5K60bpclFZau3JCgiO07LpvoNB9lhI_nyqPyRleGI9Yt4JBz_KVKhl5jGG6_B07Q2z-4924ZpfFaqpR6omc9uCCoDWH3PL2RHsFsNRO1tWlTRDnU3NYQfUJTKe0KdDlI0BfZ_xquQHzQ5yynCe-5CgBTLiv4ijNme_fB4sK7mTz-2vxJubsHkEvihZQyaS59nKVaeq_b9KEgvtKeeMRzMMjyACDLOCQQ; sFrontToken=eyJ1aWQiOiI5YWYwMjQ4Mi0wM2ZjLTQ2MDEtYmUxMy0zZjRiZmE4ZGI3ZTUiLCJhdGUiOjE3OTAyMzg4MzIwMDAsInVwIjp7ImFudGlDc3JmVG9rZW4iOm51bGwsImV4cCI6MTc5MDIzODgzMiwiaWF0IjoxNzkwMjI4NTQ2LCJpc3MiOiJodHRwczovL2FwaS5kaXZhci5pci92OC9hdXRoZW50aWNhdGUiLCJwYXJlbnRSZWZyZXNoVG9rZW5IYXNoMSI6ImY1YTVkZTM3NzFhMWE4YjA5MzY5NjNkMWRmMmM2MWE5OWU2YjU1ZGNiMWI5MDNiOWRjZDFkNWVmMzM4Mjg4ZmEiLCJwaG9uZU51bWJlciI6Iis5ODkzNjE2MzQ1NzEiLCJyZWZyZXNoVG9rZW5IYXNoMSI6IjJmM2I0YWUyYTVlOWI4ZjBjZDYyOGZlYWM3ZTNmOWIxM2MzZTk2ZTY3NDgxNGRkMGYxYTcxOGUxOTU0YWVlMzYiLCJzZXNzaW9uSGFuZGxlIjoiMDZhZjQ1MTMtNmI5Ny00YWNlLTkxNGUtMTJkOTkzZTY2MDgzIiwic3QtcGVybSI6eyJ0IjoxNzkwMjI4NTQ2LCJ2IjpbXX0sInN0LXJvbGUiOnsidCI6MTc5MDIyODU0NiwidiI6W119LCJzdWIiOiI5YWYwMjQ4Mi0wM2ZjLTQ2MDEtYmUxMy0zZjRiZmE4ZGI3ZTUiLCJ0SWQiOiJwdWJsaWMifX0=; ff=%7B%22f%22%3A%7B%22device_fp_enable%22%3Atrue%2C%22enable-places-selector-online-search-web%22%3Atrue%2C%22chat_message_disabled%22%3Atrue%2C%22web_sentry_sample_rate%22%3A0.2%2C%22web_sentry_traces_sample_rate%22%3A0.01%2C%22is_web_proactive_refresh_enabled%22%3Atrue%2C%22post-stats-batch-event-web-max-batch-size%22%3A%2220%22%2C%22post-stats-batch-event-web-flush-interval-sec%22%3A%2220%22%2C%22divar_default_call_center%22%3A%22neda%22%2C%22is_circle_location_enabled%22%3Atrue%2C%22web_client_exporter_page_load_sample_rate%22%3A0.5%7D%2C%22e%22%3A1790232146947%2C%22r%22%3A1790314946947%7D; _ga_1G1K17N77F=GS2.1.s1790228549$o26$g1$t1790228560$j49$l0$h0; resolution_width=875"
                    }
                    try:
                        RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HH).json()
                        title = str(RRR["widget_list"][0]["data"]["title"]) 
                        number = str(RRR["widget_list"][0]["data"]["value"])
                        phone = f"{title} : {number}"
                        print(phone, flush=True)
                        await asyncio.sleep(1)
                    except:
                        try:
                            prox = proxy_list[random.randint(0,15)]
                            print(prox, flush=True)
                            RRR = requests.post(f"https://api.divar.ir/v8/postcontact/web/contact_info_v2/{token}", headers=HH, proxies=prox).json()
                            title = str(RRR["widget_list"][0]["data"]["title"]) 
                            number = str(RRR["widget_list"][0]["data"]["value"])
                            phone = f"{title} : {number}"
                            print(phone, flush=True)
                            await asyncio.sleep(1)
                        except:
                            phone = "اطلاعات تماس یافت نشد"
                    #------------
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
                    I_phone = Paragraph(get_display(arabic_reshaper.reshape(phone), fa_style))
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
