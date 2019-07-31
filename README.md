# notifook

notifookはTwitterとFacebookで特定のユーザーの投稿を監視し、指定された正規表現に当て嵌る投稿をSlackに通知するエゴサーチソフトウェアです。

## 前提条件

動作には以下の環境が必要です。

- インターネットへのアクセス(具体的にはTwitter、Facebook、Slack)
- Python 3
- カレントディレクトリへのファイル読み書き権限
- cronやsystemd-timer

## 設定

環境変数に設定してください。
このフォルダにある`.env.sample`を`/etc/notifook.json`にコピーして中身を適宜書き換えて `source .env` しても良いと思います。

### SLACK

Slackへの通知に関する設定です。

|キー|概要|サンプル|
|---|---|-------|
|`TEXT`|投稿する際のお知らせテキスト|`新規投稿です`|
|`WEBHOOK`|incomingwebhookのアドレス|`https://hooks.slack.com/services/EXAMPLE/WEBHOOK/ADDRESS`|
|`username`|通知するBotの表示名|`エゴ太郎`|
|`channel`|通知先のチャンネル名|`#egosearch`|
|`icon_emoji`|通知するBotのアイコン|`:sunglasses:`|

### TWITTER

Twitterアカウントについての設定です。

|キー|概要|サンプル|
|---|---|-------|
|`TEXT`|投稿する際のTwitterのテキスト|`Twitterのリンクです`|
|`TOKEN`|Consumer KeyとConsumer Secretから作ったBearer token|`exampletwittertoken`|
|`SCREENNAME`|監視するアカウントのID|`twitterjp`|
|`REGEX`|通知対象の正規表現|`^.*凍結.*`|

### FACEBOOK

Facebookアカウントについての設定です。

|キー|概要|サンプル|
|---|---|-------|
|`TEXT`|投稿する際のFacebookのテキスト|`Facebookのリンクです`|
|`TOKEN`|Consumer KeyとConsumer Secretから作ったBearer token|`example|facebooktoken`|
|`SCREENNAME`|監視するアカウントのID|`FacebookJapan`|
|`REGEX`|通知対象の正規表現|`^.*Twitter.*`|

## 実行方法

1. このリポジトリをclone
2. `.env` に設定を書き込み(サンプルファイルをコピーすると楽です)
3. `$ source .env`
4. `$ python src/notifook.py`

## コマンドラインオプション

### -d/--dry

Webhookでの通知を行わず、コマンドラインに結果を表示します。

### -t/--twitter_oauth

TwitterのConsumer KeyとConsumer SecretからBearer tokenを生成します。

### -f/--facebook_oauth

FacebookのConsumer KeyとConsumer SecretからBearer tokenを生成します。

## 注意

カレントディレクトリ以下に前回投稿時のデータを吐くようになっています。
アクセス権限がない場合はエラーを吐いて止まりますので権限を与えてください。

あまりにも高頻度で監視をするとAPI規制にぶつかる可能性があります。
15分を目安に適切な頻度で監視するようにしてください。

