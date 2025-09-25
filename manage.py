from app import create_app, db
from flask_migrate import Migrate

# Create app using your factory
app = create_app()

# Initialize migrations
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
