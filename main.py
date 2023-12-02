from text_translator import GoogleTranslator
from file_writer import MicrosoftWordWriter
from qbreader_query_service import QBReaderQueryService
from tossup_translator import TossupTranslator
from typedefs import Language

import aioconsole
import aiohttp
import asyncio

async def main():
    source_set_name = await aioconsole.ainput("Which question set do you want the SLURM tossups from? ")
    source_packet_number = int(await aioconsole.ainput("Which packet number do you want? "))

    async with aiohttp.ClientSession() as session:
        query_service = await QBReaderQueryService.create(session)
        tossups = await query_service.packet_tossups(source_set_name, source_packet_number)

        translator = TossupTranslator(GoogleTranslator(session))
        num_translations = int(await aioconsole.ainput("How many times do you want the tossups to be translated? "))
        packet_name = await aioconsole.ainput("Give your SLURM packet a name: ")

        translated_tossups = []
        for tossup in tossups:
            translated_tossup = await translator.translate_tossup(tossup, num_translations, Language.ENGLISH, Language.ENGLISH)
            translated_tossups.append(translated_tossup)
    
    writer = MicrosoftWordWriter()
    writer.write_tossups(packet_name, translated_tossups, packet_name)

asyncio.run(main())