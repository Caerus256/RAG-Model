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

1. Clone the repository:

```bash
git clone https://github.com/your_username/your_repository.git
cd your_repository
