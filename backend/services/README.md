# Services Folder Purpose

This folder contains backend business logic and data/model access utilities.

## File Purpose

- __init__.py: Marks services as a Python package.
- forecast_service.py: Loads and summarizes CNN+LSTM forecast outputs.
- battery_service.py: Loads battery degradation outputs and computes fleet metrics.
- dispatch_service.py: Loads dispatch model, runs prediction, and builds SHAP explanations.
