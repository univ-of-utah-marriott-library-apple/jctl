import setuptools
import subprocess
import os

jctl_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

#assert os.path.isfile("jctl/version.py")
with open("jctl/VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{jctl_version}\n")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jctl",
    version=jctl_version,
    author="The University of Utah",
    author_email="mlib-its-mac@lists.utah.edu",
    description="Command line tool that utilizes Python-Jamf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/univ-of-utah-marriott-library-apple/jctl",
    package_data={'jctl': ['VERSION']},
    include_package_data=True,
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