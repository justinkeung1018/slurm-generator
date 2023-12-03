from slurm.qbreader_query_service import QBReaderQueryService
from tests import async_assert_exception, ScopedAsync

import pytest
import pytest_asyncio

import asyncio
from typing import Self


@pytest.fixture(scope="module")
def event_loop():
    """ Stop pytest from complaining about fixture with class scope. """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

SAMPLE_PACKET_NAME = "2021 ACF Winter"

class TestQBReaderQueryService:

    @pytest_asyncio.fixture(scope="class")
    async def service(self: Self) -> ScopedAsync:
        """ Share the same instance of QBReaderQueryService across all tests. """
        return await ScopedAsync(QBReaderQueryService).create()
    
    @pytest.mark.asyncio
    async def test_valid_set_name(self: Self, service: ScopedAsync) -> None:
        await service.num_packets(SAMPLE_PACKET_NAME)

    @pytest.mark.asyncio
    async def test_invalid_set_name_throws_valueerror(self: Self, service: ScopedAsync) -> None:
        await async_assert_exception(service.num_packets, ValueError, "Invalid set name")
    
    @pytest.mark.asyncio
    async def test_packet_number_out_of_bounds(self: Self, service: ScopedAsync) -> None:
        num_packets = await service.num_packets(SAMPLE_PACKET_NAME)
        await async_assert_exception(service.packet_tossups, ValueError, SAMPLE_PACKET_NAME, 0)
        await async_assert_exception(service.packet_tossups, ValueError, SAMPLE_PACKET_NAME, num_packets + 1)