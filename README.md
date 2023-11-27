# Text Organizer Web Application

This project is a full-stack web application that utilizes HTML, CSS, and JavaScript for the frontend , Flask as the backend, which is used to  integrate a Machine Learning model. The aim of the application is to take a text file as input and organize its information.
This project was done under the guidance of Professor Sumit Anand

## Features

- **Text File Input:** Users can upload a text file containing unstructured information.
- **Text Input:** Users can write the text they want to be organized.
- **ML Model Integration:** The application incorporates a Machine Learning model that processes the text file and identifies sections to create subheadings.
- **Dynamic Interface:** The frontend provides a user-friendly interface that dynamically displays the organized content.
- **Flask Backend:** The backend, built with Flask, handles file uploads, interacts with the ML model, and serves processed data to the frontend.

## Prerequisites

Before running this application, ensure you have the following installed:

- Python = 3.11.x


## Installation and Usage
### For Linux Users:
   
   1. Clone the repository:
   
      ```bash
      git clone git@github.com:Sauptik23/InsightsAI.git
      ```
   
   2. Install the required dependencies:
   
      ```bash
      pip install -r requirements.txt
      ```
   
   3. Navigate to the project directory and run the Flask application:
   
      ```bash
      python app.py
      ```
   
   4. Access the application in your web browser at `http://localhost:5000`.

## Usage Example

1. Open the web application in your browser.
2. Upload a text file containing unstructured information.
3. Submit the file for processing.
4. The application will organize the information into subheadings and display the structured content.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements or feature suggestions.

## Acknowledgments

- This project was inspired by the need to organize unstructured text data efficiently.
- Special thanks to contributors and Professor Sumit Anand for his guidance.
