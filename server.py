from flask import Flask, request, jsonify, render_template,Response
from flask import request
from flask_cors import CORS,cross_origin
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import subprocess
import keyword
import builtins
import inspect
import pyautogui as webo
import ast
import os
import pylint.lint
import tempfile
import pyflakes.api
import io
import pyflakes.reporter


    
def click_image(path):    
    pass
        
def double_click_image(path):    
    pass

def screenshot():    
    pass


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"])




@app.route('/', methods=['GET', 'POST'])
def test_endpoint():
    return render_template("index.html")



@app.route('/runserver', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def run_server():
    if request.is_json:
        try:
            python_code = request.json.get('code')
            compiled_code = compile(python_code, "<string>", "exec")
            

            # If the code execution completes without errors, return success response
            return jsonify({'result': 'Code executed successfully.'}), 200 

        except SyntaxError as se:
            # Handle syntax errors
            return jsonify({'error': f'Syntax Error: {se.msg}, line {se.lineno}'}), 400

        except NameError as ne:
            # Handle name errors
            return jsonify({'error': f'Name Error: {ne}'}), 400

        except Exception as e:
            # Handle other exceptions
            return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

    else:
        return jsonify({'error': 'Unsupported Media Type - Content-Type must be application/json'}), 415


def get_python_functions():
    functions = []

    # Get built-in functions
    functions.extend(dir(builtins))

    # Remove duplicates and keywords
    functions = list(set(functions) - set(keyword.kwlist))
    functions.extend(additional_suggestions)
    return functions

# Function to get information about a specific function
def get_function_info(function_name):
    try:
        function = eval(function_name)
        docstring = inspect.getdoc(function)
        parameters = [param.name for param in inspect.signature(function).parameters.values()]
        first_line_docstring = docstring.split('\n')[0] if docstring else ''
 
        return {
            "label": function_name,
            "kind": "Method",  # Adjust this based on your needs
            "insertText": f"{function_name}({', '.join(parameters)})",
            "documentation": first_line_docstring,
            "parameters": parameters
        }
    except:
        return None

# Manually defined additional suggestions
additional_suggestions = [
    "for", "while", "if", "else", "elif", "def", "class", "try", "except",
    "import", "from", "return", "True", "False", "None" , "webo"
]

# Combine suggestions from built-ins with manually defined suggestions
all_suggestions = get_python_functions()

# Endpoint to provide autocompletion suggestions
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    suggestions = [get_function_info(name) for name in all_suggestions if get_function_info(name)]
    suggestions = [s for s in suggestions if s is not None]  # Filter out None values
    return jsonify({"suggestions": suggestions})

if __name__ == '__main__':
    app.run(debug=True,port = 7734)


