import flask
from flask import request
import mysql.connector
import cohere
import re
from termcolor import colored
import json
from utils import CustomJSONEncoder
from TextToSql import Text2SQL
from faissStore import FaissStore
from DataToChart import Data2Chart


co = cohere.Client(
    api_key="fgEMvVbRmXBgaiqhbhcSsPYOWVKweF0Twl4qH4FO",
)

app = flask.Flask(__name__)
schema = {}

MySQL_HOST = None
MySQL_USER = None
MySQL_PASSWORD = None
MySQL_DATABASE = None
db = None


def get_schema(host, user, password, database):
    """
    The function `get_schema` retrieves the schema of a database by connecting to it, querying for
    tables and their columns, and returning the schema as a dictionary.
    
    :param host: The `host` parameter in the `get_schema` function refers to the hostname or IP address
    of the database server you want to connect to. This is where the database is hosted and can be
    provided as a string in the function call
    :param user: The `get_schema` function you provided is a Python function that connects to a MySQL
    database and retrieves the schema information for all tables in the specified database. It fetches
    the list of tables and then iterates over each table to get the columns present in each table
    :param password: It seems like you were about to ask for clarification on the `password` parameter
    in the `get_schema` function. The `password` parameter in this function is used to provide the
    password required to connect to the database specified by the `host`, `user`, and `database`
    parameters. This
    :param database: The `get_schema` function you provided is a Python function that connects to a
    MySQL database using the given host, user, password, and database parameters. It retrieves the
    schema information for all tables in the specified database
    :return: The `get_schema` function returns a dictionary where the keys are table names and the
    values are lists of column names for each table in the specified database.
    """
    # Connect to the database
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    cursor = conn.cursor()
    
    # Query to get the list of tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    schema = {}
    
    # Iterate over each table to get its columns
    for (table_name,) in tables:
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = cursor.fetchall()
        schema[table_name] = [column[0] for column in columns]
    
    cursor.close()
    conn.close()
    
    return schema

#  Function to cache the schema
faiss_store = FaissStore(dir='faiss_store', name='schema_store', cohere_client=co)

def cache_schema(schemas):
    """
    The function `cache_schema` writes the input `schemas` to a Faiss store and prints a success
    message.
    
    :param schemas: The `schemas` parameter in the `cache_schema` function likely refers to a data
    structure or collection of schemas that are being passed to the function for caching. The function
    `faiss_store.write(schemas)` is used to write these schemas to some kind of storage, possibly a
    Faiss store,
    """
    faiss_store.write(schemas)
    print("Schema cached successfully.")

@app.route('/')
def index():
    """
    The `index` function returns a rendered template for MySQL configuration in Flask.
    :return: The `index()` function is returning the rendered template for 'chat-interface.html'.
    """
    return flask.render_template('chat-interface.html')

@app.route('/submit-form', methods=['POST'])
def handle_form():
    """
    The `handle_form` function processes form data or JSON data to configure a MySQL database connection
    and retrieve table information.
    :return: The `handle_form()` function is designed to handle form submissions and JSON data.
    Depending on the request method and data received, it returns different JSON responses:
    """

    global MySQL_DATABASE, MySQL_HOST, MySQL_USER, MySQL_PASSWORD, db, tables


    if request.method == 'POST':
        if request.form:
            # Process form data here



            return flask.jsonify(message="Form submitted"), 200
        elif request.json:
            MySQL_HOST = request.json['host']
            MySQL_USER = request.json['username']
            MySQL_PASSWORD = request.json['password']
            MySQL_DATABASE = request.json['database']
            db = mysql.connector.connect(
                host=MySQL_HOST,
                user=MySQL_USER,
                password=MySQL_PASSWORD,
                database=MySQL_DATABASE
            )
            mycursor = db.cursor()
            mycursor.execute("SHOW TABLES")

            
            tables = mycursor.fetchall()

            schema = get_schema(MySQL_HOST, MySQL_USER, MySQL_PASSWORD, MySQL_DATABASE)
            print(colored("Schema fetched successfully.", 'green'))
            cache_schema(schema)

            return flask.jsonify(message="JSON submitted"), 200
        else:   
            # No form or JSON data could be found
            return flask.jsonify(message="No data submitted"), 400
    else:
        # Method not allowed
        return flask.jsonify(message="Databse not configured"), 405
@app.route('/chat')
# tempalts/chat.html
def chat():
    return flask.render_template('ai-chat.html')
# get chat message from frontend

@app.route('/chat-message', methods=['POST'])
def chat_response():
    """
    This Python function processes a POST request, generates an SQL query based on the input message,
    executes the query on a database, fetches the result, generates charts based on the result, and
    returns the data in JSON format.
    :return: The `chat_response` function returns a JSON response containing the SQL message, query
    result, and generated charts data. If the request method is POST and a database is configured, it
    processes the incoming JSON message, generates an SQL query, executes the query, fetches the result,
    generates charts based on the result, and returns a JSON response with the SQL message, query
    result, and charts data.
    """
    global schema
    if request.method == 'POST' and db!=None:
        if request.json:
            message = request.json['messagePerson']

            relevant_tables = []
            relevant_tables = faiss_store.search(message)
            text2sql = Text2SQL(schema=schema, cohere_client=co)
            sql = text2sql.gen_sql(database_schema=schema, requirement=message, relevant_tables=relevant_tables)


            if sql:
                sql_query = None
                mycursor = db.cursor()
                
                pattern = r"```sql\s+(.*?)\s+```"
                match = re.search(pattern, sql, re.DOTALL)

                if match:
                    # Extract the SQL query (group 1 of the match)
                    sql_query = match.group(1)
                    print("Extracted SQL query:", sql_query)
                else:
                    print("SQL query not found in the string.")


                result = []
                if sql_query != None:
                    try:
                        mycursor.execute(sql_query)
                        result = mycursor.fetchall()
                        print("Result fetched successfully.")
                    except Exception as e:
                        print("Error in fetching result:", e)
                        result = []
            else:
                print("Error in generating SQL. Please try again.")

            c = Data2Chart(cohere_client=co)
            charts = c.gen_chart(message, result, "Function")
            response_data = {
            "message": sql,
            "result": result,
            "charts": charts.generations[0].text.strip().replace('\\', '').replace('\\n', '').replace('\n', '')  # Include charts data in the response
        }   
            json_data = json.dumps(response_data, indent=4, cls=CustomJSONEncoder)

            return json_data, 200
        else:
            # No form or JSON data could be found
            return flask.jsonify(message="No data submitted"), 400
    else:
        # Method not allowed
        return flask.jsonify(message="No database configured"), 405
@app.route('/schema', methods=['GET'])
def get_schema_user():
    """
    The function `get_schema_user` retrieves the schema information of tables in a MySQL database and
    returns it as a JSON response.
    :return: The function `get_schema_user` is returning a JSON response containing the schema of the
    database tables. The schema includes the list of tables and their respective columns. The response
    is returned with a status code of 200 if successful, or a message indicating that no database is
    configured with a status code of 400 if there is no database connection.
    """
    # DatabaseError if not connected to the database
    if db == None:
        return flask.jsonify(message="No database configured"), 400
    else:
        
        conn = mysql.connector.connect(
            host=MySQL_HOST,
            user=MySQL_USER,
            password=MySQL_PASSWORD,
            database=MySQL_DATABASE

            )
        
        cursor = conn.cursor()
        
        # Query to get the list of tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        schema = {}
        
        # Iterate over each table to get its columns
        for (table_name,) in tables:
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = cursor.fetchall()
            schema[table_name] = [column[0] for column in columns]
        
        cursor.close()
        conn.close()
        
        return flask.jsonify(schema), 200


if __name__ == '__main__':
    app.run(debug=True)