#!/usr/bin/env bash
# Cloud Agent install script for pandas 0.20.x.
#
# pandas 0.20.x targets the Python 3.6 / NumPy 1.13 / Cython 0.25 era, so this
# script provisions a pinned conda environment (matching the project's CI, which
# builds via miniconda) and builds the C/Cython extensions in place.
#
# This script must be idempotent: it can run repeatedly against a cached or
# partially prepared VM without failing or corrupting state.
set -euo pipefail

MINICONDA_DIR="${MINICONDA_DIR:-$HOME/miniconda3}"
ENV_NAME="pandas"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[cloud-install] repo dir: ${REPO_DIR}"

# 1. Install Miniforge (conda) if it is not already present.
if [ ! -x "${MINICONDA_DIR}/bin/conda" ]; then
    echo "[cloud-install] installing Miniforge into ${MINICONDA_DIR}"
    tmp_installer="$(mktemp --suffix=.sh)"
    curl -fsSL -o "${tmp_installer}" \
        "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
    bash "${tmp_installer}" -b -p "${MINICONDA_DIR}"
    rm -f "${tmp_installer}"
else
    echo "[cloud-install] reusing existing conda at ${MINICONDA_DIR}"
fi

# Make conda available to this non-interactive shell.
# shellcheck disable=SC1091
source "${MINICONDA_DIR}/etc/profile.d/conda.sh"

# 2. Create the pinned environment if it does not already exist.
#    Versions match the pandas 0.20.3 release era. pytest/xdist/forked are pinned
#    to versions compatible with the 0.20.x test suite (written for pytest 3.x).
if ! conda env list | grep -qE "^${ENV_NAME}\s"; then
    echo "[cloud-install] creating conda env '${ENV_NAME}'"
    conda create -y -n "${ENV_NAME}" -c conda-forge \
        "python=3.6" \
        "numpy=1.13" \
        "cython=0.25" \
        python-dateutil \
        pytz \
        setuptools \
        "pytest=3.2" \
        "pytest-xdist=1.20" \
        "pytest-forked=1.0" \
        flake8
else
    echo "[cloud-install] reusing existing conda env '${ENV_NAME}'"
fi

conda activate "${ENV_NAME}"

echo "[cloud-install] python: $(python --version 2>&1)"
python -c "import numpy, cython; print('[cloud-install] numpy', numpy.__version__, 'cython', cython.__version__)"

# 3. Build the C / Cython extensions in place and install pandas in develop mode.
#    build_ext only recompiles sources that changed, so re-running is cheap.
cd "${REPO_DIR}"
python setup.py build_ext --inplace -j "$(nproc)"
python setup.py develop

echo "[cloud-install] verifying import"
python -c "import pandas as pd; print('[cloud-install] pandas', pd.__version__, 'import OK')"

echo "[cloud-install] done"
