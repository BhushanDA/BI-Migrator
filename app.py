from flask import Flask, request, jsonify, send_file
import openai
import os

app = Flask(__name__)

# Function to convert scripts between languages using OpenAI API
def convert_script(source_script, source_language, target_language, api_key):
    # Set the OpenAI API key from the form data
    openai.api_key = api_key

    prompt = (
        f"Convert the following {source_language} script into {target_language} syntax, "
        f"return only the equivalent expression, without any explanation:\n\n"
        f"{source_script}\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant that helps convert between different scripting languages."},
                      {"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.3,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/convert_scripts', methods=['POST'])
def convert_scripts():
    # Get API key from the form
    api_key = request.form['api_key']
    
    # Ensure API key is provided
    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    # Get other form data
    source_language = request.form['source_language']
    target_language = request.form['target_language']
    uploaded_file = request.files['file']

    if uploaded_file:
        # Read and process the uploaded file
        file_content = uploaded_file.read().decode('utf-8')
        scripts = file_content.splitlines()

        # Convert scripts using OpenAI API
        converted_scripts = [convert_script(script, source_language, target_language, api_key) for script in scripts]

        output_filename = 'converted_scripts.txt'
        with open(output_filename, 'w') as output_file:
            for script in converted_scripts:
                output_file.write(script + "\n")

        return send_file(output_filename, as_attachment=True)
    else:
        return jsonify({"error": "No file uploaded"}), 400

if __name__ == '__main__':
    app.run(debug=True)

