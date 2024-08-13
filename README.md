# Movie Listing App

This is a comprehensive movie listing application that allows users to register, log in, view, rate, and comment on movies. The application is built using FastAPI, PostgreSQL, and SQLAlchemy. Still some work to be done on the testing and containerizing.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **User Registration and Authentication**: Secure user registration and login using JWT tokens.
- **Movie Listing**: Browse through a catalog of movies with details such as title, release year, genre, and synopsis.
- **Movie Ratings**: Users can rate movies and provide a review.
- **Movie Comments**: Users can comment on movies and view comments by others.
- **Search Movies by Title**: Users can search for movies using their title.
- **API Documentation**: Automatic API documentation is provided through Swagger UI.

## Requirements

- **Python**: Version 3.10 or above
- **PostgreSQL**: Version 12 or above
- **Docker and Docker Compose**: For containerized deployment

## Installation

Follow these steps to set up the application on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- **On Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **On Linux/macOS**:

  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory and configure the following variables, Your sensitive information will be stored here:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/movie_listing_db
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/movie_listing_test_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
POSTGRES_DB=movie_listing_db
```

## Running the Application

To start the application, run the following command:

```bash
uvicorn movie_listing_app.main:app --reload
```

The application will be available at `http://localhost:8000`.

## Running Tests

To run the test suite, execute the following command:

```bash
pytest
```

This command will run all the tests located in the `tests` directory.

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when the application is running. It provides a user-friendly interface for interacting with the API endpoints.

## Docker Deployment

### Building the Docker Image

To build the Docker image, use the following command:

```bash
docker build -t movie-listing-app .
```

### Running the Docker Container

To start the application using Docker, run the following command:

```bash
docker-compose up
```

The application will be available at `http://localhost:8000`.

### Stopping the Docker Container

To stop the Docker containers, run:

```bash
docker-compose down
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeatureName`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeatureName`
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or need further assistance, please contact:

- **Name**: Golden-Joe Osegbe
- **Email**: osegbegoldenjoe1@gmail.com
- **GitHub**: [osegbeg](https://github.com/osegbeg)

---
