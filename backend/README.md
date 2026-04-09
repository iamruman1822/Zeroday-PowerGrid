# Backend Folder Purpose

This folder contains the Flask API server used by the XplainableAI project.

## File and Folder Guide

- app.py: Flask application entry point. Registers all API blueprints and CORS.
- requirements.txt: Python dependencies required to run the backend.
- .gitignore: Ignore rules for cache, environment, editor files, and logs.
- routes/: API endpoint layer. Each file defines HTTP routes for one module.
- services/: Data and model logic layer used by the route handlers.

## Routes Folder Purpose

The routes folder maps HTTP requests to service functions and returns JSON responses.

## Services Folder Purpose

The services folder loads model outputs, computes summaries, and performs dispatch inference.
