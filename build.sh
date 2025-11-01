#!/bin/bash

# 1. Python packages install karo
pip install -r requirements.txt

# 2. C aur C++ compilers install karo
apt-get update
apt-get install -y gcc g++