from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ==============================================
# CONFIG - @Adarsh_330
# ==============================================

DEVELOPER = "@Adarsh_330"
OWNER = "@Adarsh_330"
API_KEY = "@Adarsh_330"
ORIGINAL_API = "https://mowa-endpoints.vercel.app/api/mobile"

# ==============================================
# RESPONSE MODIFIER
# ==============================================

def modify_response(data):
    if isinstance(data, dict):
        data.pop("developer", None)
        data.pop("owner", None)
        data.pop("dev", None)
        
        if "data" in data and isinstance(data["data"], dict):
            data["data"].pop("developer", None)
            data["data"].pop("owner", None)
            data["data"].pop("dev", None)
        
        data["developer"] = DEVELOPER
        data["owner"] = OWNER
        
        if "data" in data and isinstance(data["data"], dict):
            data["data"]["developer"] = DEVELOPER
            data["data"]["owner"] = OWNER
        
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
    
    return data

# ==============================================
# ROUTES
# ==============================================

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Mobile Number Information API",
        "developer": DEVELOPER,
        "owner": OWNER,
        "version": "2.0",
        "endpoints": {
            "/api/mobile": "?key=@Adarsh_330&query=number"
        }
    })

@app.route('/api/mobile', methods=['GET'])
def mobile_info():
    key = request.args.get('key')
    query = request.args.get('query', '')
    
    if key != API_KEY:
        return jsonify({
            "status": "error",
            "message": "Invalid API key",
            "developer": DEVELOPER,
            "owner": OWNER
        }), 401
    
    if not query or len(query) < 2:
        return jsonify({
            "status": "error",
            "message": "Query must be at least 2 characters",
            "developer": DEVELOPER,
            "owner": OWNER,
            "detail": [{
                "loc": ["query", "q"],
                "msg": "String should have at least 2 characters",
                "input": query,
                "ctx": {"min_length": 2}
            }]
        }), 400
    
    try:
        original_url = f"{ORIGINAL_API}?key={API_KEY}&query={query}"
        response = requests.get(original_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            modified_data = modify_response(data)
            return jsonify(modified_data)
        else:
            return jsonify({
                "status": "error",
                "message": f"Request failed",
                "developer": DEVELOPER,
                "owner": OWNER
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "developer": DEVELOPER,
            "owner": OWNER
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "success",
        "message": "API is running",
        "developer": DEVELOPER,
        "owner": OWNER,
        "timestamp": datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "developer": DEVELOPER,
        "owner": OWNER
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "developer": DEVELOPER,
        "owner": OWNER
    }), 500

if __name__ == "__main__":
    print("=" * 60)
    print("🔥 MOWA API CLONE")
    print("=" * 60)
    print(f"👤 Developer: {DEVELOPER}")
    print(f"👑 Owner: {OWNER}")
    print(f"🔑 API Key: {API_KEY}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
