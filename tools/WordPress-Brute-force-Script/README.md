# WordPress Brute-force Script (WPForce-based) 🔓

This project provides a simple WordPress brute-force script, leveraging the **WPForce** tool to perform brute-force login attempts on WordPress sites. 🚀

## Table of Contents 📚

- [Introduction](#introduction)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Install Dependencies](#install-dependencies)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Brute-force Script](#running-the-brute-force-script)
  - [Additional Options](#additional-options)
- [Customization](#customization)
- [Notes](#notes)
- [License](#license)

## Introduction 👨‍💻

This tool automates the process of brute-forcing WordPress login credentials. It fetches usernames from the WordPress REST API, combines them with common passwords, and attempts login using **WPForce**. 💥

![Demo](https://i.imgur.com/zvzJUnG.gif)

## Setup 🛠️

### Prerequisites 📋

Before using the script, ensure you have the following dependencies installed:

- **Python 2.x** (for running WPForce)
- **Python 3.x** (for running the custom brute-force script)
- **[WPForce](https://github.com/n00py/WPForce)** - A WordPress brute-forcing tool 🧰

### Install Dependencies ⚙️

1. Clone this repository:
    ```bash
    git clone https://github.com/avishaigonen123/WordPress-vuln-lab.git
    cd WordPress-vuln-lab
    ```

2. Install necessary Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
3. Navigate to the folder:
    ```bash
    cd tools/WordPress-Brute-force-Script
    ```

4. Clone WPForce (if not done already):
    ```bash
    git clone https://github.com/n00py/WPForce.git
    ```

### Configuration ⚡

- Ensure that you have `wpforce.py` downloaded from [WPForce GitHub](https://github.com/n00py/WPForce). 🔧
- You can adjust configurations like the user-agent in the script to suit your needs. ✨

## Usage 💡

### Running the Brute-force Script ⚔️

To run the script, use the following command:

```bash
python3 run_bruteforce.py <target-domain> [--agent "<user-agent-string>"]
```

Where:
- `<target-domain>` is the domain of the WordPress site you want to target (e.g., `example.com`).
- `[--agent "<user-agent-string>"]` is an optional argument to specify a custom User-Agent for the requests. If not specified, the default User-Agent will be used. 

Example:
```bash
python3 run_bruteforce.py example.com --agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
```

### Additional Options ⚙️

- If no User-Agent is provided, a default one is used.
- The script will automatically download common passwords or use an existing `pwd.txt` file for the brute-force attempts. 🔑

## Customization 🎨

- **User-Agent**: You can pass a custom user-agent string to bypass security mechanisms that block generic user-agent strings. 🧳
- **Password Lists**: You can modify the `pwd.txt` file with your own password list for brute-forcing. 🗂️

## Notes 📝

- The script works only with WordPress sites that expose their user list via the REST API (`/wp-json/wp/v2/users`). 📡
- If the target website has security measures such as CAPTCHA, rate-limiting, or WAF, brute-forcing may be blocked. 🛑

## License 🛡️

This project is licensed under the MIT License.
