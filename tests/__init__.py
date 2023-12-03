import pytest

import aiohttp
from typing import Any, Callable, Type, Self


async def async_assert_exception(func: Callable, exception: Type[Exception], *args, **kwargs):
    """ Asserts that the given async function, when called with the given arguments, raises the specified exception. """
    with pytest.raises(exception):
        await func(*args, **kwargs)


class ScopedAsync:
    """ Wrapper around async types that manages its own aiohttp.ClientSession instance. """

    def __init__(self: Self, async_type: Type):
        self.session = self.async_instance = None
        self.async_type = async_type
    
    async def create(self: Self) -> Self:
        """
        Instantiates ScopedAsync by creating a new aiohttp.ClientSession and calling the appropriate
        methods/constructors of the underlying type. Note that this is an instance method, but not
        a class method.
        """
        self.session = aiohttp.ClientSession()
        if hasattr(self.async_type, "create") and callable(self.async_type.create):
            self.async_instance = await self.async_type.create(self.session)
        else:
            self.async_instance = self.async_type(self.session)
        return self
    
    def __getattr__(self: Self, attr):
        """ Use a wrapped instance like the instance itself. """
        return getattr(self.async_instance, attr)

    async def __aenter__(self: Self) -> Self:
        """ Enter async context. """
        return self
    
    async def __aexit__(self: Self, exc_type, exc_val, exc_tb) -> None:
        """ Exit async context. """
        await self.session.close()