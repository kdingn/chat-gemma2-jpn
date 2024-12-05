# AivisSpeech API Server

[Aivis Project](https://aivis-project.com/) でのプロダクトである [AivisSpeech-Engine](https://github.com/Aivis-Project/AivisSpeech-Engine) を起動するための Dockerfile が含まれています．ライセンスや利用方法は公式レポジトリをご参照ください．

## GPU 利用

### dockerfile の編集
`dockerfile` 内を以下のように書き換えてください．
```sh
FROM ghcr.io/aivis-project/aivisspeech-engine:nvidia-latest
ENTRYPOINT [ "/entrypoint.sh"  ]
CMD [ "gosu", "user", "/opt/python/bin/poetry", "run", "python", "./run.py", "--host", "0.0.0.0" ]
```

### compose.yaml の編集
レポジトリルートの `compose.yaml` のコメントアウトを外してください．
```sh
deploy:
    resources:
    reservations:
        devices:
        - driver: nvidia
            count: 1
            capabilities: [gpu]
```

