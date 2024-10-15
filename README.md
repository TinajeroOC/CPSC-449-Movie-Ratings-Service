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
  
### POST `/update`




  



- **Description**: Allows a user to update their movie rating.
- **Authentication**: Access token required.
- **Fields**:
  - `movie_title` (string, required): The title of the movie.
  - `movie_release_year` (string, required): The year the movie was released.
  - `rating` (int, required): The new rating the user wishes to give the movie. Must be an integer between 1 and 5.
- **Request Body**:

  ```json
  {
    "movie_title": "Movie Title",
    "movie_release_year": "2024",
    "rating": 5
  }
  ```
  
### POST `/delete`

- **Description**: Allows a user to delete their own movie rating.
- **Authentication**: Access token required.
- **Fields**:
  - `movie_title` (string, required): The title of the movie.
  - `movie_release_year` (int, required): The year the movie was released.
- **Request Body**:

  ```json
  {
    "movie_title": "Movie Title",
    "movie_release_year": "2024"
  }
  ```
  
### POST `/admin/delete`

- **Description**: Allows an admin to delete any user's movie rating.
- **Authentication**: Access token required.
- **Fields**:
  - `movie_title` (string, required): The title of the movie.
  - `movie_release_year` (int, required): The year the movie was released.
  - `user_id` (string, required): The UUID of the user whose rating you wish to delete.

- **Request Body**:

  ```json
  {
    "movie_title": "Movie Title",
    "movie_release_year": "2024",
    "user_id": "e7af5813-0849-4768-ab9c-3d2de6da7bfc"
  }
  ```


  ### File Upload Endpoint

#### POST `/upload`

- **Description**: Allows authenticated users to upload files to the server. Only files with allowed extensions will be accepted.

- **Authentication**: Access token required.

- **Request** (via Postman):
  
  - Select the `POST` method.
  - Set the URL to: `http://localhost:5000/upload`
  - In the "Authorization" tab, select `Bearer Token` and paste your access token.
  - In the "Body" tab, select `form-data`, and add a key named `file` with the type set to `File`. Upload the file you want to send.

- **Response**:
  - On success:
    ```json
    {
      "message": "File <filename> uploaded successfully"
    }
    ```
  - On failure (e.g., unsupported file type):
    ```json
    {
      "error": "File type not allowed"
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
