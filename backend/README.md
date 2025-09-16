# Trash-Kan Backend

This is the backend API for the Trash-Kan application, built with FastAPI.

## Features

- FastAPI web framework
- OAuth integration
- RESTful API endpoints

## Installation

```bash
poetry install
```

## Running the API

```bash
poetry run uvicorn api.main:app --reload
```

## Dependencies

- FastAPI: Web framework for building APIs
- Uvicorn: ASGI server
- Requests: HTTP library
- OAuthLib: OAuth implementation