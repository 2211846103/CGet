#    CGet - A lightweight package manager for C++ projects using CMake and CPM.
#    Copyright (C) 2025  Mohamed Ibrahim
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    For questions, feedback, or contributions, you can reach me at:
#                   Email: m.ibrahim9276@gmail.com


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