#!/bin/bash
gunicorn run:app --threads 2 -b 0.0.0.0:8080 --reload 
#python run.py