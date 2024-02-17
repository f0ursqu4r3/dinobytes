import unittest
from dinobytes import networkmessage, unpack_msg


@networkmessage
class TestMsg:
    name: str
    value: int


class TestNetMsg(unittest.TestCase):
    def test_serialization_deserialization(self):
        # Test serialization and deserialization of a NetMsg subclass
        msg = TestMsg(name="Test", value=123)
        serialized_msg = msg.to_bytes()
        deserialized_msg = TestMsg.from_bytes(serialized_msg)

        self.assertEqual(msg.name, deserialized_msg.name)
        self.assertEqual(msg.value, deserialized_msg.value)

    def test_registry(self):
        # Ensure the message type is registered
        self.assertIn(TestMsg.__type__, TestMsg.__registry__)
        self.assertEqual(TestMsg, TestMsg.__registry__[TestMsg.__type__])

    def test_unpack_msg(self):
        # Test unpacking a message from bytes
        msg = TestMsg(name="Unpack", value=456)
        serialized_msg = msg.to_bytes()
        unpacked_msg = unpack_msg(serialized_msg)

        self.assertIsInstance(unpacked_msg, TestMsg)
        self.assertEqual(msg.name, unpacked_msg.name)
        self.assertEqual(msg.value, unpacked_msg.value)


if __name__ == "__main__":
    unittest.main()
