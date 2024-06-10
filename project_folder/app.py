from flask import Flask, request, send_file, render_template, redirect, url_for
import os
import codecs

app = Flask(__name__)

def convertir_archivo(input_file, output_file):
    if not os.path.isfile(input_file):
        return "Error: El archivo no se encuentra."

    with codecs.open(input_file, 'r', 'utf-8-sig') as infile:
        lines = infile.readlines()

    output_lines = []
    count = 1
    for i, line in enumerate(lines):
        line = line.strip()
        if "Pulse INTRO para continuar:" in line:
            continue
        
        parts = line.split()
        x_value = None
        y_value = None
        
        for part in parts:
            if part.startswith("X="):
                try:
                    x_value = float(part.split('=')[1])
                except ValueError:
                    break
            elif part.startswith("Y="):
                try:
                    y_value = float(part.split('=')[1])
                except ValueError:
                    break
        
        if x_value is not None and y_value is not None:
            formatted_x = f"{x_value:.3f}"
            formatted_y = f"{y_value:.3f}"
            output_line = f"REP{count},{formatted_x},{formatted_y}"
            output_lines.append(output_line)
            count += 1
    
    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(output_lines))

    return output_file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    input_path = os.path.join("input", file.filename)
    output_path = os.path.join("output", "converted_" + file.filename)
    
    file.save(input_path)
    
    result = convertir_archivo(input_path, output_path)
    
    if result.startswith("Error"):
        return result
    
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    app.run(debug=True)