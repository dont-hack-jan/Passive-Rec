# Passive-Rec

'Passive-Rec' is a Python-based passive reconnaissance tool that gathers information about a target domain using various OSINT sources and external tools.

## Features

- WHOIS lookup  
- DNS enumeration with `dig` and `host`  
- Subdomain discovery using `amass` and `subfinder` (passive mode)  
- Certificate Transparency logs from crt.sh  
- URL enumeration from the Wayback Machine  
- Shodan search integration  
- GitHub code search using GitHub API  

## Requirements

- Python 3.x  
- External tools installed and in your PATH:  
  - [amass](https://github.com/OWASP/Amass)  
  - [subfinder](https://github.com/projectdiscovery/subfinder)  
  - `dig` (usually pre-installed on Linux/macOS)  
  - `host` (usually pre-installed on Linux/macOS)  
- Python packages:
  - `requests`
  - `shodan` (`pip install shodan`)

## Setup

1. Clone or download this repository.

2. Install required Python packages:

   ```bash
   pip install requests shodan

## Usage

python3 recon.py example.com

## Outputs 

Outputs will be saved in a folder named recon-example.com/ with multiple files such as:

example.com/
├── whois.txt
├── dig.txt
├── host-mx.txt
├── host-txt.txt
├── amass.txt
├── subfinder.txt
├── crtsh.txt
├── wayback.txt
├── shodan.json
├── github.json
