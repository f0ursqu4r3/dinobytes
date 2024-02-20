# DinoBytes

![dinobytes](./assets/dinobytes.png)

DinoBytes is a dynamic serialization framework designed to simplify network communication by providing a robust set of tools for serializing and deserializing messages using the MessagePack format. With its easy-to-use decorator and base class, DinoBytes makes defining and handling network messages both efficient and intuitive, suitable for applications ranging from simple messaging systems to complex distributed architectures.

## Features

- **Automatic Message Type Registration**: Utilizes a decorator to automatically register class types and assign unique identifiers, ensuring a smooth serialization and deserialization process.
- **Simplified Serialization**: Offers a straightforward method (`to_bytes`) for converting class objects into serialized bytes.
- **Effortless Deserialization**: Allows for easy conversion of bytes back into class objects using the `from_bytes` method, facilitating quick and reliable class parsing.
- **Streamlined Message Definition**: Leverages Python's dataclass decorator within the custom `dbyte` decorator to reduce boilerplate and enhance readability when defining new class types.
- **Message Registry**: Automatically maintains a registry of class types, simplifying the process of managing different kinds of network messages within your application.

## Installation

Install DinoBytes using pip:

```bash
pip install dinobytes
```

## Quick Start

### Defining a Message

```python
from dinobytes import dbyte

@dbyte
class MyMessage:
    content: str
```

### Serializing a Message

```python
message = MyMessage(content="Hello, DinoBytes!")
serialized_message = message.to_bytes() # or bytes(message)
```

### Deserializing a Message

```python
received_message = MyMessage.from_bytes(serialized_message)
print(received_message.content)  # Output: Hello, DinoBytes!
```

The `unpackd` convenience method can also be used to automatically unpack into the correct type:

```python
from dinobytes import unpackd

received_message = unpackd(serialized_message)
print(received_message.content)  # Output: Hello, DinoBytes!
```

## Contributing

Contributions to DinoBytes are welcome! Whether it's bug reports, feature requests, or code contributions, please feel free to reach out or submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

DinoBytes is released under the Apache 2.0 License. See the LICENSE file for more details.
