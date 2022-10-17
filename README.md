# dqx_rpc
![SnapShot](https://cdn.discordapp.com/attachments/866343429223088198/1031527930716762172/2022-10-17_200718.png)

https://hiroba.dqx.jp/sc/character/\<cid\>/friendlist/をスクレイピングして自分がいるサーバーとエリアの情報を取得し、Discordに表示する非公式ツールです。

# 必要なもの

* Python実行環境
* Discordに表示させたいDQXのキャラ
* 上記のフレンドのキャラ

# 使い方
config.jsonを正しく設定し、必要なモジュールをインストールしてdqx_rpc.pyを実行するだけです。

# config.jsonの設定

ここでは例としてAA111-111の情報を表示したいものとし、BB222-222がフレンドだとします。

`target_character_id`にAA111-111を設定します。

`friend_token`には[https://hiroba.dqx.jp/sc/](https://hiroba.dqx.jp/sc/)にBB222-222としてログインした際のCookieの`sm_open_5`の値を設定します。
![Cookie](https://cdn.discordapp.com/attachments/866343429223088198/1031528207222059078/token_open_sm5.png)

# 制限

当然ですがフレンド(例の場合はBB222-222)が行ったことない場所は？？？？？として表示されます