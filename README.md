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

### More examples

```python
from dataclasses import dataclass

from dinobytes import dbyte, unpackd

@dbyte
class Parent:
  def __init__(self, children: list[Child] | None =None):
    self.children = children or []

  def __repr__(self):
    return f"Parent(children={self.children})"

@dbyte
@dataclass
class Child:
  name:str = '<default>'

parent = Parent()
child = Child(name="Jimothy")

parent.children.append(child)

serialized = bytes(parent)
print(serialized)
print(unpackd(serialized))
```

Output:

```shell
b'\x92\x00\x91\xc4\n\x92\x01\xa7Jimothy'
Parent(children=[Child(name='Jimothy')])
```

---

```python
from dataclasses import dataclass

from dinobytes import dbyte, unpackd


@dbyte
@dataclass
class ClassA:
  value: int

@dbyte
@dataclass
class ClassB:
  value: str

@dbyte
@dataclass
class ClassC:
  value:list[int]


classA = ClassA(1)
classB = ClassB('hello')
classC = ClassC([1,2,3])

for x in [
  bytes(classB),
  bytes(classC),
  bytes(classA)
]:
  match unpackd(x):
    case ClassA(value):
      print(f'ClassA: {value=}')
    case ClassB(value):
      print(f'ClassB: {value=}')
    case ClassC(value):
      print(f'ClassC: {value=}')
    case _:
      print('unknown class')
```

Output:

```shell
ClassB: value='hello'
ClassC: value=[1, 2, 3]
ClassA: value=1
```

## Contributing

Contributions to DinoBytes are welcome! Whether it's bug reports, feature requests, or code contributions, please feel free to reach out or submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

DinoBytes is released under the Apache 2.0 License. See the LICENSE file for more details.
