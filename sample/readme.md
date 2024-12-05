# Gemma 2 × AivisSpeech サンプルコード

ローカル CPU 環境で実行可能なボイスチャットボットアプリを開発すべく，Google が開発した言語モデル [Gemma 2](https://huggingface.co/google/gemma-2-2b-jpn-it) と高品質な音声合成エンジン [AivisSpeech-Engine](https://github.com/Aivis-Project/AivisSpeech-Engine) を組み合わせて対話するためのシステムを構築しました．

## セットアップと実行手順

### 1. Docker 環境の構築

```bash
docker compose up --build -d
```

このコマンドで、Gemma 2 と AivisSpeech を含む全サービスが構築されバックグラウンドで起動します。

### 2. Notebook での実行

Docker 環境の構築後、提供されている `sample.ipynb` を開いて実行することで Gemma 2 と AivisSpeech を連携した対話システムの動作を確認できます。

## 実行例
