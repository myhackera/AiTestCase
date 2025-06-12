from flask import Flask, render_template, request, send_file, jsonify
import os
import sys

# Add parent directory to path to import from AI
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from main import TestCaseApp

app = Flask(__name__)
test_case_app = TestCaseApp()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_test_cases():
    try:
        user_story = request.form.get('user_story')
        custom_prompt = request.form.get('prompt')
        
        if not user_story:
            return jsonify({'error': 'User story is required'}), 400

        # Use custom prompt if provided
        if custom_prompt:
            # Ensure the prompt includes the user_story placeholder
            if '{user_story}' not in custom_prompt:
                custom_prompt = custom_prompt + "\n\n{user_story}"
            test_case_app.parser.test_case_prompt = custom_prompt
            
        # Generate test cases and get file path
        output_path = test_case_app.generate_and_export(user_story)
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name='test_cases.xlsx'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 