from slurm.text_translator import TextTranslator
from slurm.types import Language, Tossup

import copy
import random
from typing import Self


class TossupTranslator:
    def __init__(self: Self, translator: TextTranslator):
        self.translator = translator
    
    """ 
    Translates a tossup from the source language to the target language, going through the
    specified number of intermediate translations.
    """
    async def translate_tossup(
        self: Self,
        tossup: Tossup, 
        num_intermediate_translations: int, 
        source_language: Language, 
        target_language: Language
    ) -> Tossup:
        translated_tossup = copy.deepcopy(tossup)
        if num_intermediate_translations < 0:
            return translated_tossup
        for _ in range(num_intermediate_translations):
            next_language = random.choice(list(Language))
            translated_tossup.question = await self.translator.translate(translated_tossup.question, source_language, next_language)
            source_language = next_language
        translated_tossup.question = await self.translator.translate(translated_tossup.question, source_language, target_language)

        return translated_tossup