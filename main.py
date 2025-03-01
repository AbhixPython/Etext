from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_token', methods=['POST'])
def check_token():
    data = request.get_json()
    access_token = data.get('access_token')

    if not access_token:
        return jsonify({'error': 'Access token is required'}), 400

    try:
        url = f"https://graph.facebook.com/me?fields=id,name,picture&access_token={access_token}"
        response = requests.get(url)
        response.raise_for_status()
        user_data = response.json()

        return jsonify({
            'name': user_data['name'],
            'uid': user_data['id'],
            'profile_picture': user_data['picture']['data']['url']
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Invalid token or network error: {e}'}), 400
    except KeyError:
        return jsonify({'error': 'Invalid token or insufficient permissions.'}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
