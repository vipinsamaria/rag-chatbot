# RAG-Chatbot

This repository contains a Retrieval-Augmented Generation (RAG)-based chatbot application. The chatbot is designed to provide intelligent responses by leveraging both retrieval-based methods and generative models.

## Features

- **Retrieval-Augmented Generation (RAG):** Combines traditional information retrieval with generative models to provide comprehensive responses.
- **Frontend UI:** A simple, intuitive HTML-based UI for interacting with the chatbot.
- **Scalable:** Can be adapted to various use cases with minor modifications.

## Folder Structure

- api/ # Contains the code logic to handle api requests
- db/ # Contains database code logic for configuration and database models.
- model/ #Contains the model code logic to generate answers
- UI/ # Frontend HTML file for client-side interactions


## Installation

To get started with this project, follow the steps below.

### Prerequisites

Ensure you have the following installed:

- Python 3.10.x
- Node.js (for running the frontend if any modifications are required)

### Backend Setup

1. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Start the backend server:

    ```bash
    uvicorn main:app --reload
    ```

### Frontend Setup

The frontend can be loaded directly in the browser by accessing the HTML file:

1. Navigate to the `UI` folder:

    ```bash
    cd UI
    ```

2. Open the `index.html` file in your browser:

    ```bash
    open index.html  # Or double-click the file
    ```

This will load the frontend for interacting with the chatbot.


Usage
Once both the backend and frontend are running, you can interact with the chatbot through the browser UI.
The chatbot takes a query from the user, retrieves relevant information, and generates a response using the RAG model.
Contributing
Feel free to open issues or submit pull requests for improvements, bug fixes, or additional features. Contributions are always welcome!

License
This project is licensed under the MIT License. See the LICENSE file for more information.
