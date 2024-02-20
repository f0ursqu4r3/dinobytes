import unittest
from dataclasses import dataclass

from dinobytes import dbyte, unpackd


@dbyte
@dataclass
class Message:
    name: str
    value: int


@dbyte
@dataclass
class Container:
    message: Message


@dbyte
@dataclass
class NestedContainer:
    container: Container


class TestDinoBytes(unittest.TestCase):
    def test_serialization_deserialization(self):
        # Test serialization and deserialization of a NetMsg subclass
        msg = Message(name="Test", value=123)
        serialized_msg = msg.to_bytes()
        deserialized_msg = Message.from_bytes(serialized_msg)

        self.assertEqual(msg.name, deserialized_msg.name)
        self.assertEqual(msg.value, deserialized_msg.value)

    def test_registry(self):
        # Ensure the message type is registered
        self.assertIn(Message.__dtype__, Message.__dreg__)
        self.assertEqual(Message, Message.__dreg__[Message.__dtype__])

    def test_unpackd(self):
        # Test unpacking a message from bytes
        msg = Message(name="Unpack", value=456)
        serialized_msg = msg.to_bytes()
        unpacked_msg = unpackd(serialized_msg)

        self.assertIsInstance(unpacked_msg, Message)
        self.assertEqual(msg.name, unpacked_msg.name)
        self.assertEqual(msg.value, unpacked_msg.value)

    def test_nested(self):
        # Test serialization and deserialization of a nested message
        msg = Message(name="Nested", value=789)
        container = Container(message=msg)
        serialized_container = container.to_bytes()
        deserialized_container = Container.from_bytes(serialized_container)

        self.assertIsInstance(deserialized_container.message, Message)
        self.assertEqual(msg.name, deserialized_container.message.name)
        self.assertEqual(msg.value, deserialized_container.message.value)

    def test_multilevel_nested(self):
        # Test serialization and deserialization of a multilevel nested message
        msg = Message(name="Multilevel", value=101112)
        container = Container(message=msg)
        nested_container = NestedContainer(container=container)
        serialized_nested_container = nested_container.to_bytes()
        deserialized_nested_container = NestedContainer.from_bytes(
            serialized_nested_container
        )

        self.assertIsInstance(deserialized_nested_container.container.message, Message)
        self.assertEqual(msg.name, deserialized_nested_container.container.message.name)
        self.assertEqual(
            msg.value, deserialized_nested_container.container.message.value
        )


if __name__ == "__main__":
    unittest.main()
