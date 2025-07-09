# **ChatSystem Backend**

Real-time messaging backend built with **Django**, **Django Channels**, and **Redis**, supporting WebSocket-based communication with features like live chat, typing indicators, and user presence tracking.

---

## **Key Features**

- **WebSocket Integration**:  
  Utilizes Django Channels to support WebSocket connections for real-time messaging.

- **Redis**:  
  Acts as the message broker to enable WebSocket functionality and handle asynchronous events.

- **Daphne**:  
  A production-ready ASGI server used to serve WebSocket and HTTP traffic.

- **Message Persistence**:  
  Messages are stored in a PostgreSQL or SQLite database using Django ORM.

- **Authentication**:  
  Supports token-based authentication for secure communication.

- **Online and Typing Indicators**:  
  Real-time updates for online users and typing notifications.

- **Role-based Access**:  
  Ensures users can only access conversations they are part of.

---

## **Understanding WebSocket**

WebSocket provides a persistent connection between the client and server, enabling bi-directional communication without waiting for a server response like HTTP. This is crucial for achieving real-time functionality.

---

## **WebSocket Setup in Django**

### Install Required Libraries

```bash
pip install channels_redis
pip install daphne
```

### Update `settings.py`

```python
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
```

### Start Redis Server

```bash
sudo apt install redis-server
sudo service redis-server start
redis-cli ping  # Should return PONG
```

---

## 📁 **Project Structure**

```plaintext
Backend/
├── chatapp/             # Core logic for managing conversations and messages
├── chatsystemproj/      # Django project folder with settings and ASGI config
│   ├── asgi.py          # Handles WebSocket connections
│   └── settings.py      # Django settings
├── consumers.py         # WebSocket consumers for real-time communication
├── manage.py            # Django project entry point
└── requirements.txt     # Dependencies list
```

---

## **Getting Started**

### Prerequisites

- Python 3.8+
- Node.js 14+
- Redis
- PostgreSQL or SQLite (for local development)

### Setup Instructions

1. **Create Virtual Environment**

   ```bash
   python -m venv env
   ```

2. **Activate Environment**

   - Windows:

     ```bash
     .\env\Scripts\activate
     ```

   - macOS/Linux:

     ```bash
     source env/bin/activate
     ```

3. **Navigate to Project Directory**

   ```bash
   cd chatsystemproj
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Start Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Run Daphne for WebSocket Support**

   ```bash
   daphne -b 0.0.0.0 -p 8000 chatsystemproj.asgi:application
   ```

---

## **Key Components**

### **Backend**

- **WebSocket Consumers**:

  - Message broadcasting
  - Typing notifications
  - Online user status updates

- **REST API**:
  - Fetching conversation messages
  - Creating new messages
  - Managing user authentication
