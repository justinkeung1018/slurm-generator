from slurm.file_writer import MicrosoftWordWriter
from slurm.qbreader_query_service import QBReaderQueryService
from slurm.text_translator import GoogleTranslator
from slurm.tossup_translator import TossupTranslator
from slurm.types import Difficulty, Language, Tossup

import aioconsole
import aiohttp
import asyncio
import pathlib
import time
from typing import List


async def main():
    DEFAULT_OUTPUT_DIR = "./output"

    async with aiohttp.ClientSession() as session:
        query_service = await QBReaderQueryService.create(session)

        ##################################################
        ##########      USER PROMPTS BEGIN      ##########
        ##################################################

        retrieve_set_list = (await aioconsole.ainput("Do you want a list of all question sets? [y/n] ") == "y")
        if retrieve_set_list:
            organised_by_difficulty = (await aioconsole.ainput("Do you want the list to be organised by difficulty? [y/n] (WARNING: it will take a while): ") == "y")

            SPACES = "   "
            LINE_LENGTH = 41

            await aioconsole.aprint("-" * LINE_LENGTH)
            await aioconsole.aprint((SPACES + "Set list begins" + SPACES).center(LINE_LENGTH, "-"))
            await aioconsole.aprint("-" * LINE_LENGTH)

            if organised_by_difficulty:
                set_list = await query_service.set_lists_by_difficulty()
                for difficulty in list(Difficulty):
                    await aioconsole.aprint("#" * LINE_LENGTH)
                    await aioconsole.aprint((SPACES + difficulty + SPACES).center(LINE_LENGTH, "#"))
                    await aioconsole.aprint("#" * LINE_LENGTH)
                    await aioconsole.aprint("")
                    if set_list[difficulty]:
                        await aioconsole.aprint("\n".join(set_list[difficulty]))
                    else:
                        await aioconsole.aprint("(No packets are in this difficulty.)")
                    await aioconsole.aprint("")
            else:
                set_list = await query_service.set_list()
                await aioconsole.aprint("\n".join(set_list))

            await aioconsole.aprint("-" * LINE_LENGTH)
            await aioconsole.aprint((SPACES + "Set list ends" + SPACES).center(LINE_LENGTH, "-"))
            await aioconsole.aprint("-" * LINE_LENGTH)

        retrieved_num_packets = False
        while not retrieved_num_packets:
            set_name = await aioconsole.ainput("Which question set do you want the SLURM tossups from? ")
            try:
                num_packets = await query_service.num_packets(set_name)
                retrieved_num_packets = True
            except ValueError:
                await aioconsole.aprint("ERROR: Invalid set name. ", end="")

        retrieved_packet_number = False
        translate_entire_set = False
        while not retrieved_packet_number:
            try:
                packet_number = await aioconsole.ainput(f"{set_name} has {num_packets} packets. Which packet number do you want? [enter 'all' for all packets] ")
                translate_entire_set = (packet_number.lower() == "all")
                if translate_entire_set:
                    break
                packet_number = int(packet_number)
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

        """ Create the output directory and any parents if they do not exist. """
        output_dir = await aioconsole.ainput(f"Specify the output directory [defaults to {DEFAULT_OUTPUT_DIR}]: ") or DEFAULT_OUTPUT_DIR
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

        if translate_entire_set:
            slurm_set_name = await aioconsole.ainput("Give your SLURM set a name [skip for default]: ") or f"SLURM_{set_name}"
        else:
            slurm_packet_name = await aioconsole.ainput("Give your SLURM packet a name [skip for default]: ") or f"SLURM_{set_name}_Packet {packet_number}"

        ##################################################
        ###########      USER PROMPTS END      ###########
        ##################################################

        translator = TossupTranslator(GoogleTranslator(session))
        writer = MicrosoftWordWriter()


        async def generate_packet(
            packet_name: str,
            tossups: List[Tossup],
        ) -> int:
            start_time = time.time()
            translated_tossups = [await translator.translate_tossup(tossup, num_translations, Language.ENGLISH, Language.ENGLISH) for tossup in tossups]
            writer.write_tossups(packet_name, translated_tossups, output_dir + "/" + packet_name)
            end_time = time.time()
            await aioconsole.aprint(f"SLURM packet generation complete. Time taken: {end_time - start_time} seconds.")
            return end_time


        if translate_entire_set:
            set_start_time = time.time()
            for packet_number in range(1, num_packets + 1):
                await aioconsole.aprint(f"Generating SLURM packet {packet_number} out of {num_packets}...")
                tossups = await query_service.packet_tossups(set_name, packet_number)
                set_end_time = await generate_packet(f"{slurm_set_name}_Packet {packet_number}", tossups)
            await aioconsole.aprint(f"{num_packets} SLURM packets generation complete. Total time taken: {set_end_time - set_start_time} seconds.")
        else:
            await aioconsole.aprint(f"Generating SLURM packet...")
            await generate_packet(slurm_packet_name, tossups)


if __name__ == "__main__":
    asyncio.run(main())