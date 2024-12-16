import re
import requests

import aiohttp
import chainlit as cl
import emoji

ENDPOINT_AIVISSPEECH = "http://api-aivisspeech:10101"
ENDPOINT_LLM = "http://api-gemma2:8000/chat"
SENTENCE_SPLITTERS = ["。", "！", "？"]
PROMPT_TEMPLATE = """あなたは先生です。以下のことに注意して回答してください。
* 自然な会話文で回答する。
* 丁寧な言葉遣いで回答する。
* 箇条書きを避ける。
* 特殊文字の使用を避ける。
"""
START_MESSAGE = "こんにちは、なにかご用でしょうか。"
ROLE_USER = "質問"
ROLE_RESPONSE = "回答"


def create_prompt(current_message, message_history=[]):
    prompt = PROMPT_TEMPLATE
    for message in message_history:
        prompt += list(message.keys())[0] + ": " + list(message.values())[0] + "\n"
    prompt += ROLE_USER + ": " + current_message + "\n" + ROLE_RESPONSE + ": "
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


async def create_voice_wav(text):
    endpoint = ENDPOINT_AIVISSPEECH

    async with aiohttp.ClientSession() as session:
        # get style id
        endpoint_speakers = endpoint + "/speakers"
        async with session.get(endpoint_speakers) as res:
            speakers = await res.json()
            style_id = speakers[0]["styles"][3]["id"]

        # get audio query
        endpoint_audioquery = endpoint + "/audio_query"
        params = {"speaker": style_id, "text": text}
        async with session.post(endpoint_audioquery, params=params) as res:
            audioquery_json = await res.json()

        # create audio data
        endpoint_synthesis = endpoint + "/synthesis"
        params = {"speaker": style_id}
        async with session.post(
            endpoint_synthesis, params=params, json=audioquery_json
        ) as res:
            audio_data = await res.read()

    return audio_data


async def create_audio_element(text, auto_play=False, show_name=True):
    name = ""
    if show_name:
        if len(text) > 10:
            name = text[:10] + "..."
        else:
            name = text
    audio = await create_voice_wav(text)
    element = cl.Audio(name=name, content=audio, display="inline", auto_play=auto_play)
    return element


async def stream_request_response_message(text):
    endpoint = ENDPOINT_LLM

    message_history = cl.user_session.get("message_history")
    prompt = create_prompt(text, message_history=message_history)
    message_json = {"message": prompt}
    res = requests.post(endpoint, json=message_json, stream=True)

    for chunk in res.iter_content(chunk_size=50, decode_unicode=True):
        if chunk:
            yield clean_text(chunk)


async def show_response_message(text):
    message = cl.Message(content="")
    current_chunk = ""
    response_message = ""

    # stream request
    async for chunk in stream_request_response_message(text):
        if chunk:
            await message.stream_token(chunk)
            current_chunk += chunk
            response_message += chunk
            if any(splitter in current_chunk for splitter in SENTENCE_SPLITTERS):
                splitted_sentences = split_sentences(
                    current_chunk, separator=SENTENCE_SPLITTERS
                )
                sentences = splitted_sentences[:-1]
                current_chunk = splitted_sentences[-1]
                for sentence in sentences:
                    element = await create_audio_element(sentence)
                    message.elements.append(element)
                    await message.update()
    await message.update()

    return response_message


@cl.on_chat_start
async def on_chat_start():
    start_message = START_MESSAGE

    cl.user_session.set("message_history", [])

    element = await create_audio_element(start_message, show_name=False)
    await cl.Message(content=start_message, elements=[element]).send()


@cl.on_message
async def main(input_message):
    response_message = await show_response_message(input_message.content)

    message_history = cl.user_session.get("message_history")
    message_history.append({ROLE_USER: input_message.content})
    message_history.append({ROLE_RESPONSE: response_message})
    cl.user_session.set("message_history", message_history)
