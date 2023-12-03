from slurm.text_translator import GoogleTranslator
from slurm.types import Language
from tests import ScopedAsync

import pytest
import pytest_asyncio

import asyncio
import random
from typing import List, Self


@pytest.fixture(scope="module")
def event_loop():
    """ Stop pytest from complaining about fixture with class scope. """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


class TestTextTranslator:

    @pytest_asyncio.fixture(scope="class")
    async def google_translator(self: Self) -> ScopedAsync:
        """ Share the same instance of GoogleTranslator across all tests. """
        return await ScopedAsync(GoogleTranslator).create()

    async def google_translate_through_all_languages(self: Self, languages: List[Language], google_translator: ScopedAsync):
        sentence = "The quick brown fox jumps over the lazy dog"
        source_language = Language.ENGLISH
        for target_language in languages:
            sentence = await google_translator.translate(sentence, source_language, target_language)
            source_language = target_language
        sentence = await google_translator.translate(sentence, source_language, Language.ENGLISH)

    @pytest.mark.asyncio
    async def test_google_translate_through_all_languages_in_order(self: Self, google_translator: ScopedAsync) -> None:
        await self.google_translate_through_all_languages(list(Language), google_translator)

    @pytest.mark.asyncio
    async def test_google_translate_through_all_languages_in_reverse_order(self: Self, google_translator: ScopedAsync) -> None:
        languages = list(Language)
        languages.reverse()
        await self.google_translate_through_all_languages(languages, google_translator)

    @pytest.mark.asyncio
    async def test_google_translate_through_all_languages_in_random_order(self: Self, google_translator: ScopedAsync) -> None:
        languages = list(Language)
        random.shuffle(languages)
        await self.google_translate_through_all_languages(languages, google_translator)