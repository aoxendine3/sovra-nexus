from setuptools import setup, find_packages

setup(
    name="sovra-ctz",
    version="18.0.0",
    packages=find_packages(),
    install_requires=[
        "PyJWT>=2.8.0",
        "python-dotenv>=1.0.0"
    ],
    description="SOVRA Zero-Point Deep Locking API Middleware",
)
