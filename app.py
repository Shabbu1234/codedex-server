import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'cpp').lower()

    if not code:
        return jsonify({'output': 'Error: Koi code nahi mila.'}), 400

    filename = ""
    executable = ""
    compile_command = []
    run_command = []

    if language == 'c++':
        filename = "temp.cpp"
        executable = "temp_cpp.out" # Linux (Render) .exe nahi use karta
        compile_command = ['g++', filename, '-o', executable]
        run_command = [executable]
    elif language == 'c':
        filename = "temp.c"
        executable = "temp_c.out"
        compile_command = ['gcc', filename, '-o', executable]
        run_command = [executable]
    else:
        return jsonify({'output': f"Error: Language '{language}' support nahi karti."}), 400

    output_text = ""
    error_text = ""

    try:
        with open(filename, 'w') as f:
            f.write(code)

        compile_process = subprocess.run(compile_command, capture_output=True, text=True, timeout=10)

        if compile_process.returncode == 0:
            run_process = subprocess.run(run_command, capture_output=True, text=True, timeout=10)
            output_text = run_process.stdout
            error_text = run_process.stderr
        else:
            error_text = compile_process.stderr

    except Exception as e:
        error_text = str(e)

    finally:
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(executable):
            os.remove(executable)

    if error_text:
        return jsonify({'output': error_text})
    else:
        return jsonify({'output': output_text})

# Render ke liye
if __name__ == '__main__':
    # Render 10000 port expect karta hai
    app.run(host='0.0.0.0', port=10000)