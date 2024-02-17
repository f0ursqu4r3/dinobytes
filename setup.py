from setuptools import find_packages, setup

setup(
    name="dinobytes",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "msgpack>=1.0.2",
    ],
    author="Kyle Dougan",
    author_email="kdougan@gmail.com",
    description="Dino-Bytes: A Dynamic Serialization Framework for Network Communication",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kdougan/dino-bytes",
)
