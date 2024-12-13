import chainlit as cl

import json
import requests


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


@cl.on_message
async def main(message: cl.Message):
    audio = create_voice_wav(message.content)
    elements = [
        cl.Audio(
            name=message.content[:10],
            content=audio,
            display="inline",
            auto_play=True,
        )
    ]

    await cl.Message(
        content=f"Received: {message.content}",
        elements=elements,
    ).send()
