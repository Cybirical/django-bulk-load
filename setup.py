import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "1.4.8"

setuptools.setup(
    name="cyb-django-bulk-load",
    version=__version__,
    author="Cedar",
    author_email="support@cedar.com",
    license="MIT",
    description="Bulk load Django models [Cybirical Fork]",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cybirical/django-bulk-load",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    python_requires=">=3.9",
    install_requires=[
        "django>=5.1",
        "psycopg>=3.2.2",
    ],
    extras_require={"test": []},
)
