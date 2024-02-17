"""
This code defines a base class `NetMsg` and a decorator `networkmessage` for creating network message classes.
The `NetMsg` class provides methods for serializing and deserializing network messages using the MessagePack format.
The `networkmessage` decorator is used to create subclasses of `NetMsg` with added data fields and automatically register them in a message registry.

The `NetMsg` class has the following attributes and methods:
- `__type__`: an integer representing the message type, automatically assigned based on the order of subclass registration
- `__registry__`: a dictionary mapping message types to their corresponding subclass types
- `to_bytes()`: serializes the message object into a bytes object using MessagePack format
- `from_bytes(bytes_: bytes)`: deserializes a bytes object into a message object using MessagePack format
- `__bytes__()`: returns the serialized bytes object of the message object

The `networkmessage` decorator takes a class as input and performs the following steps:
- Decorates the class with the `dataclass` decorator to automatically generate boilerplate code for data classes
- Creates a new subclass of `NetMsg` and the input class, with the input class as the base class
- Returns the new subclass

The `unpack_msg` function is a helper function that deserializes a bytes object into a message object using the `from_bytes` method of `NetMsg`.

"""

from dataclasses import dataclass
from typing import Any, Type

import ormsgpack


class NetMsg:
    """
    Represents a network message.

    Attributes:
        __type__ (int): The type of the network message.
        __registry__ (dict[int, Type]): A dictionary that maps message types to their corresponding classes.

    Methods:
        to_bytes(): Converts the network message to bytes.
        from_bytes(bytes_: bytes): Converts bytes to a network message.
        __bytes__(): Converts the network message to bytes.
    """

    __type__: int
    __registry__: dict[int, Type] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__type__ = len(cls.__registry__)
        cls.__registry__[cls.__type__] = cls

    def to_bytes(self) -> bytes:
        return ormsgpack.packb([self.__type__, *list(vars(self).values())])

    @staticmethod
    def from_bytes(bytes_: bytes) -> Any:
        message_type, *values = ormsgpack.unpackb(bytes_)
        assert (
            message_type in NetMsg.__registry__
        ), f"Unknown message type: {message_type}"
        return NetMsg.__registry__[message_type](*values)

    def __bytes__(self) -> bytes:
        return self.to_bytes()


def networkmessage(cls: Type) -> Type:
    """
    This function takes a class as an argument, converts it into a dataclass, and then
    creates a new type that inherits from both the input class and the NetMsg class.
    The new type has the same name as the input class. It returns the new type.

    Parameters:
    cls (Type): The input class that will be converted to a dataclass and from which
                the new type will inherit.
    Returns:
    Type: The new type that inherits from both the input class and the NetMsg class.
    """
    # Convert the input class to a dataclass
    cls = dataclass(cls)

    # Create a new type that inherits from both the input class and the NetMsg class
    cls = type(cls.__name__, (NetMsg, cls), {})

    return cls


def unpack_msg(msg: bytes) -> Any:
    """
    Unpacks a network message from bytes.

    Args:
        msg (bytes): The message to unpack.

    Returns:
        Any: The unpacked network message.
    """
    return NetMsg.from_bytes(msg)
