from __future__ import annotations

import contextlib
from typing import Any, Type

import ormsgpack


class DinoClass:
    """
    Base class for dinosaur objects.
    """

    __dtype__: int
    __dreg__: dict[int, Type] = {}

    def __init_subclass__(cls, **kwargs):
        """
        Method called when a subclass of DinoClass is defined.
        It updates the __dtype__ attribute of the subclass and adds it to the __dreg__.
        """
        super().__init_subclass__(**kwargs)
        cls.__dtype__ = len(cls.__dreg__)
        cls.__dreg__[cls.__dtype__] = cls

    def to_bytes(self) -> bytes:
        """
        Convert the DinoClass object to bytes using ormsgpack serialization.
        """
        return ormsgpack.packb(
            [
                self.__dtype__,
                *[
                    self._value_to_bytes(v)
                    for k, v in vars(self).items()
                    if not k.startswith("__")
                ],
            ],
            default=bytes,
        )

    @staticmethod
    def _value_to_bytes(value) -> Any:
        """
        Convert a value to bytes if it is an instance of DinoClass, otherwise return the value as is.
        """
        return value.to_bytes() if isinstance(value, DinoClass) else value

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> Any:
        """
        Convert bytes to a DinoClass object using ormsgpack deserialization.
        """
        message_type, *values = ormsgpack.unpackb(bytes_)
        assert message_type in cls.__dreg__, f"Unknown message type: {message_type}"
        values = [cls._value_from_bytes(value) for value in values]
        return cls.__dreg__[message_type](*values)

    @staticmethod
    def _value_from_bytes(value) -> Any:
        """
        Convert a value from bytes to a DinoClass object if possible, otherwise return the value as is.
        """
        match value:
            case list() | set() | tuple():
                return [DinoClass._value_from_bytes(v) for v in value]
            case dict():
                return {k: DinoClass._value_from_bytes(v) for k, v in value.items()}
            case bytes():
                with contextlib.suppress(AssertionError, ValueError):
                    return DinoClass.from_bytes(value)
            case _:
                return value

    def __bytes__(self) -> bytes:
        """
        Convert the DinoClass object to bytes using ormsgpack serialization.
        """
        return self.to_bytes()


def dbyte(cls: Type) -> Type:
    """
    Decorator function that adds DinoClass as a base class to the given class.
    """
    cls = type(cls.__name__, (DinoClass, cls), {})
    return cls


def unpackd(msg: bytes) -> Any:
    """
    Convert bytes to a DinoClass object using ormsgpack deserialization.
    """
    return DinoClass.from_bytes(msg)
