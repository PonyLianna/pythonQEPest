# pythonQEPest

[![pythonQEPest](https://github.com/PonyLianna/pythonQEPest/actions/workflows/python-package.yml/badge.svg)](https://github.com/PonyLianna/pythonQEPest/actions/workflows/python-package.yml)


Python implementation of QEPest (Quantitative Estimation of Pesticide), a program for scoring molecules as herbicides (QEH), insecticides (QEI), and fungicides (QEF).

Originally published in: [J Cheminform - QEPest](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-014-0042-6)
Original Program Link is [here](https://static-content.springer.com/esm/art%3A10.1186%2Fs13321-014-0042-6/MediaObjects/13321_2014_42_MOESM2_ESM.zip)  

## Features

- Calculate pesticide scores for herbicidal, insecticidal, and fungicidal activity
- Command-line interface (CLI)
- Graphical User Interface (GUI)
- Support for JSON and TXT output formats

### Pre-built binaries

Download ready-to-use executables from [Releases](https://github.com/PonyLianna/pythonQEPest/releases):

| Platform | Download |
|----------|----------|
| Windows CLI | [main.exe](https://github.com/PonyLianna/pythonQEPest/releases/download/v2.0.0-alpha/main.exe) |
| Windows GUI | [gui.exe](https://github.com/PonyLianna/pythonQEPest/releases/download/v2.0.0-alpha/gui.exe) |


## Installation

```bash
pip install pythonQEPest
```

Or from source:

```bash
git clone https://github.com/PonyLianna/pythonQEPest.git
cd pythonQEPest
poetry install
```

### With GUI support

```bash
pip install pythonQEPest[gui]
# or
poetry install --with ui
```


## Quick Start

### CLI

```bash
pythonqepest -i data.txt -o result.txt
pythonqepest --input data.txt --format json
pythonqepest -v  # show version
```

### GUI

```bash
pythonqepest-gui
# or
python -m pythonQEPest.gui.gui
```

### Python API

```python
from pythonQEPest import QEPest, QEPestInput

# Create input data
qepest = QEPest()
qepest.initialize_coefficients()
qepest.initialize_normalisers()

# From individual values
inp = QEPestInput(
    name="mol1",
    mol_weight=240.2127,
    log_p=3.2392,
    hbond_acceptors=5,
    hbond_donors=1,
    rotatable_bonds=4,
    aromatic_rings=1
)

result = qepest.compute_params(inp)

print(result.name)       # mol1
print(result.data.qe_herb)   # 0.8511
print(result.data.qe_insect) # 0.5339
print(result.data.qe_fung)   # 0.6224

# Convert to array
print(result.to_array())  # ["mol1", 0.6224, 0.8511, 0.5339]
```

## Input Format

The input file should be a tab-separated text file with the following columns:

| Column | Description |
|--------|-------------|
| Name   | Molecule name |
| MW     | Molecular weight (g/mol) |
| LogP   | Hydrophobicity (octanol-water partition coefficient) |
| HBA    | Number of hydrogen bond acceptors |
| HBD    | Number of hydrogen bond donors |
| RB     | Number of rotatable bonds |
| arR    | Number of aromatic rings |

Example `data.txt`:

```
Name	MW	LogP	HBA	HBD	RB	arR
mol1	240.2127	3.2392	5	1	4	1
mol2	249.091	3.0273	3	1	5	1
mol3	308.354	2.1086	1	0	7	1
```

## Output Format

### TXT (default output for CLI)

```
Name	QEF	QEH	QEI
mol1	0.6224	0.8511	0.5339
mol2	0.7310	0.9750	0.6913
```

### JSON

```json
[
  {"name": "mol1", "qe_fung": 0.6224, "qe_herb": 0.8511, "qe_insect": 0.5339},
  {"name": "mol2", "qe_fung": 0.731, "qe_herb": 0.975, "qe_insect": 0.6913}
]
```

## Configuration

### Custom Coefficients

```python
from pythonQEPest import QEPest

custom_coefficients = {
    "herb": [
        (70.77, 283.0, 84.97, -1.185),
        (93.81, 3.077, 1.434, 0.6164),
        # ... 6 tuples total
    ],
    "insect": [...],
    "fung": [...]
}

qepest = QEPest(coefficients=custom_coefficients)
```

### Custom Normalisers

```python
from pythonQEPest import QEPest
from pythonQEPest.dto.normalisation.Normaliser import Normaliser

qepest = QEPest(normalisers={"herb": Normaliser(...), ...})
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i`, `--input` | Input file path | data.txt |
| `-o`, `--output` | Output file path | data.out.txt |
| `-f`, `--format` | Output format (json, txt) | txt |
| `-v`, `--version` | Show version | - |

## Development

### Run tests

```bash
poetry run pytest
```

### Build

```bash
# CLI executable
poetry run poe build-simple

# GUI executable
poetry run poe build-gui
```
