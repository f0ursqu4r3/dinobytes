from typing import Any, Type
import ormsgpack


class DinoClass:
    """
    Base class for dinosaur objects.
    """

    __dinotype__: int
    __dinoregistry__: dict[int, Type] = {}

    def __init_subclass__(cls, **kwargs):
        """
        Method called when a subclass of DinoClass is defined.
        It updates the __dinotype__ attribute of the subclass and adds it to the __dinoregistry__.
        """
        super().__init_subclass__(**kwargs)
        cls.__dinotype__ = len(cls.__dinoregistry__)
        cls.__dinoregistry__[cls.__dinotype__] = cls

    def to_bytes(self) -> bytes:
        """
        Convert the DinoClass object to bytes using ormsgpack serialization.
        """
        return ormsgpack.packb(
            [
                self.__dinotype__,
                *[self._value_to_bytes(value) for value in vars(self).values()],
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
        assert (
            message_type in cls.__dinoregistry__
        ), f"Unknown message type: {message_type}"
        values = [cls._value_from_bytes(value) for value in values]
        return cls.__dinoregistry__[message_type](*values)

    @staticmethod
    def _value_from_bytes(value) -> Any:
        """
        Convert a value from bytes to a DinoClass object if possible, otherwise return the value as is.
        """
        if not isinstance(value, bytes):
            return value
        try:
            return DinoClass.from_bytes(value)
        except (AssertionError, ValueError):
            return value

    def __bytes__(self) -> bytes:
        """
        Convert the DinoClass object to bytes using ormsgpack serialization.
        """
        return self.to_bytes()


def cerealbox(cls: Type) -> Type:
    """
    Decorator function that adds DinoClass as a base class to the given class.
    """
    cls = type(cls.__name__, (DinoClass, cls), {})
    return cls


def consume(msg: bytes) -> Any:
    """
    Convert bytes to a DinoClass object using ormsgpack deserialization.
    """
    return DinoClass.from_bytes(msg)
