from slurm.file_writer import MicrosoftWordWriter
from slurm.qbreader_query_service import QBReaderQueryService
from slurm.text_translator import GoogleTranslator
from slurm.tossup_translator import TossupTranslator
from slurm.types import Language

import aioconsole
import aiohttp
import asyncio
import time


async def main():
    async with aiohttp.ClientSession() as session:
        query_service = await QBReaderQueryService.create(session)

        ##################################################
        ##########      USER PROMPTS BEGIN      ##########
        ##################################################

        retrieved_num_packets = False
        while not retrieved_num_packets:
            set_name = await aioconsole.ainput("Which question set do you want the SLURM tossups from? ")
            try:
                num_packets = await query_service.num_packets(set_name)
                retrieved_num_packets = True
            except ValueError:
                await aioconsole.aprint("ERROR: Invalid set name. ", end="")

        retrieved_packet_number = False
        while not retrieved_packet_number:
            try:
                packet_number = int(await aioconsole.ainput(f"{set_name} has {num_packets} packets. Which packet number do you want? "))
            except ValueError:
                await aioconsole.aprint("ERROR: Please enter a number. ", end="")
                continue
            try:
                tossups = await query_service.packet_tossups(set_name, packet_number)
                retrieved_packet_number = True
            except ValueError:
                await aioconsole.aprint("ERROR: Packet number out of bounds. ", end="")

        retrieved_num_translations = False
        while not retrieved_num_translations:
            try:
                num_translations = int(await aioconsole.ainput("How many times do you want the tossups to be translated? "))
                retrieved_num_translations = True
            except ValueError:
                await aioconsole.aprint("ERROR: Please enter a number. ", end="")

        packet_name = await aioconsole.ainput("Give your SLURM packet a name: ")

        ##################################################
        ###########      USER PROMPTS END      ###########
        ##################################################

        await aioconsole.aprint("Generating SLURM packet...")
        start_time = time.time()

        translator = TossupTranslator(GoogleTranslator(session))
        translated_tossups = [await translator.translate_tossup(tossup, num_translations, Language.ENGLISH, Language.ENGLISH) for tossup in tossups]
    
    writer = MicrosoftWordWriter()
    writer.write_tossups(packet_name, translated_tossups, packet_name)

    end_time = time.time()
    await aioconsole.aprint(f"SLURM packet generation complete. Time taken: {end_time - start_time}.")


if __name__ == "__main__":
    asyncio.run(main())