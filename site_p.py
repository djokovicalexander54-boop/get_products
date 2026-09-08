from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Bot
import requests
import os
from flask import Flask, render_template
import threading
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN_key")
bot = Bot(TOKEN)
name_list = []
price_list = []
comment_list = []
image_list = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Authorization": "Bearer 3601352|2pchDqCyyHVTbmIbTvvJ1Gx7r2U7NDCvQPI7oTAPgYf3cNPKXt3zqsHjPa9dkrY681x7dXxDRbtdsBoo3BwGQF7nQ1BU027uLW8AurwFz11zmEfODYodQyNMg3KIdx5vX6SAnKWS0h0uiPn8E4dk0eYYVeM2HBmI0DHyhf1fCr7mZ6xf5BYYj27V97clMuj7Gkx7uoaElyR7VvBK7HmZrx0SEd17wVXDihL9jPEkJT2vXZr910WxOXhDfOVHNQKAaXrCxpBom3JhJz4TUXv2IK2AtNbaoOY3uXJVI9kCPgugo0bJfu9byE3ZRryGZlByW9hlZiptQEf91vCR88cKhty1ai2GX7JvwJhrjv8Hlt0Eg4TK9UjTnrX33XVIMkt4ozkfBP8c9wdroHdstLSofqyIw5lHfjhARnxkd95pwLbTEldt9yTMAalfWjRTTevGHnuyHECuNgBJcLRKTSVHMHkO6QN9oig52LX6pA6aPNeGQaQog38H9zQkNt33adJpdh7aVfe3BfYH1UR2cg625uWGt11k",
    "Accept": "application/json",
    "Cookie": "_ga=GA1.1.628874232.1763970736; _ym_uid=1763970736422822680; _ym_d=1763970736; tracker_glob_new=dU6Q8eT; ab_test_experiments=%5B%22229ea1a233356b114984cf9fa2ecd3ff%22%2C%224905b18f64695e6dbfd739d20a4ae2c0%22%2C%22f0fd80107233fa604679779d7e121710%22%2C%22ff6e05e42fe897c23b7ed9bfa93e9373%22%2C%2237136fdc21e0b782211ccac8c2d7be63%22%5D; _sp_ses.13cb=*; PHPSESSID=00u8ss4jc9tfd30qc08hlup1sj; tracker_session=dZftEMX; TS01b9d479=0181654207017da64abe3ab865bfe38867079f7796d6f8035cbda1fbbf8a880597b3840206e06c661a89495a9c9538a88443b7ffd2903530b6887e59f20ff8313cc4818563990e3ad48c26aea66f5c0d43aa85b2b9; TS01b6ea4d=01816542076c252359bedd2274d0f6dcbd9dd74dbbd6f8035cbda1fbbf8a880597b384020627665b36500c762db4ce55f388bb9f7bf1cf6a8f821f72b11752448771cdfa3ab8a1a20395f5743933a813962d95a429; TS01c77ebf=01023105919f7f30bc99b6dc8a3494395ad19880c3f743915daaa70230412c1e91031b5c91eeba917d382a129d1ac79d6f5a29e047; _sp_id.13cb=4cfaffba-ff9b-4a42-a43f-13db96f93e4d.1767360169.60.1788585520.1788552733.b32a1298-9e74-4005-8dbc-e73d6056ca7d.a0ac33de-c4b9-445b-8f3e-4fbe11633281.e34968d3-67a6-43c2-a8a0-2305e4d1fcfd.1788585504994.17; _ga_QQKVTD5TG8=GS2.1.s1788585507$o70$g1$t1788585526$j41$l0$h0"
}
url = "https://api.digikala.com/v1/categories/mobile-phone/brands/samsung/search/?page=1"
site_code = requests.get(url, headers=headers)
id_list_1 = []
id_list_2 = []
image_url = []
products = site_code.json()["data"]["products"]
for item in products:
    id_1 = item["id"]
    id_2 = item["url"]["params"][0]["variant_id"]
    image = item["images"]["main"]["url"][0]
    id_list_1.append(id_1)
    id_list_2.append(id_2)
    image_url.append(image)
i=0
image_list = image_url
for data in id_list_1:
    url_01 = f"https://api.digikala.com/v2/product/{data}/?product_id={data}&variant_id={id_list_2[i]}"
    site_dode_01 = requests.get(url_01, headers=headers)
    name = str(site_dode_01.json()["data"]["data_layer"]["ecommerce"]["detail"]["products"][0]["name"])
    price000 = str(site_dode_01.json()["data"]["data_layer"]["ecommerce"]["detail"]["products"][0]["price"])
    price00 = list(price000)
    del price00[-1]
    price0 = "".join(price00)
    price = f"{int(price0):,}"
    data_type = type(site_dode_01.json()["data"]["product"]["comments_overview"])
    name_list.append(name)
    price_list.append(price)
    if data_type==dict:
        all_comment = site_dode_01.json()["data"]["product"]["comments_overview"]["overview"] # خلاصه دیدگاه ها
        comment_list.append(str(all_comment))
    elif data_type==list:
        comments = site_dode_01.json()["data"]["product"]["last_comments"]
        comment = comments[0]["body"]
        comment_list.append(str(comment))
    i+=1
    if i==18:
        break
    print(f"ok --> {i}", flush=True)
print("yes men...", flush=True)
app = Flask(__name__)
@app.route("/")
def home():
    return render_template(
        "site_phone.html",
        names = name_list,
        prices = price_list,
        comment_site = comment_list,
        image = image_list
    )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id , text="سلام. در این ربات میتوانید محصولات موبایل سایت دیجی کالا را مشاهده کنید")
    reply = InlineKeyboardMarkup([[InlineKeyboardButton(text="مشاهده محصولات", url="https://telegold.ir")]])
    await context.bot.send_message(chat_id=update.effective_chat.id , text="برای مشاهده محصولات، کلیک کنید", reply_markup=reply)
async def start1(message, update: Update ,context:ContextTypes.DEFAULT_TYPE):
    if 'send_text' in message.text:
        id_name = update.effective_user.first_name
        await context.bot.send_message(chat_id=update.effective_chat.id , text=f"کاربر {id_name}، شما از سایت محصولات موبایل به اینجا هدایت شدید")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id , text="این ربات صرفا برای تست است")
def run_bot():
    app1 = Application.builder().token(TOKEN).build()
    app1.add_handler(CommandHandler("start",start))
    app1.add_handler(CommandHandler("start1",start1))
    app1.run_polling()
threading.Thread(target=run_bot).start()
port = int(os.environ.get("PORT",80))
app.run(host="0.0.0.0", port=port, debug=False)
