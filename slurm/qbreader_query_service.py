from qbreader import Async as qbr
from qbreader import Sync
import qbreader
from slurm.types import Difficulty, Tossup

import aiohttp
from collections import defaultdict
from typing import Dict, List, Self, Type


class QBReaderQueryService:
    """ 
    Service to retrieve tossups from the specified set and packet. 
    This class must be instantiated using the create() method in an async environment.
    """

    @classmethod
    async def create(cls: Type[Self], session: aiohttp.ClientSession):
        self = cls()
        self.client = await qbr.create(session)
        self.sync_client = Sync()
        self.session = session
        return self

    async def packet_tossups(self: Self, set_name: str, packet_number: int) -> List[Tossup]:
        """ Retrieves the list of tossups from the given set and packet. """
        def qbreader_tossup_to_our_tossup(qbr_tossup: qbreader.Tossup) -> Tossup:
            return Tossup(
                question=qbr_tossup.question,
                formatted_answer=qbr_tossup.formatted_answer,
                answer=qbr_tossup.answer,
                category=qbr_tossup.category,
                subcategory=qbr_tossup.subcategory
            )
        return list(map(qbreader_tossup_to_our_tossup, await self.client.packet_tossups(set_name, packet_number)))

    async def num_packets(self: Self, set_name: str) -> int:
        """ Retrieves the number of packets in the set. """
        return await self.client.num_packets(set_name)

    async def set_list(self: Self) -> List[str]:
        """ Retrieves a list of all question sets in the QBReader database. """
        return await self.client.set_list()

    async def set_lists_by_difficulty(self: Self) -> Dict[Difficulty, List[str]]:
        """
        Retrieves all question sets in the QBReader database, organised by difficulty.
        This method will take a while to execute.
        """
        set_list = await self.set_list()
        by_difficulty = defaultdict(list)
        for set_name in set_list:
            by_difficulty[await self.get_difficulty(set_name)].append(set_name)
        return by_difficulty

    async def get_difficulty(self: Self, set_name: str) -> Difficulty:
        """ Retrieves the difficulty of the given question set. """
        try:
            response = await self.client.query(questionType="tossup", setName=set_name, maxReturnLength=1)
            return list(Difficulty)[int(response.tossups[0].difficulty.value) - 1]
        except Exception:
            return Difficulty.UNRATED