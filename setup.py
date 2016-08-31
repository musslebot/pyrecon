try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="PyRECONSTRUCT",
    version="2.2.0",
    author="Michael Musslewhite",
    author_email="mdmusslewhite@gmail.com",
    url="https://github.com/musslebot/pyrecon",
    packages=[
        "classes",
        "tools",
        "gui"
    ],
    package_dir={
        "classes": "pyrecon/classes",
        "tools": "pyrecon/tools",
        "gui": "pyrecon/gui",
    },
    license="LICENSE.txt",
    description="Python for interacting with RECONSTRUCT files",
    long_description=open("README.txt").read(),
)
