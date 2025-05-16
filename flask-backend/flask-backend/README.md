 Flask Backend API
A robust Flask-based RESTful API backend service that provides various functionalities including authentication, story management, video handling, product management, and bubble features.
## Features
- User Authentication and Authorization using JWT
- Story Management System
- Video Processing
- Product Management
- Bubble System
- Settings Management
- Cross-Origin Resource Sharing (CORS) enabled
- PostgreSQL Database Integration
## Tech Stack
- Python 3.x
- Flask 2.3.2
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.4.4
- Flask-Marshmallow 0.14.0
- PostgreSQL (via psycopg2-binary)
- Flask-Migrate 4.0.4
## Project Structure
```
flask-backend/
├── app.py              # Main application initialization
├── config.py           # Configuration settings
├── models.py           # Database models
├── run.py             # Application entry point
├── schemas.py         # Marshmallow schemas for serialization
├── requirements.txt   # Project dependencies
└── routes/           # API endpoints
    ├── auth.py       # Authentication routes
    ├── bubble.py     # Bubble-related functionality
    ├── product.py    # Product management
    ├── settings.py   # Settings management
    ├── stories.py    # Story management
    └── video.py      # Video handling
```
## Installation
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in a `.env` file:
   ```
   DATABASE_URL=your_database_url
   JWT_SECRET_KEY=your_secret_key
   ```
## Running the Application
1. Activate the virtual environment if not already activated
2. Run the application:
   ```bash
   python run.py
   ```
   The server will start on `http://localhost:5000`
## API Endpoints
### Authentication
- POST `/auth/login` - User login
- POST `/auth/register` - User registration
### Stories
- GET `/stories` - Get all stories
- POST `/stories` - Create a new story
- GET `/stories/<id>` - Get specific story
- PUT `/stories/<id>` - Update a story
- DELETE `/stories/<id>` - Delete a story
### Products
- GET `/products` - Get all products
- POST `/products` - Create a new product
- GET `/products/<id>` - Get specific product
### Settings
- GET `/settings` - Get user settings
- PUT `/settings` - Update user settings
### Videos
- GET `/videos` - Get all videos
- POST `/videos` - Upload a new video
- GET `/videos/<id>` - Get specific video
### Bubbles
- GET `/bubbles` - Get all bubbles
- POST `/bubbles` - Create a new bubble
- GET `/bubbles/<id>` - Get specific bubble
- PUT `/bubbles/<id>` - Update a bubble
- DELETE `/bubbles/<id>` - Delete a bubble
## Security
- JWT-based authentication
- CORS enabled for cross-origin requests
- Database credentials and sensitive information stored in environment variables
## Development
The application runs in debug mode by default when running through `run.py`. For production deployment, ensure to:
- Disable debug mode
- Configure proper CORS settings
- Use proper security measures
- Set up proper database configurations
## Database
The application uses PostgreSQL as its database. Make sure to:
1. Have PostgreSQL installed and running
2. Create a database
3. Configure the database URL in your environment variables
## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
