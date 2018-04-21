const googlehome = require('google-home-notifier')
const language = 'ja';

googlehome.device('Google-Home', language);
googlehome.ip("192.168.11.3");
googlehome.notify('今日の帰宅時間頃は天気が崩れそうです。傘を忘れずに。', function(res) {
  console.log(res);
});