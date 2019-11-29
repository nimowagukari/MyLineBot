# 概要

本スクリプトは、Lambda と API Gateway を利用した LineBot です。  
Python と AWS 各種サービスを学習する目的で個人的に作った、とても単純なものです。  
現時点では下記程度のことしかできません。

- 発言に対して定期的にランダムで返信する ※あいづち機能
- "さよなら！"と書き込むとトークから退室してくれる ※Air Reading 機能

ソースコードのほとんどは、下記サイトを参考にしています。

[Lambdaでline-bot-sdk-pythonを使用してオウム返しBOTを作成する](https://qiita.com/konikoni428/items/fd1ab5993bc5526726bb)

## 使い方

ほぼ上記リンクに説明がありますが、流れを簡単に記載します。  
各項目の細かい手順は、ネット上により良い情報があふれているので割愛します。  
※スクリプト実行に必要なライブラリは同梱していないため、ライブラリのダウンロードおよびスクリプトとのマージ(zip化)のため、python(pip) が導入された環境が必要です。

### 1. Line 設定

- [公式サイト](https://developers.line.biz/ja/docs/messaging-api/getting-started/)を参考に Line Developers にてアカウント、プロバイダ、チャネルを作成する
- 作成したチャネル内で、チャネルアクセストークンを生成する
- 生成したチャネルアクセストークンとチャネルシークレットを控える

### 2. Lambda 設定

- AWS で Lambda 関数を作成する
- requirements.txt を利用し、ローカル環境の適当なパスで、`pip install -r requirements.txt -t <インストールフォルダ名>` にて必要なパッケージがインストールされたフォルダを作成する。
- lambda_function.py を上記フォルダに格納し、zip 圧縮する。
- 圧縮した zip を Lambda 関数にアップロードする。
- LINE設定にて控えたチャネルアクセストークンとチャネルシークレットを、Lambda 環境変数として登録しておく

```python
LINE_CHANNEL_SECRET：<チャネルシークレット>
LINE_CHANNEL_ACCESS_TOKEN：<チャネルアクセストークン>
```

### 3. API Gateway 設定

- 上記参考サイトをもとに API Gateway を作成し、作成した Lambda 関数と関連づける
- デプロイしたステージの URL を控える

### 4. LINE Webhook/Bot設定

- API Gateway 設定にて控えた URL を、LINE チャネル設定の Webhook URL に設定する
- Bot 情報の QR コードから Bot を友達追加
- 追加した Bot が存在するトークで誰かが発言すれば、応答を返してくれる

## 今後の方針

こんなことをやっていきたい。

- DynamoDB を利用した、各トークルームのパラメータ保持
- StepFunctions による状態遷移の実装
- 簡単な便利機能・お遊び機能などの追加
  - じゃんけん
  - しりとり ※奥が深そう
    - 読み仮名判別、使用済み単語チェック、存在しない単語チェック、回答時間制限モード
    - 多人数参加型、参加者の発言順序有効/無効、一対多モード(Bot vs ルームメンバ全員)
  - 幹事代行
  - 目隠し将棋
- Bot プロフィールの設定練りこみ・キャラ付け
  - 面白くしたい
  - 愛され Bot を目指したい
