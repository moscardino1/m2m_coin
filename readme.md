# M2M Coin System

## Description
The M2M Coin System is a Flask-based application that simulates a decentralized cryptocurrency system where participants can transact coins with each other and interact with a central bank. This README provides an overview of the application structure, key functionalities, and instructions for running the application.

## Installation
1. Clone the repository:
  ```
git clone <repository_url>
  ```

2. Navigate to the project directory:
  ```
cd <project_directory>
  ```

3. Install dependencies using pip:
  ```
pip install -r requirements.txt
  ```


## Usage
1. Set up the database:
- Ensure you have SQLite installed.
- Run the following command to create the SQLite database:
  ```
  python app.py
  ```

2. Run the application:
python app.py


3. Access the application:
- Open a web browser and go to `http://127.0.0.1:5000`.

## Features
- **User Registration and Login:** Participants can register and log in to the system securely.
- **Profile Management:** Users can update their profile information, including their name and profile picture URL.
- **Coin Transactions:** Participants can transfer coins to other users with transaction subject descriptions.
- **Central Bank Operations:** The central bank manages the total coin supply and redistributes coins among active participants.
- **Transaction Logs:** All transactions are logged with timestamps, sender, receiver, amount, and subject.
- **FAQ Page:** Provides answers to frequently asked questions about the M2M Coin System.

## Project Structure
- **model.py:** Defines the database models for participants, the central bank, and transactions.
- **app.py:** Configures the Flask application and initializes the database.
- **routes.py:** Contains route definitions for different endpoints and their corresponding functionalities.
- **templates:** Contains HTML templates for rendering the user interface.
- **static:** Contains static files such as CSS stylesheets and images.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/feature-name`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries or suggestions, please contact [alessandrocarli90@gmail.com](mailto:alessandrocarli90@gmail.com).
