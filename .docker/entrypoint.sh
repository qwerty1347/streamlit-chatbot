#!/bin/bash
set -e

cd /app

exec streamlit run main.py --server.port=${PORT:-8501} --server.address=0.0.0.0