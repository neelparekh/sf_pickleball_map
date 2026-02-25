#!/bin/bash
# Local test of Railway deployment
cd backend && gunicorn app:app --bind 0.0.0.0:5000
