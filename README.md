# AI Mail Flask App

A Flask web application that generates email replies using OpenAI's GPT model, stores the replies in an SQLite database, and allows you to retrieve saved replies with pagination.

## Features

- **Generate Email Reply**: Sends a request to OpenAI's API to generate a professional reply to an email.
- **Save Replies**: Automatically saves the generated email reply along with the original email and timestamp in an SQLite database.
- **Get Saved Replies**: Retrieve stored replies with pagination for easy viewing.
- **Health Check**: A simple health check route to ensure the server is running.

## Installation

### Prerequisites

Ensure you have Python 3.x installed on your system. You also need an OpenAI API key.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/ai-mail-flask-app.git
   cd ai-mail-flask-app
   ```

2. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On MacOS/Linux:

     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the OpenAI API key**:

   Create a `.env` file in the project root and add your API key as follows:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Run the Flask app**:

   ```bash
   flask run
   ```

   The app will be available at `http://127.0.0.1:5000/`.

## Endpoints

### 1. **POST /generate-reply**

- **Description**: Generate a reply for the given email content.
- **Request Body**:

   ```json
   {
     "email_content": "I want to know about your services."
   }
   ```

- **Response**:

   ```json
   {
     "original_email": "I want to know about your services.",
     "ai_reply": "Here is the professional reply to your inquiry about our services..."
   }
   ```

### 2. **GET /get-replies**

- **Description**: Retrieve saved email replies with pagination.
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `limit`: Number of replies per page (default: 10)

- **Response**:

   ```json
   [
     {
       "id": 1,
       "original_email": "I want to know about your services.",
       "ai_reply": "Here is the professional reply to your inquiry about our services...",
       "timestamp": "2024-12-28T14:00:00"
     },
     {
       "id": 2,
       "original_email": "Can you provide more details on the service?",
       "ai_reply": "Sure! Here's more information on our services...",
       "timestamp": "2024-12-28T14:05:00"
     }
   ]
   ```

### 3. **GET /health**

- **Description**: Check if the server is running.
- **Response**:

   ```json
   {
     "status": "Server is running"
   }
   ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for the GPT model.
- Flask for building the web application.

```
