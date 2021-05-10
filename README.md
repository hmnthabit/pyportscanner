# pyportscanner
pyportscanner is a python script that identifies the active ports of a given host.

## Features

- Mutli-threaded port scans.
- Supports scanning a range of ports.
- Supports scanning a specific list of ports.
- Identifies the service names of the active ports.


## Requirements

- `colored` library

```bash
pip install colored
```


## Usage

- **Help menu**

```bash
python port_scanner.py --help
usage: port_scanner.py -a HOST -p PORT1,PORT2
Example 1: python3 port_scan.py -a HOST -p 21,80
Example 2: python3 port_scan.py -a HOST --portrange 1,100 -out scan1.txt

optional arguments:
  -h, --help            show this help message and exit
  -a HOST               Specify the target host
  -p PORTS              Specify The target ports
  --range RANGE         Specify the port range e.g --range 100,200
  -o output_file, --fout output_file		Specify the output file
```


## Examples

- **Scan a specific list of ports**

```bash
python port_scanner.py -a localhost -p 80,443,100 -o loclhost.txt
```

- **Scan a specific range of ports**

```bash
python port_scanner.py -a 192.168.0.100 --portrange 80,90
```
