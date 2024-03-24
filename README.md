# Flask PDF Q&A System with User Authentication

This project implements a Flask-based Question and Answering (Q&A) system that allows users to upload PDF files, trains a model using the uploaded PDF, and then provides answers to questions posed by the users based on the content of the PDF. Additionally, it incorporates user authentication functionalities to secure certain routes of the application.

## Features

- **User Authentication:** Users can register and log in securely to access protected routes.
- **PDF Upload:** Users can upload PDF files for processing.
- **Q&A System:** The application extracts text from uploaded PDF files, trains a model, and provides answers to user questions based on the content of the PDF.
- **Dynamic HTML Rendering:** HTML templates are rendered dynamically based on user actions.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- Flask
- PyPDF2
- Cassandra
- langchain_openai
- Werkzeug

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/your_repository.git
    cd your_repository
    ```

2. **Install the dependencies:**

    ```bash
    pip install Flask PyPDF2 cassandra-driver langchain_openai
    ```

3. **Set up your environment variables:**

    - `ASTRA_DB_APPLICATION_TOKEN`: Your Astra DB application token.
    - `ASTRA_DB_ID`: Your Astra DB ID.
    - `OPENAI_API_KEY`: Your OpenAI API key.
    - `SECRET_KEY`: A secret key for Flask session management.
  
## Usage

1. **Initialize the SQLite database by running:**

    ```bash
    python app.py
    ```

2. **Start the Flask server:**

    ```bash
    python app.py
    ```

3. **Access the application in your browser at** `http://localhost:5000`.

## Routes

- **/**: Renders the login page.
- **/register**: Allows users to register with a unique username and password.
- **/login**: Enables users to log in with their credentials.
- **/protected**: Renders the protected route after successful authentication.
- **/upload**: Handles file upload for PDF processing.
- **/ask**: Accepts POST requests to ask questions and returns answers.


