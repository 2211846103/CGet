from setuptools import setup, find_packages


setup(
  name="cget",
  version="0.1.0",
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    "click>=8.0",
    "requests>=2.0"
  ],
  entry_points={
    "console_scripts": [
      "cget = cget.cli:cli",
    ]
  },
  author="Mohamed Ibrahim",
  description="Lightweight C++ package manager using CPM and CMake made with Python",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
  ],
  python_requires='>=3.7',
)