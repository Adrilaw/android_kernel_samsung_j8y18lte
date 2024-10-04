# Samsung J8  Nethunter Kernel Development
**This repository contains the kernel source and build scripts for the Samsung Galaxy J8 (model j8y18lte). The scripts automate the process of building the kernel and applying necessary nethunter patches**.

## Prerequisites
**Before you begin, ensure you have the following installed on your system:**

**Install Required Packages**
You can install the required packages using the following commands:
```bash
sudo apt update
```
```bash
sudo apt install -y build-essential
```
```bash
sudo apt install -y git
```
```bash
sudo apt install -y make
```
```bash
sudo apt install -y zip
```
```bash
sudo apt install -y patch
```
```bash
sudo apt install -y bc bison flex libssl-dev libncurses5-dev libelf-dev
```

## Installing Kernel 
```bash
git clone -b branchname https://github.com/Adrilaw/android_kernel_samsung_j8y18lte
```
```bash
cd android_kernel_samsung_j8y18lte
```
## Compile Kernel
**In the kernel source there is a file build-nethunter-kernel.py called this script automates the building of the kernel it downloads toolchain and applies patches.**

### Note !! When first time running script when patches prompt pop ups enter no for script to apply patches also when the config screens start refer to the nethunter porting guide to configure kernel.
```bash
python3 build-nethunter-kernel.py
```
**wait a few minutes and kernel will be in your home directory named nethunter-j8-kernel.zip**
