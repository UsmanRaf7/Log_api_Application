from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Log model for the database
class LogRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    level = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create database tables within an application context
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    """
    Root endpoint to display a welcome message.
    """
    return jsonify({
        "message": "Welcome to the Log API. Use /log to send logs and /logs to retrieve them."
    })

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/log', methods=['POST'])
def collect_log():
    """
    Endpoint to collect log records.
    Expects JSON input with 'level' and 'message' fields.
    """
    data = request.get_json()
    
    if not data or 'level' not in data or 'message' not in data:
        return jsonify({"error": "Invalid input. 'level' and 'message' are required."}), 400

    level = data['level']
    message = data['message']

    # Create a new log record
    log_record = LogRecord(level=level, message=message)
    db.session.add(log_record)
    db.session.commit()

    return jsonify({"message": "Log recorded successfully."}), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Endpoint to retrieve all stored logs.
    """
    logs = LogRecord.query.all()
    logs_list = [
        {
            "id": log.id,
            "timestamp": log.timestamp.isoformat(),
            "level": log.level,
            "message": log.message
        }
        for log in logs
    ]

    return jsonify({"logs": logs_list})

if __name__ == '__main__':
    app.run(debug=True)
