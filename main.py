from flask import Flask, request, jsonify
import json
import time
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def send_messenger_file(appstate, convo_tid, abuse_file_path, hater_name=None):
    print(f"Sending file to {convo_tid}: {abuse_file_path}")
    if hater_name:
        print(f"Hater name: {hater_name}")
    return {"success": True, "message": f"File sent to {convo_tid}"}

@app.route('/send_files', methods=['POST'])
def send_files():
    appstate = request.form.get('appstate')
    convo_tids = json.loads(request.form.get('convo_tids'))
    time_delay = float(request.form.get('time_delay'))
    hater_name = request.form.get('hater_name')
    abuse_file = request.files.get('abuse_file')

    if not abuse_file:
        return jsonify({"success": False, "message": "No file uploaded."})

    filename = abuse_file.filename
    abuse_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    abuse_file.save(abuse_file_path)

    if not appstate or not convo_tids:
        return jsonify({"success": False, "message": "Missing required parameters."})

    results = []
    for tid in convo_tids:
        time.sleep(time_delay)
        result = send_messenger_file(appstate, tid, abuse_file_path, hater_name)
        results.append(result)

    return jsonify({"success": True, "message": "Files sent.", "results": results})

if __name__ == '__main__':
    app.run(debug=True)
