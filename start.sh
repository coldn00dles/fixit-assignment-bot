#!/bin/sh
uvicorn backend:app --host 0.0.0.0 --port 7860 --reload &
streamlit run app.py