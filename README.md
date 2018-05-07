# never-forget-umbrella
## Introduction
朝は晴れていたのに、帰宅時間にちょうど雨に降られて残念な気持ちになった経験はありませんか？
never-forget-umbrellaを使えば、濡れて帰ることも、突発的にビニール傘で出費することも、雨が止むまで無駄な残業をする必要もなくなります。なぜならば、GoogleのAIスピーカーが出勤前に傘を持っていく必要があるかどうかを自発的に喋って教えてくれるからです。

## Product Movie
[完成物の動画](https://www.youtube.com/watch?v=UumwTBwXvbU)をYouTubeに投稿しました。

## Algorithm OverView
1. cronで[OpenWeatherMap](https://openweathermap.org/)のREST-APIを利用して指定都市の天気情報取得
2. あらかじめ設定した帰宅時間帯の天気が悪天候（雨、雪、雷のいずれか）であればGoogle Homeに音声通知リクエスト
3. Google Homeが音声通知

<img width="518" alt="2018-05-05 14 00 53" src="https://user-images.githubusercontent.com/19632119/39659853-eba9bd7e-506c-11e8-86e3-ed83885ade90.png">

## Deploy
### 前提
- ServerとGoogleHomeがネットワークで接続されている。
- Serverにpythonとpython-pipとnode.jsとgoogle-home-notifierとgitがインストール済み。

### 動作確認環境
- rasbian 8.0
- python 3.6.4
- pip 9.0.1
- node V9.8.0
- git 2.1.4

### 手順
#### OpenWeatherMapのAPPID取得
[OpenWeatherMap](https://openweathermap.org/)でアカウント登録し、APPIDを取得する。（無料）
後にコンフィグ設定で必要になる。

#### never-forget-umbrellaをclone
```
$ git clone https://github.com/gold-kou/never-forget-umbrella.git
```

#### main.jsをgoogle-home-notifierディレクトリに移動
上記cloneしたmain.jsファイルを自身のgoogle-home-notifierディレクトリにコピーする。

```
$ cp main.js <your google-home-notifier directory>
```

#### config.iniの設定
config.iniファイルを自身の環境に応じて設定する。

```
$ vi config.ini
[back_time]
back_time = 18:00:00 ←自身の予想帰宅時間を00:00:00、03:00:00、06:00:00、09:00:00、12:00:00、15:00:00、18:00:00、21:00:00の中から選択して設定する。デフォルトでは18:00:00。

[openweathermap]
city_id = 1850147 ← http://bulk.openweathermap.org/sample/に記載されている都市のIDを設定する。デフォルトではTokyo。
app_id = ←自身のOpenWeatherMapのAPPIDを設定する。デフォルトでは空。

[googlehomenotifier]
js_file = ←main.jsファイルを配置した場所を絶対パスで指定する。デフォルトでは空。
```

#### requestsモジュールのインストール
REST-APIを実行するために必要なpythonのrequestsモジュールをインストールする。

```
$ sudo pip install requests
```

#### crontabの編集をvimでできるように設定
必須ではないが、vimの方が編集しやすい方はこの設定をする。

```
$ export EDITOR=vim.basic
```

#### cron設定
ここでは月曜日〜金曜日の毎朝8時にcronするように設定する。

```
$ crontab -e
以下行を末尾に追記
00 8 * * 1-5 $HOME/.pyenv/shims/python <your github directory>/never-forget-umbrella/weather.py
```

## その他
### /var/log/umbrella.logへの書き込みエラーが発生する
権限の問題の可能性があります。権限設定を適切に設定するか、cron実行ユーザの書き込みアクセス可能な適当なディレクトリにログを書き込むようにlogging.confのhandler_fileHandlerセクションのargsの値を書き換えてください。

### コンフィグ関連でKeyErrorが発生する
weather.pyのコンフィグファイル(config.iniとlogging.conf)読み込みのパスを自身の環境に応じて絶対パスで指定してください。

### WARNINGログに関して
homebridgeでWARNINGログが出力されますが、以下の通り問題ないです。
https://github.com/nfarina/homebridge/blob/master/README.md#errors-on-startup

### GUIは無いのか？
現状はGUIを実装しておらず、設定はコンフィグからのみとなっております。
