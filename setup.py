import setuptools
import re


def get_property(prop, file):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(file).read())
    return result.group(1)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jctl",
    version=get_property("__version__", "jctl/jctl"),
    author="The University of Utah",
    author_email="mlib-its-mac@lists.utah.edu",
    description="Command line tool that utilizes Python-Jamf",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/univ-of-utah-marriott-library-apple/jctl",
    scripts=["jctl/jctl", "jctl/pkgctl", "jctl/patch.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # 4 - Beta
        # 5 - Production/Stable
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.6",
    install_requires=["python-jamf>=0.6.9"],
)
