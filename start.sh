#!/bin/sh
uvicorn backend:app --host localhost --port 7860 --reload &
streamlit run app.py