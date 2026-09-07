# Copilot Instructions

## Project Overview

This repository contains a small FastAPI application for viewing and signing up for Mergington High School activities.

## Structure

- `src/app.py`: FastAPI application and in-memory activity data.
- `src/static/`: frontend HTML, JavaScript, and CSS served by the API.
- `src/README.md`: application-specific setup and endpoint documentation.
- `requirements.txt`: Python runtime dependencies.
- `pytest.ini`: pytest configuration.

## Development

- Install dependencies with `pip install -r requirements.txt`.
- Start the app from `src/` with `python app.py`.
- The API is available at `http://localhost:8000`; interactive docs are at `/docs`.
- Run Python checks from the repository root with `python3 -m compileall src`.

## Implementation Notes

- Keep changes focused on the FastAPI app and its static frontend.
- Activity data is intentionally in memory and resets when the process restarts.
- Preserve the existing endpoint contract unless a task explicitly changes it.
- There are currently no committed automated tests; add focused tests when changing API behavior.
