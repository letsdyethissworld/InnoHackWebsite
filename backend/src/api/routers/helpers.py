from src.bootstrap import Bootstrap


async def get_uow():
    """Get a unit of work for the current request"""
    uow = Bootstrap.bootstrapped().uow_partial()
    async with uow:
        yield uow


async def get_flat_uow():
    """Get a unit of work that could be used manually with `async with`"""
    return Bootstrap.bootstrapped().uow_partial()
