from qbreader import Async as qbr
import qbreader
from slurm.types import Tossup

import aiohttp
from typing import List, Self, Type


class QBReaderQueryService:
    """ 
    Service to retrieve tossups from the specified set and packet. 
    This class must be instantiated using the create() method in an async environment.
    """

    @classmethod
    async def create(cls: Type[Self], client: aiohttp.ClientSession):
        self = cls()
        self.client = await qbr.create(client)
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