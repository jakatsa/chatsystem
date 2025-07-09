Key Features
Backend:
WebSocket Integration: Utilizes Django Channels to support WebSocket connections for real-time messaging.
Redis: Acts as the message broker to enable WebSocket functionality and handle asynchronous events.
Daphne: A production-ready ASGI server used to serve WebSocket and HTTP traffic.
Message Persistence: Messages are stored in a PostgreSQL or SQLite database using Django ORM.
Authentication: Supports token-based authentication for secure communication.
Online and Typing Indicators: Real-time updates for online users and typing notifications.
Role-based Access: Ensures users can only access conversations they are part of.

What You Need to Know About WebSocket
WebSocket provides a persistent connection between the client and server, enabling bi-directional communication without waiting for a server response like HTTP. This is crucial for achieving real-time functionality.

To set up WebSocket in Django:

Install the Django Channels library:
pip install channels_redis
pip install daphne
Update your settings.py to configure Channels and Redis:
INSTALLED_APPS = [
...
'channels',
]

ASGI_APPLICATION = "chatsystemproj.asgi.application"

CHANNEL_LAYERS = {
"default": {
"BACKEND": "channels_redis.core.RedisChannelLayer",
"CONFIG": {
"hosts": [("127.0.0.1", 6379)],
},
},
}
Ensure you have a running Redis server:
sudo apt install redis-server
sudo service redis-server start
redis-cli ping # Should return PONG

Project Structure
Backend:
chatapp/: Contains the core logic for managing conversations and messages.
chatsystemproj/: The Django project folder, including settings and ASGI configuration.
asgi.py: Configures the ASGI application to handle WebSocket connections.
consumers.py: Implements WebSocket consumers for handling real-time communication.

Getting Started
Prerequisites
Python 3.8+
Node.js 14+
Redis
PostgreSQL (or SQLite for local development)
Backend Setup
Create a Virtual Environment:
python -m venv env
Activate the Virtual Environment:
On Windows:
.\env\Scripts\activate
On macOS/Linux:
source env/bin/activate
Navigate to the Backend Directory:
cd chatsystemproj
Install Dependencies:
pip install -r requirements.txt
Run Migrations:
python manage.py migrate
Run the Development Server:
python manage.py runserver
Run Daphne (for WebSocket support):
daphne -b 0.0.0.0 -p 8000 chatsystemproj.asgi:application

Key Components
Backend:
WebSocket Consumers: Handles incoming and outgoing WebSocket messages, including:

Message broadcasting.
Typing notifications.
Online user status updates.
REST API: Provides endpoints for:

Fetching conversation messages.
Creating new messages.
Managing user authentication.
