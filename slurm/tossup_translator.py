from slurm.text_translator import TextTranslator
from slurm.types import Language, Tossup

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
        if num_intermediate_translations < 0:
            return tossup
        for _ in range(num_intermediate_translations):
            next_language = random.choice(list(Language))
            tossup.question = await self.translator.translate(tossup.question, source_language, next_language)
            source_language = next_language
        tossup.question = await self.translator.translate(tossup.question, source_language, target_language)
        return tossup