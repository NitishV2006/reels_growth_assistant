import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from db.supabase_client import supabase

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Server running"}), 200


@app.route("/add_reel", methods=["POST"])
def add_reel():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # Required fields validation
        required_fields = [
            "topic",
            "format",
            "views",
            "likes",
            "comments",
            "shares",
            "length"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        # Insert into Supabase
        response = supabase.table("reels").insert({
            "topic": data["topic"],
            "format": data["format"],
            "views": data["views"],
            "likes": data["likes"],
            "comments": data["comments"],
            "shares": data["shares"],
            "length": data["length"]
        }).execute()

        return jsonify({
            "message": "Reel added successfully",
            "data": response.data
        }), 201

    except Exception as e:
        error_msg = str(e)
        app.logger.error(f"Error adding reel: {error_msg}")
        # Temporary: return detailed error for debugging
        return jsonify({"error": "Internal server error", "details": error_msg}), 500


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes"))
