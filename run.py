from app import create_app

app = create_app()
from app import db, create_app
from app.models import User, FoodPost

app = create_app()

with app.app_context():
    db.create_all()   # 🚀 Creates all tables if not exist


if __name__ == '__main__':
    app.run(debug=True)
