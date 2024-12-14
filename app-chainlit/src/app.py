import chainlit as cl

import json
import requests


def create_response_message(text):
    response_message = text
    return response_message


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
            name=text,
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
    # get message hisotry from user_session
    message_history = cl.user_session.get("message_history")
    message_history.append({"質問": message.content})

    # show response on browser
    response_message = create_response_message(message.content)
    elements = create_response_elemeents(response_message)
    await cl.Message(
        content=f"Received: {response_message}",
        elements=elements,
    ).send()

    # save message history
    message_history.append({"回答": response_message})
    cl.user_session.set("message_history", message_history)

    # show logs on console
    print(message_history)
