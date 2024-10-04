# Samsung J8  Nethunter Kernel Development
**This repository contains the kernel source and build scripts for the Samsung Galaxy J8 (model j8y18lte). The scripts automate the process of building the kernel and applying necessary nethunter patches**.

## Prerequisites
**Before you begin, ensure you have the following installed on your system:**

**Install Required Packages**
You can install the required packages using the following commands:
```bash
sudo apt update


sudo apt install -y build-essential


sudo apt install -y git


sudo apt install -y make


sudo apt install -y zip

# Install patch
sudo apt install -y patch

# Install additional packages (optional but recommended)
sudo apt install -y bc bison flex libssl-dev libncurses5-dev libelf-dev

