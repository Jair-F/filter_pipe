#!/bin/bash

python3 -m pip install --break-system-packages -e ".[dev]"

pre-commit install
pre-commit run
