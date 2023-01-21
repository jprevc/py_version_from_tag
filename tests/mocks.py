from dataclasses import dataclass
from typing import Callable


@dataclass
class MockCliReturn:
    stdout: bytes


def create_mock_subprocess_return_object(return_bytes: bytes) -> Callable:
    def mock_subprocess_run(*args, **kwargs) -> MockCliReturn:  # pylint: disable=unused-argument
        ret_val = MockCliReturn(return_bytes)
        return ret_val

    return mock_subprocess_run
