# Monitoring_Made_Ezy
<img width="1440" alt="Screenshot 2023-10-16 at 6 19 02 PM" src="https://github.com/rohitttsingh/Monitoring_Made_Ezy/assets/73903627/69389dc7-211c-4646-8abc-c024f74410a0">
<img width="603" alt="Screenshot 2023-10-16 at 6 19 31 PM" src="https://github.com/rohitttsingh/Monitoring_Made_Ezy/assets/73903627/87b29b25-4717-48ad-8b4a-5404a665d8f3">

# Flask Script for Infra API Data Retrieval and Excel Export

## Overview

This script is built using the Flask framework to interact with the Infra API, fetch customized data, and store it in a local Excel spreadsheet. It provides a simple web interface for initiating the data retrieval and exporting it to an Excel file. 

## Prerequisites

- Python installed on your system (3.6 or higher)
- Flask framework (you can install it using pip: `pip install Flask`)
- Requests library (you can install it using pip: `pip install requests`)
- Pandas library (you can install it using pip: `pip install pandas`)
- An active Infra API account and access credentials

## Installation and Setup

1. Clone the repository or download the script to your local machine.

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install Flask requests pandas
    ```

4. Configure your Infra API credentials:
   - Open the script and locate the place where API credentials are required.
   - Replace the placeholders with your Infra API credentials.

5. Run the Flask app:

    ```bash
    python app.py
    ```

6. Access the web interface in your browser at `http://localhost:3000`.

## Usage

1. Access the web interface in your browser at `http://localhost:3000`.

2. Provide the necessary parameters such as data customization options.

3. Click the "Fetch Data and Export to Excel" button.

4. The script will interact with the Infra API, retrieve the data, and save it to a local Excel file.

## Additional Notes

- You can customize the route and URL endpoint in the `app.py` file to fit your specific needs.
- Ensure that your Infa API credentials are kept secure and not hardcoded directly in the script if it's intended for production use.
- This script serves as a basic example. Depending on your requirements, you may need to implement error handling and additional features for robustness and scalability.

---

