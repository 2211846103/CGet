# CGet

**CGet** is a lightweight C++ package manager designed to simplify dependency management using [CPM.cmake](https://github.com/cpm-cmake/CPM.cmake). It automatically fetches, installs, and configures external CMake-based packages via GitHub repositories.

---

## Features
- Add dependencies via GitHub 
- Header + source file retrieval
- CLI-based interface with modular command support (`add`, `install`, `remove`, and `list`)

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/2211846103/CGet.git
cd CGet
pip install -r requirements.txt
```

---

## Usage

### Initialize a project:
```bash
python cget.py init
```

### Install a dependency:
```bash
python cget.py install fmtlib/fmt
```

### Remove a dependency:
```bash
python cget.py remove fmtlib/fmt
```

### List all dependencies:
```bash
python cget.py list
```

---

## Supported Platforms

- Linux 
- macOS 
- Windows (Python required)

---

## Contact

**Author:** Mohamed Ibrahim  
**Email:** m.ibrahim9276@gmail.com

---

## 📄 License

This project is licensed under the GNU General Public License v3.0.  
See [LICENSE](LICENSE) for more details.
