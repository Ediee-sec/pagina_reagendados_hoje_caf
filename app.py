from flask import Flask
from config import Config
from models import db
from routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    
    # Inicializar extensões
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(main)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5600)

