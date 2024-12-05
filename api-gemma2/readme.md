# Gemma 2 API Server
[Gemma 2 JPN モデル](https://huggingface.co/google/gemma-2-2b-jpn-it) を利用する API サーバーを作成するための Dockerfile が含まれています。

## 前提条件
APIサーバーを構築する前に、以下の手順を完了してください：
1. [Hugging Face モデルページ](https://huggingface.co/google/gemma-2-2b-jpn-it)で Gemma 2 モデルの利用規約に同意してください。
2. [設定ページ](https://huggingface.co/settings/tokens)で Hugging Face トークンを生成してください。
3. トークンの権限を編集し、「リポジトリ」セクションで Gemma 2 JPN モデルへのアクセス権を付与してください。
4. `/api-gemma2/.env.secret` というファイルを作成し、以下の形式で Hugging Face アクセス・トークンを追加してください：
    ```text
    HF_TOKEN="hf_your_access_token"
    ```
    `hf_your_access_token` を生成した Hugging Face トークンに置き換えてください。

## コンテナのビルドと実行
APIサーバーコンテナをビルドして実行するには、以下の手順に従ってください：
1. Dockerイメージをビルドします：
```sh
docker build -t api-gemma2 .
```
2. コンテナを実行します：
```sh
docker run -d -p 8000:8000 -v $PWD/src:/app/src api-gemma2
```

注意：ビルドプロセスには、Gemma 2 モデルのダウンロードや Python 環境のセットアップが含まれるため、10～20分以上かかる場合があります。所要時間は通信速度やシステム性能によって異なります。

## 使用方法
コンテナ起動中 APIサーバーに以下のURLでアクセスできます：
- http://localhost:8000.

自動生成されたAPIドキュメントは以下から確認できます：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

