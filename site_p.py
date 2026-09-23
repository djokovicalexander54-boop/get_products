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
                    link = Paragraph(get_display(arabic_reshaper.reshape(f"<a href='{advertisement_link}'><font color='blue'><u>برای مشاهده جزئیات کامل آگهی در سایت دیوار کلیک کنید</u></font></a>")), fa_style)
                    story.append(link)
                    story.append(Spacer(1,20))
                    story.append(PageBreak())
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
        ffg = None
        text_long = None
        await context.bot.send_message(chat_id=update.effective_chat.id, text="در حال تلاش برای ارتباط گیری با مدل هوش مصنوعی...")
        MM = "pdf_divar.pdf"
        # خواندن پی دی اف
        READ = PdfReader(MM)
        text_long = ""
        for page in READ.pages:
            text = page.extract_text()
            if text:
                text_long+= f"{text} \n"
        if text_long is not None:
            explain_user = "سلام. من کارگاه قطعه بندی مرغ (ران رستورانی سایز،فیله مرغ،سینه بدون استخوان، بال بازو،) دارم. لطفا اگهی های مربوط به استخدام نیرو متخصص رستوران مثل سر اشپز کمک اشپز و .. پیدا کن"
            sentence = f"لطفا با توجه به این متن : {explain_user}, تمام آگهی های مربوط به این توضیحات را از این متنی که فرستاده میشود پیدا کن. سپس فقط و فقط شماره آگهی آنها رو که در فایل وجود دارد، بصورت یک لیست بده. لطفا سعی کن شماره صفحه آگهی هایی رو پیدا کنی که مطابق با توضیحات یا شباهت زیادی با آن داشته باشند. بقیه آگهی ها رو درنظر نگیر.لطفا هیچ توضیح اضافه ای نده، فقط لیست شماره آگهی ها رو بفرست. متن آگهی ها به این شرح است : {text_long}"
            try:
                key = os.getenv("key_gemini")
                gemini_ai = genai.Client(api_key=key)
                #pdf_file_A = gemini_ai.files.upload(file=MM)
                responce = gemini_ai.models.generate_content( 
                    model = f"gemini-3.6-flash", 
                    contents=[sentence]
                )
                await context.bot.send_message(chat_id=update.effective_chat.id, text=str(responce.text))
            except Exception as e:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
                key_0 = os.getenv("key_llama")
                try:
                    cv = OpenAI(
                        base_url = "https://api.groq.com/openai/v1", 
                        api_key = key_0 
                    )
                    responce = cv.chat.completions.create( 
                        model = "llama-3.3-70b-versatile", 
                        messages=[{"role":"user", "content":sentence}] 
                    )
                    ai_answer = responce.choices[0].message.content
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=ai_answer)
                except Exception as e: 
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
            if ffg is None:
                # ساخت پی دی اف جدید
                # پاسخ هوش مصنوعی یک لیستی از شماره ها خواهد بود که باید در هنگام ساخت پی دی اف جدید فقط این شماره ها آگهی ها باید وجود داشته باشند
                new_list = [1,4,5,7,10] # برای تست این لیست فرضی رو بعنوان پاسخ هوش مصنوعی در نظر میگیریم. در واقع باید داشته باشیم new_list = responce.text
                first_pdf = "pdf_divar.pdf" # پی دی اف اولیه
                new_pdf = "new_pdf_divar.pdf" # پی دی اف جدید
                reader =PdfReader(first_pdf) # خواندن پی دی اف اولیه
                writer = PdfWriter() # آماده سازی پی دی اف جدید جهت ساختن
                new_list_0 = [q-1 for q in new_list]
                for index, page in enumerate(reader.pages):
                    if index in new_list_0:
                        writer.add_page(page)
                with open(new_pdf, "wb") as f:
                    writer.write(f)
                with open(new_pdf, "rb") as ff:
                    if ff:
                        await context.bot.send_document(chat_id=update.effective_chat.id, document=ff, caption="آگهی های فیلتر شده توسط هوش مصنوعی")
                    else:
                        await context.bot.send_message(chat_id=update.effective_chat.id, text="pdf یافت نشد !!!!")
            elif ffg is None:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="داداش!!! هوش مصنوعی کار نکرد..")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="متن pdf خوانده نشد..")
appp = Flask(__name__)
@appp.route("/")
def home():
    return "tiday is good..."
def help():
    port = int(os.environ.get("PORT", 5000))
    appp.run(host='0.0.0.0', port=port)
if __name__ == '__main__':
    threading.Thread(target=help, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(click_data))
    app.run_polling()
