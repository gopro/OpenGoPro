from typing import TypeVar

from returns.future import future_safe, FutureSuccess, FutureFailure, FutureResult
from returns.io import IOSuccess, IOFailure, IO
from returns.result import Success, Failure, Result
import pytest


async def div(first_number: int, second_number: int) -> Result[int, ZeroDivisionError]:  # noqa: FURB118
    try:
        return Result.from_value(first_number // second_number)
    except ZeroDivisionError as e:
        return Result.from_failure(e)


@future_safe(exceptions=(ZeroDivisionError,))
async def future_div(first_number: int, second_number: int) -> int:  # noqa: FURB118
    return first_number // second_number


@pytest.mark.asyncio
async def test_future_returns_10():
    match await future_div(20, 2):
        case IOSuccess(Success(10)):
            assert True

        case IOSuccess(Success(value)):
            assert False

        case IOFailure(Failure(ZeroDivisionError())):
            assert False

        case IOFailure(Failure(_)):
            assert False

        case _:
            assert False


@pytest.mark.asyncio
async def test_future_returns_2():
    match await future_div(20, 10):
        case IOSuccess(Success(10)):
            assert False

        case IOSuccess(Success(value)):
            assert value == 2

        case IOFailure(Failure(ZeroDivisionError())):
            assert False

        case IOFailure(Failure(_)):
            assert False

        case _:
            assert False


@pytest.mark.asyncio
async def test_future_divide_by_zero():
    match await future_div(20, 0):
        case IOSuccess(Success(10)):
            assert False

        case IOSuccess(Success(value)):
            assert False

        case IOFailure(Failure(ZeroDivisionError())):
            assert True

        case IOFailure(Failure(_)):
            assert False

        case _:
            assert False


@pytest.mark.asyncio
async def test_returns_10():
    match await div(20, 2):
        case Success(10):
            assert True

        case Success(value):
            assert False

        case Failure(ZeroDivisionError()):
            assert False

        case Failure(_):
            assert False

        case _:
            assert False


@pytest.mark.asyncio
async def test_returns_2():
    match await div(20, 10):
        case Success(10):
            assert False

        case Success(value):
            assert value == 2

        case Failure(ZeroDivisionError()):
            assert False

        case Failure(_):
            assert False

        case _:
            assert False


@pytest.mark.asyncio
async def test_divide_by_zero():
    match await div(20, 0):
        case Success(10):
            assert False

        case Success(value):
            assert False

        case Failure(ZeroDivisionError()):
            assert True

        case Failure(_):
            assert False

        case _:
            assert False
