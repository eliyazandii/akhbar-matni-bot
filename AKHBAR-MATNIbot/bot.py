import time
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN   = "8541225332:AAEf2ndNwokYM43Gq5NGl5tX-5aliicTe_4"
CHANNEL_ID  = "@Akhbar_Matni"

# منابع:
SOURCES = {
    "general": "https://www.isna.ir/rss",             # اخبار عمومی
    "sports":  "https://www.khabaronline.ir/rss/tp/6" # اخبار ورزشی
}

CHECK_EVERY = 120   # هر ۲ دقیقه
sent_titles = set()  # جلوگیری از تکراری‌ها در همان اجرا


def get_latest_item(url):
    """خواندن اولین خبر از RSS"""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        root = ET.fromstring(r.content)
        item = root.find("./channel/item")

        if item is None:
            print("❌ Hich itemi peyda nashod.")
            return None, None

        title = item.find("title").text or ""
        desc_tag = item.find("description")
        desc = desc_tag.text if desc_tag is not None else ""

        return title.strip(), desc.strip()

    except Exception as e:
        print("❌ Error:", e)
        return None, None


def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)


# قالب اخبار عمومی
def format_general(title, desc):
    return (
        f"📰 <b>{title}</b>\n\n"
        f"{desc}\n\n"
        "———————————————\n"
        "برای دریافت آخرین اخبار روز، کانال اخبار متنی را دنبال کنید 📰\n"
        "@Akhbar_Matni"
    )


# قالب اخبار ورزشی
def format_sports(title, desc):
    return (
        "🏅 <b>خبر ورزشی</b>\n\n"
        f"📰 <b>{title}</b>\n\n"
        f"{desc}\n\n"
        "———————————————\n"
        "برای دریافت آخرین اخبار روز، کانال اخبار متنی را دنبال کنید 📰\n"
        "@Akhbar_Matni"
    )


def main():
    print("🚀 Robot Akhbar Matni start shod...")

    while True:
        # بررسی اخبار عمومی
        title_g, desc_g = get_latest_item(SOURCES["general"])
        if title_g and title_g not in sent_titles:
            sent_titles.add(title_g)
            msg = format_general(title_g, desc_g)
            send_to_telegram(msg)
            print("✔ General ersal shod:", title_g)

        # بررسی اخبار ورزشی
        title_s, desc_s = get_latest_item(SOURCES["sports"])
        if title_s and title_s not in sent_titles:
            sent_titles.add(title_s)
            msg = format_sports(title_s, desc_s)
            send_to_telegram(msg)
            print("✔ Sports ersal shod:", title_s)

        print("⏳ Checking again...")
        time.sleep(CHECK_EVERY)



if __name__ == "__main__":
    main()
