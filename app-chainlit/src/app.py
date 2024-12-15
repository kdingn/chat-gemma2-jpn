import chainlit as cl
import emoji

import json
import requests
import re

SENTENCE_SPLITTERS = ["。", "！", "？"]
PROMPT_TEMPLATE = """あなたは先生です。以下のことに注意して回答してください。
* 箇条書きを避ける。
* 丁寧な言葉遣いを心がける。
* 自然な会話文で回答する。
* 特殊文字の使用を避ける。
* 課題がある場合は解決策を提示する。
* 課題がない場合は補足情報を追加する。
"""
ENDPOINT_AIVISSPEECH = "http://api-aivisspeech:10101"
ENDPOINT_LLM = "http://api-gemma2:8000/chat"


def create_prompt(current_message, message_history=[]):
    prompt = PROMPT_TEMPLATE
    for message in message_history:
        prompt += (
            list(message.keys())[0] + ": " + list(message.values())[0] + "\n"
        )
    prompt += "質問: " + current_message + "\n回答: "
    return prompt


def split_sentences(sentences, separator):
    separators = "".join(separator)
    pattern = rf"(?<=[{separators}])"
    return re.split(pattern, sentences)


def clean_text(text):
    text = text.replace(" *", "")
    text = text.replace("* ", "")
    text = text.replace("*", "")
    text = text.replace("「", "")
    text = text.replace("」", "")
    text = emoji.replace_emoji(text)
    return text


async def create_response_message(text):
    endpoint = ENDPOINT_LLM

    message_history = cl.user_session.get("message_history")
    prompt = create_prompt(text, message_history=message_history)
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
                    cleaned_sentence = clean_text(sentence)
                    if len(cleaned_sentence) > 1:
                        yield clean_text(sentence)


def create_voice_wav(text):
    endpoint = ENDPOINT_AIVISSPEECH

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
    start_message = "こんにちは！なにか御用でしょうか．"
    cl.user_session.set("message_history", [{"回答": start_message}])

    elements = create_response_elemeents(start_message, auto_play=False)
    await cl.Message(content=start_message, elements=elements).send()


@cl.on_message
async def main(message: cl.Message):
    # show response on browser
    total_response_message = ""
    async for response_message in create_response_message(message.content):
        elements = create_response_elemeents(response_message, auto_play=False)
        await cl.Message(
            content=response_message,
            elements=elements,
        ).send()
        total_response_message += response_message

    # add messages to message hisotry
    message_history = cl.user_session.get("message_history")
    message_history.append({"質問": message.content})
    message_history.append({"回答": response_message})
    cl.user_session.set("message_history", message_history)
