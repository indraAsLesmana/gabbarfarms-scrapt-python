from dbconnection import DBconnection
from flask import Flask, Response, jsonify, g, request
from main import get_contenttab, get_hometab, search_product


app = Flask(__name__)
app.debug = True

USERNAME = 'indra'
PASSWORD = 'indra'

# Define a function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = DBconnection()  # Create a database connection if it doesn't exist in the context
    return g.db

# Close the database connection at the end of the request
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.__exit__(None, None, None)  # Call the __exit__ method to close the connection

# Function to request authentication
def authenticate():
    return Response('Authentication required', 401, {'WWW-Authenticate': 'Basic realm="Authentication Required"'})

# Define a decorator for authentication
def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    # Rename the decorated function to preserve the endpoint name
    decorated.__name__ = f.__name__
    return decorated

# Function to check authentication
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

@app.route('/api/search', methods=['GET'])
@requires_auth
def search_product_api():
    # Get the search key from the query parameters
    search_key = request.args.get('key')
    
    # Check if the result for this key exists in the database
    db = get_db()
    cached_result = db.get_cached_result(search_key.lower())

    if cached_result:
        # If the result is cached in the database, return it
        print("result from cached")
        return jsonify(cached_result)
    else:
        # Call the search_product function and store the results
        products = search_product(search_key)
        # Check if products were found
        if products:
            # Save the search key and its result to the database
            db.save_search_result(search_key, products)
            return jsonify(products)
        else:
            return jsonify({"message": "No products found for the given search key."}), 404

@app.route('/api/tab', methods=['GET'])
@requires_auth
def get_tab():
    db = get_db()
    cached_result = db.get_cached_result("tab")

    if cached_result:
        # If the result is cached in the database, return it
        print("result from cached")
        return jsonify(cached_result)
    else:
        # Call the search_product function and store the results
        products = get_hometab()
        # Check if products were found
        if products:
            # Save the search key and its result to the database
            db.save_tab_result(products)
            return jsonify(products)
        else:
            return jsonify({"message": "No products found for the given search key."}), 404

@app.route('/api/tab_content', methods=['GET'])
@requires_auth
def get_tabcontent():
    # Get the search key from the query parameters
    search_key = request.args.get('key')
    
    # Check if the result for this key exists in the database
    db = get_db()
    cached_result = db.get_cached_result(search_key.lower())

    if cached_result:
        # If the result is cached in the database, return it
        print("result from cached")
        return jsonify(cached_result)
    else:
        # Call the search_product function and store the results
        products = get_contenttab(search_key)
        # Check if products were found
        if products:
            # Save the search key and its result to the database
            db.save_search_result(search_key, products)
            return jsonify(products)
        else:
            return jsonify({"message": "No products found for the given search key."}), 404

@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)