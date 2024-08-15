from typing import Callable, Any, Optional

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Bytecode(ABC):
    """
    Base absract class for byte-convertible classes
    """
    @abstractmethod
    def to_bytes(self):
        pass

    @staticmethod
    @abstractmethod
    def byte_length() -> int:
        pass


@dataclass
class InstructionsLUTEntry:
    command_code: int
    func: Callable[
        [int, Optional[Any], Optional[Any], Optional[Any]],
        int
    ]

    def get_bytes(
            self,
            operand1: Optional[Any],
            operand2: Optional[Any],
            operand3: Optional[Any]
    ) -> bytes:
        return self.func(
            self.command_code,
            operand1,
            operand2,
            operand3
        ).to_bytes(2, "big", signed=False)

