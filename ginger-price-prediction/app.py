from flask import Flask, render_template, request, jsonify
from config import Config
from database.models import init_db

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db(app)
from database.models import db

# Import routes
from routes import auth, dashboard, prediction, weather, analysis, api
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(prediction.bp)
app.register_blueprint(weather.bp)
app.register_blueprint(analysis.bp)
app.register_blueprint(api.bp)

# Main route
@app.route('/')
def index():
    return render_template('dashboard/index.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)