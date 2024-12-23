# 🗼 Chat Gemma2 JPN

Google が開発した言語モデル [Gemma 2](https://huggingface.co/google/gemma-2-2b-jpn-it) と高品質な音声合成エンジン [AivisSpeech-Engine](https://github.com/Aivis-Project/AivisSpeech-Engine) を組み合わせた音声つきのLLMチャットアプリです。アプリを構成する全てのサービスがローカルのCPU環境で稼働するため、非ネットワーク環境やGPUの利用できない環境でも利用することができます。

<p align="center">
    <img src="https://github.com/user-attachments/assets/901c9f55-e451-4703-84cd-2c7e597f7fc3" alt="network" width="70%"></img>
</p>

## 🎥 デモ

https://github.com/user-attachments/assets/d92a42cc-13f0-4966-82d3-3f258da6c56e

## 🚀 クイックスタート

リポジトリをクローンする
```sh
git clone https://github.com/kdingn/chat-gemma2-jpn.git
```

### Gemma 2 の利用準備

1. [Hugging Face のモデルページ](https://huggingface.co/google/gemma-2-2b-jpn-it)で Gemma 2 モデルの利用規約に同意する
2. [設定ページ](https://huggingface.co/settings/tokens)で Hugging Face トークンを生成する
3. トークンの権限を編集し、「リポジトリ」セクションで Gemma 2 JPN モデルへのアクセス権を付与する
4. `/api-gemma2/.env.secret` というファイルを作成し、以下の形式で Hugging Face アクセストークンを追加する
    ```text
    HF_TOKEN="hf_your_access_token"
    ```
    `hf_your_access_token` を生成した Hugging Face トークンに置き換えてください

### アプリの起動とアクセス
イメージのビルドとコンテナの起動
```sh
docker compose up --build -d
```

ブラウザの http://localhost:8000 からアプリにアクセスする

## ✨ 要素技術

### Gemma 2 JPN

Google より 2024年10月3日 に公開された [google/gemma-2-2b-it](https://huggingface.co/google/gemma-2-2b-jpn-it) を LLM として利用しています。パラメータ数が 20億 と非常に軽量なモデルとなっており CPU 環境でも動作します。また、タスクによっては [GPT-3.5 を上回るパフォーマンス](https://blog.google/intl/ja-jp/company-news/technology/gemma-2-2b/)を発揮することが示されています。

### Aivisspeech

[Aivis Project](https://aivis-project.com/) より 2024年11月19日 にリリースされた [AivisSpeech-Engine](https://github.com/Aivis-Project/AivisSpeech-Engine) を合成音声のエンジンとして利用しています。高品質な音声データを CPU 環境で合成することができ、アプリなどと統合しやすい HTTP API が提供されています。また GUI で直感的に操作することのできるアプリケーションも提供されており、非常に簡単に合成音声を活用することができます。

### Chainlit

2024年1月に正式リリースされた [Chainlit](https://github.com/Chainlit/chainlit) をチャット UI のフレームワークとして利用しています。シンプルな利用であれば非常に簡潔なコードでアプリケーションを作成することができます。また添付ファイルの入力や音声出力など様々な I/O への対応が可能であったり、その他のカスタマイズ性も高くなっています。

