import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jctl",
    version="1.1.4",
    author="The University of Utah",
    author_email="mlib-its-mac@lists.utah.edu",
    description="Command line tool that utilizes Python-Jamf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/univ-of-utah-marriott-library-apple/jctl",
    scripts=['jctl/jctl','jctl/pkgctl'],
    entry_points={
        'console_scripts': ['jamfconfig=jamf.setconfig:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # 4 - Beta
        # 5 - Production/Stable
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
)
