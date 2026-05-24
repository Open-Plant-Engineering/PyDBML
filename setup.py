from setuptools import setup, find_packages

setup(
    name="pydbml",
    version="0.0.1",
    description="Python Database Macro Language",
    author="Shivang Kheradiya",
    author_email="shivangatul@gmail.com",
    url="https://github.com/Open-Plant-Engineering/PyDBML",
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.10",
    license="MIT license",
    project_urls={
        "Documentation": "https://github.com/Open-Plant-Engineering/PyDBML",
        "Source":"https://github.com/Open-Plant-Engineering/PyDBML",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: MIT License",   # change if needed
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    
)