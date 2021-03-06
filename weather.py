import configparser
import datetime
import requests
import os
import logging.config

# コンフィグファイル読み込み
inifile = configparser.ConfigParser()
inifile.read("config.ini")

# ログコンフィグファイル読み込み
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("root")

# 本日の日付を取得
today = str(datetime.date.today())

# 帰宅時間を取得
back_time = inifile.get("back_time", "back_time")

# 天気情報取得パラメータ設定
city_id = inifile.get("openweathermap", "city_id")
app_id = inifile.get("openweathermap", "app_id")
params = {"id": city_id, "APPID": app_id}
headers = {"content-type": "application/json"}

# 天気情報を取得
response = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=params, headers=headers)
data = response.json()

# 本日の帰宅時間の天気情報を抽出
weather_today_back_time = ""
for date_time in data["list"]:
    if date_time["dt_txt"].startswith(today) and date_time["dt_txt"].endswith(back_time):
        weather_today_back_time = date_time["weather"][0]["main"]
        logging.info("The weather of going home time: " + weather_today_back_time)

# もし悪天候であればGoogleHomeを喋らせるNodeJSを実行
if weather_today_back_time == "Rain" or weather_today_back_time == "Snow" or weather_today_back_time == "Thunderstorm":
    js_file = inifile.get("googlehomenotifier", "js_file")
    command = "/usr/local/bin/node " + js_file
    os.system(command)
