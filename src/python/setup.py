"""Setup script for OBDPHAWD Python package."""

from setuptools import setup, find_packages
import pathlib

# Read the README file
here = pathlib.Path(__file__).parent.parent.parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

# Read version from __init__.py
version = {}
with open("obdphawd/__init__.py") as fp:
    exec(fp.read(), version)

setup(
    name="obdphawd",
    version=version["__version__"],
    description="OBD2 and Automotive Protocol Handler with Bluetooth Low Energy Support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phawd/OBDPHAWD",
    author="PHAWD Team",
    author_email="support@phawd.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="obd2, automotive, bluetooth, ble, diagnostics, elm327",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "bleak>=0.20.0",
        "asyncio-mqtt>=0.11.0",
        "pyserial>=3.5",
        "crcmod>=1.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0",
            "isort>=5.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
        "docs": [
            "sphinx>=5.0",
            "sphinx-rtd-theme>=1.0",
        ],
        "gui": [
            "tkinter",
            "matplotlib>=3.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "obdphawd-scan=obdphawd.cli.scanner:main",
            "obdphawd-monitor=obdphawd.cli.monitor:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/phawd/OBDPHAWD/issues",
        "Source": "https://github.com/phawd/OBDPHAWD",
        "Documentation": "https://obdphawd.readthedocs.io/",
    },
)