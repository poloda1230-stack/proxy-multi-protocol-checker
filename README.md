Project Introduction
A multi-protocol proxy detector (HTTP / HTTPS / SOCKS5) that supports batch reading proxies from a text file, tests their availability using multi-threading, and outputs separate lists of available proxies. This project is an original implementation and does not depend on or reference code or materials from other repositories.

Features
Supported Protocols: HTTP, HTTPS, and SOCKS5.

Batch Checking: Reads a list of proxies from a file (one ip:port per line).

Multi-threading: Uses a thread pool for parallel checking to speed up detection.

Result Output: Automatically writes available proxies to good_http.txt, good_https.txt, and good_socks5.txt.

File Structure
main.py: Command-line entry point, menu, and interaction.

checker.py: Core detection logic and multi-threading implementation.

requirements.txt: Python dependency list (requests + SOCKS support).

proxies.txt: List of proxies to be checked (must be filled in by the user).

Proxy List Format
Edit proxies.txt in the repository's root directory. Add one proxy per line in the format:

ip:port

Example:

127.0.0.1:8080
127.0.0.1:1080
Lines beginning with # can be used as comments and will be ignored.

Environment Requirements
Python 3.8+ (3.10 or higher recommended).

pip (Python package manager).

This project has been verified to install and run on the following systems:

Debian series (e.g., Debian 11/12)

Ubuntu series (e.g., Ubuntu 20.04/22.04/24.04)

Alpine Linux (3.x)

Installation and Usage on Debian / Ubuntu
Install system dependencies:

Bash

sudo apt update
sudo apt install -y git python3 python3-pip
Clone the repository:

Bash

cd ~
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install Python dependencies:

Bash

pip3 install -r requirements.txt
or

Bash

python3 -m pip install -r requirements.txt
Run the program:

Bash

python3 main.py
Follow the prompts to complete the check.

Installation and Usage on Alpine Linux
Install system dependencies:

Bash

apk update
apk add --no-cache git python3 py3-pip
If needed, create a symlink for python (convenient in some environments):

Bash

ln -sf python3 /usr/bin/python
Clone the repository:

Bash

cd /root
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install Python dependencies:

Bash

pip3 install -r requirements.txt
or

Bash

python3 -m pip install -r requirements.txt
Run the program:

Bash

python3 main.py
Usage Instructions
After starting the program, the terminal will display a menu:

Check HTTP

Check HTTPS

Check SOCKS5

Check All (HTTP, HTTPS, SOCKS5)

The program will then ask for the following:

Proxy list filename (Default proxies.txt, just press Enter).

Number of threads (Default 100. A higher number is faster but places more load on the machine).

Custom test URL (Leave blank to use the built-in httpbin.org/ip as the test target).

During the check, the terminal will print the result for each proxy in real-time, including:

[OK] / [BAD] status

Response time (in seconds)

HTTP status code or error reason

After completion, it will summarize the total count, available count, and total time elapsed. It will also generate corresponding output files in the current directory:

good_http.txt

good_https.txt

good_socks5.txt

Each file contains one available proxy per line, in the same format as the input file.

FAQ
Q: How do I quickly deploy this on different VPS? A: Just install git, python3, and pip. Then git clone the repository, install dependencies with pip, and run python3 main.py. Use apt for Debian/Ubuntu and apk for Alpine.

Q: How do I update the code? A: In the repository directory, run: git pull, and then re-run python3 main.py.
