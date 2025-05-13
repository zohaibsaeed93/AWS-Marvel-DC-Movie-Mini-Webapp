from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- DATABASE CONFIGURATION ---
# Replace with your actual RDS credentials
# Consider using environment variables for security
DB_NAME = "db_zohaib"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "db-zohaib1t.clyucs4e44b4.ap-northeast-2.rds.amazonaws.com" # e.g., your-rds-instance.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com
DB_PORT = "5432" # Default PostgreSQL port

TABLE_NAME = "tbl_zohaib_marvel_dc"

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        # In a real app, you might want to handle this more gracefully
        return None

@app.route('/data', methods=['GET'])
def get_data():
    """Fetches all data from the specified table."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        # Adjust column names if they differ slightly in your actual table
        cur.execute(f"SELECT id, movie, \"Year\", genre, runtime, description, imdb_score FROM {TABLE_NAME}")
        # Fetch column names
        colnames = [desc[0] for desc in cur.description]
        # Fetch all rows and convert them to dictionaries
        rows = cur.fetchall()
        data = [dict(zip(colnames, row)) for row in rows]
        cur.close()
        conn.close()
        return jsonify(data)
    except psycopg2.Error as e:
        print(f"Error fetching data: {e}")
        if conn:
            conn.rollback() # Rollback in case of error
            cur.close()
            conn.close()
        return jsonify({"error": f"Failed to fetch data: {e}"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


@app.route('/add', methods=['POST'])
def add_data():
    """Adds a new movie record to the table."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()
        # Basic validation (you might want more robust validation)
        required_fields = ['id', 'movie', 'Year', 'genre', 'runtime', 'description', 'imdb_score']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        cur = conn.cursor()
        # Ensure correct quoting for column names like "Year" if needed
        sql = f"""
            INSERT INTO {TABLE_NAME} (id, movie, "Year", genre, runtime, description, imdb_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (
            data['id'], data['movie'], data['Year'], data['genre'],
            data['runtime'], data['description'], data['imdb_score']
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data added successfully"}), 201
    except psycopg2.Error as e:
        print(f"Error adding data: {e}")
        if conn:
            conn.rollback() # Rollback in case of error
            cur.close()
            conn.close()
        return jsonify({"error": f"Failed to add data: {e}"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


@app.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    """Deletes a record from the table based on its ID."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        sql = f"DELETE FROM {TABLE_NAME} WHERE id = %s"
        cur.execute(sql, (item_id,))

        # Check if any row was actually deleted
        if cur.rowcount == 0:
            conn.rollback() # Rollback if ID not found
            cur.close()
            conn.close()
            return jsonify({"error": f"Item with ID {item_id} not found"}), 404

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": f"Data with ID {item_id} deleted successfully"}), 200
    except psycopg2.Error as e:
        print(f"Error deleting data: {e}")
        if conn:
            conn.rollback() # Rollback in case of error
            cur.close()
            conn.close()
        return jsonify({"error": f"Failed to delete data: {e}"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


if __name__ == "__main__":
    # Ensure the port (e.g., 5000) is open in your EC2 security group
    # Run on 0.0.0.0 to be accessible from the EC2 instance's public IP
    # Set debug=False for production environments
    app.run(host='0.0.0.0', port=5000, debug=True)
