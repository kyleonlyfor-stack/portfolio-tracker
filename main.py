import requests
import os


# =========================
# LARK CONFIG
# =========================

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
APP_TOKEN = os.getenv("APP_TOKEN")
TABLE_ID = os.getenv("TABLE_ID")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# =========================
# FINNHUB CONFIG
# =========================

FINNHUB_API_KEY = "d8cd689r01qidic7eqi0d8cd689r01qidic7eqig"

# =========================
# GET LARK ACCESS TOKEN
# =========================

auth_url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"

auth_payload = {
    "app_id": APP_ID,
    "app_secret": APP_SECRET
}

auth_response = requests.post(auth_url, json=auth_payload)

auth_data = auth_response.json()

tenant_access_token = auth_data["tenant_access_token"]

print("Lark Token 获取成功")

# =========================
# HEADERS
# =========================

headers = {
    "Authorization": f"Bearer {tenant_access_token}",
    "Content-Type": "application/json"
}

# =========================
# GET RECORDS
# =========================

records_url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"

print("Records URL:")
print(records_url)

records_response = requests.get(records_url, headers=headers)

records_data = records_response.json()

print("Records Response:")
print(records_data)

records = records_data["data"]["items"]

print("读取记录成功")

# =========================
# UPDATE ALL STOCK PRICES
# =========================

for record in records:

    fields = record["fields"]

    ticker = fields.get("Ticker")

    # 跳过空行
    if not ticker:
        continue

    print(f"正在更新: {ticker}")

    # =========================
    # GET STOCK PRICE
    # =========================

    quote_url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"

    quote_response = requests.get(quote_url)

    quote_data = quote_response.json()

    print("Quote Data:")
    print(quote_data)

    current_price = quote_data.get("c")

    # 如果价格为空
    if current_price is None:
        print(f"{ticker} 获取价格失败")
        continue

    print(f"{ticker} 当前价格: {current_price}")

    # =========================
    # UPDATE RECORD
    # =========================

    record_id = record["record_id"]

    update_url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"

    update_payload = {
        "fields": {
            "Current Price": current_price
        }
    }