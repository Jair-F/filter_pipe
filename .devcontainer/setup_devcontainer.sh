#!/bin/bash

python3 -m pip install --break-system-packages -r requirements.txt

pre-commit install
pre-commit run
