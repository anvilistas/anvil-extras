#!/bin/sh
# bumpversion_check.sh

set -e

python -m bumpversion --dry-run --verbose patch
