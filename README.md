
# SEEKER

A Python-based multithreaded port scanner designed for efficiently scanning open ports on a target system. This tool utilizes threading to improve scanning speed by concurrently checking multiple ports.


## Installation

Clone the project

```bash
  git clone https://github.com/Dark-Menace/Seeker.git
```

Go to the project directory

```bash
  cd Seeker
```
Install dependencies

```bash
  pip install -r requirements.txt

```




## Usage

Run the port scanner:

```bash
  python seeker.py X.X.X.X <scan flags>
```
Replace "X.X.X.X" with the IPv4 address of the target and use the required scan flags.

## Command-Line Options
```bash
 _____ _____ _____ _____ _____ _____ 
|   __|   __|   __|  |  |   __| __  |
|__   |   __|   __|    -|   __|    -|
|_____|_____|_____|__|__|_____|__|__|
                                     
usage: seeker.py <IPv4 address> [Scan type flags]

Seeker 1.1

positional arguments:
  host                  IPv4 of the host to scan.

options:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Scan a specific port, use "-" to specify a port range.
  -q, --quick           Quick scan the top 100 ports.
  -a, --all             Scan all ports (0-65535).
  -sV, --service        Display port services.
  -o OUTPUT, --output OUTPUT
                        Store the output in a text file at the path .
```
## Example
Scanning the IPv4 of google.com

```bash
  python seeker.py 142.250.183.228 -p 0-450
```
Here the scanner tries to ping the target through a port range of "0-450".
Without the "-p" flag the scanner script scans the most commonly used 1000 ports.

```bash                                       
 _____ _____ _____ _____ _____ _____ 
|   __|   __|   __|  |  |   __| __  |
|__   |   __|   __|    -|   __|    -|
|_____|_____|_____|__|__|_____|__|__|
                                     
142.250.183.228:   80 is open
142.250.183.228:  443 is open
```
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Disclaimer

This tool is for educational purposes only. Use responsibly and ensure compliance with applicable laws and regulations.
