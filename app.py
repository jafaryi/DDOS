
# with out strong endpoint*****************

# from flask import Flask, jsonify
# import time

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Server is running"

# @app.route("/test")
# def test():
#     return "Test endpoint response"

# @app.route("/data")
# def data():
#     return jsonify({
#         "message": "Sample data response",
#         "status": "ok"
#     })

# @app.route("/slow")
# def slow():
#     time.sleep(1)
#     return "Slow response endpoint"

# @app.route("/health")
# def health():
#     return jsonify({
#         "status": "healthy",
#         "service": "web server"
#     })

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)











# strong endpoint like a loop is added to the code to increase CPU usage so it would be great for monitoring********


# from flask import Flask, jsonify
# import time

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Server is running"

# @app.route("/test")
# def test():
#     return "Test endpoint response"

# @app.route("/data")
# def data():
#     return jsonify({
#         "message": "Sample data response",
#         "status": "ok"
#     })

# @app.route("/slow")
# def slow():
#     time.sleep(1)
#     return "Slow response endpoint"

# @app.route("/health")
# def health():
#     return jsonify({
#         "status": "healthy",
#         "service": "web server"
#     })

# @app.route("/compute")
# def compute():
#     total = 0
#     for i in range(1000000):
#         total += i * i
#     return jsonify({
#         "message": "Compute endpoint response",
#         "result": total
#     })

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
    
    
    
    
    





# request logging / 404 handler / 500 handler / Creat logs folder*******************



# from flask import Flask, jsonify, request
# import time
# import logging
# import os

# app = Flask(__name__)

# # Create logs directory if it does not exist
# if not os.path.exists("logs"):
#     os.makedirs("logs")

# # Logging configuration
# logging.basicConfig(
#     filename="logs/server.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# @app.before_request
# def log_request_info():
#     logging.info(f"Request: {request.method} {request.path} from {request.remote_addr}")

# @app.route("/")
# def home():
#     return "Server is running"

# @app.route("/test")
# def test():
#     return "Test endpoint response"

# @app.route("/data")
# def data():
#     return jsonify({
#         "message": "Sample data response",
#         "status": "ok"
#     })

# @app.route("/slow")
# def slow():
#     time.sleep(1)
#     return "Slow response endpoint"

# @app.route("/health")
# def health():
#     return jsonify({
#         "status": "healthy",
#         "service": "web server"
#     })

# @app.route("/compute")
# def compute():
#     total = 0
#     for i in range(1000000):
#         total += i * i
#     return jsonify({
#         "message": "Compute endpoint response",
#         "result": total
#     })

# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "error": "Endpoint not found"
#     }), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({
#         "error": "Internal server error"
#     }), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
    
    
    








# better logs (clear)****************



from flask import Flask, jsonify, request
import time
import logging
import os

app = Flask(__name__)

if not os.path.exists("logs"):
    os.makedirs("logs")

# Create custom logger
logger = logging.getLogger("custom_server_logger")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:
    file_handler = logging.FileHandler("logs/server.log", mode="w", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")

@app.route("/")
def home():
    return "Server is running"

@app.route("/test")
def test():
    return "Test endpoint response"

@app.route("/data")
def data():
    return jsonify({
        "message": "Sample data response",
        "status": "ok"
    })

@app.route("/slow")
def slow():
    time.sleep(1)
    return "Slow response endpoint"

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "web server"
    })

@app.route("/compute")
def compute():
    total = 0
    for i in range(1000000):
        total += i * i
    return jsonify({
        "message": "Compute endpoint response",
        "result": total
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error"
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    