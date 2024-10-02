# Movie Ratings Service

## Overview

This service allows users to register, log in, rate movies, and retrieve movie details and ratings.

## Group Members

1. Esteban Tinajero
2. Donovan Bosson
3. Haroutyun Chamelian
4. Tyler Carlsen

## Endpoints

### POST `/register`

- **Description**: Registers a new user with an email, password, and an optional admin role.
- **Request Body**:

  ```json
  {
    "email": "user@example.com",
    "password": "password",
    "is_admin": "true"
  }
  ```

  - `is_admin` is an optional field; if omitted, the default value is `false`.

### POST `/login`

- **Description**: Authenticates a user and returns an access token upon successful login.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password"
  }
  ```

### POST `/movies`

- **Description**: Adds a new movie to the database (Admin only).
- **Authentication**: Access token required.
- **Request Body**:

  ```json
  {
    "title": "Movie Title",
    "director": "John Doe",
    "genre": "Action",
    "release_year": "2024"
  }
  ```

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:TinajeroOC/CPSC-449-Movie-Ratings-Service.git
   ```

2. Change directory:

   ```bash
   cd CPSC-449-Movie-Ratings-Service
   ```

3. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

4. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Generate a hex string, create a `.env` file, and assign it to `JWT_SECRET_KEY`:

   ```bash
   openssl rand -hex 32
   ```

   > If `openssl` is not installed on your machine, then you can use an online tool to generate a random hex string.

7. Run the service:
   ```bash
   python server.py
   ```
