import chainlit as cl

import json
import requests
import re

SENTENCE_SPLITTERS = ["。", "！", "？"]


def split_sentences(sentences, separator):
    separators = "".join(separator)
    pattern = rf"(?<=[{separators}])"
    return re.split(pattern, sentences)


def clean_text(text):
    text = text.replace(" *", "")
    text = text.replace("* ", "")
    text = text.replace("*", "")
    return text


async def create_response_message(text):
    endpoint = "http://api-gemma2:8000/chat"

    prompt = """あなたは先生です．以下のことに注意して回答してください．
    * 箇条書きを避ける
    * 丁寧な言葉遣いを心がける
    * 自然な会話文で回答する
    * 特殊文字の使用を避ける
    質問: """
    prompt += text

    message_json = {"message": prompt}
    res = requests.post(endpoint, json=message_json, stream=True)

    current_chunk = ""
    for chunk in res.iter_content(chunk_size=50, decode_unicode=True):
        if chunk:
            current_chunk += chunk
            if any(
                splitter in current_chunk for splitter in SENTENCE_SPLITTERS
            ):
                splitted_sentences = split_sentences(
                    current_chunk, separator=SENTENCE_SPLITTERS
                )
                sentences = splitted_sentences[:-1]
                current_chunk = splitted_sentences[-1]
                for sentence in sentences:
                    yield clean_text(sentence)


def create_voice_wav(text):
    endpoint = "http://api-aivisspeech:10101"

    # get style id
    endpoint_speakers = endpoint + "/speakers"
    res = requests.get(endpoint_speakers)
    speakers = json.loads(res.content)
    style_id = speakers[0]["styles"][3]["id"]

    # get audio query
    endpoint_audioquery = endpoint + "/audio_query"
    params = {"speaker": style_id, "text": text}
    res = requests.post(endpoint_audioquery, params=params)
    audioquery_json = json.loads(res.content)

    # create audio data
    endpoint_synthesis = endpoint + "/synthesis"
    params = {"speaker": style_id}
    res = requests.post(
        endpoint_synthesis, params=params, json=audioquery_json
    )

    return res.content


def create_response_elemeents(text, auto_play=True):
    audio = create_voice_wav(text)
    elements = [
        cl.Audio(
            content=audio,
            display="inline",
            auto_play=auto_play,
        )
    ]
    return elements


@cl.on_chat_start
async def on_chat_start():
    start_message = "こんにちは！ご質問をどうぞ．"
    cl.user_session.set("message_history", [{"回答": start_message}])

    elements = create_response_elemeents(start_message, auto_play=False)
    await cl.Message(content=start_message, elements=elements).send()


@cl.on_message
async def main(message: cl.Message):
    # add current message to message hisotry
    message_history = cl.user_session.get("message_history")
    message_history.append({"質問": message.content})

    # show response on browser
    async for response_message in create_response_message(message.content):
        elements = create_response_elemeents(response_message)
        await cl.Message(
            content=f"Received: {response_message}",
            elements=elements,
        ).send()

    # add response message to message hisotry
    message_history.append({"回答": response_message})
    cl.user_session.set("message_history", message_history)
