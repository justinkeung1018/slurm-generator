from slurm.types import Language

import aiohttp
from typing import Self
import urllib


class TextTranslator:
    """ Interface for translating text strings. """

    async def translate(self: Self, text: str, source_language: Language, target_language: Language) -> str:
        """ Translates the given text from the source language to the target language. """
        pass


class GoogleTranslator(TextTranslator):
    """ Text translator using Google Translate REST API. """

    def __init__(self: Self, client: aiohttp.ClientSession):
        self.client = client

    async def translate(self: Self, text: str, source_language: Language, target_language: Language) -> str:
        def encode_uri(text: str) -> str:
            return urllib.parse.quote(text, safe='~@#$&()*!+=:;,?/\'');

        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" \
            + source_language \
            + "&tl=" \
            + target_language \
            + "&dt=t&q=" \
            + encode_uri(text)

        async with self.client.get(url) as response:
            response_body = await response.json()
            translated_sentences = list(map(lambda translation: translation[0], response_body[0]))
            return "".join(translated_sentences)