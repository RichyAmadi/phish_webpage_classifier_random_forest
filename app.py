import os
import pickle
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from model_utils import CLASS_LABELS, URL_FEATURE_COLUMNS, extract_url_features, validate_url

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / 'phishing_model.pkl'

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MODEL_LOADED'] = False


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f'Model file not found: {MODEL_PATH}. Run train_model.py first.'
        )
    with MODEL_PATH.open('rb') as file:
        return pickle.load(file)

try:
    model = load_model()
    app.config['MODEL_LOADED'] = True
except FileNotFoundError:
    model = None
    app.logger.warning('Model file not found. The app will start but the API is unavailable until the model is added.')


@app.route('/')
def home():
    return render_template('index.html', model_loaded=app.config['MODEL_LOADED'])


@app.route('/api/predict', methods=['POST'])
def predict():
    if not app.config['MODEL_LOADED'] or model is None:
        return jsonify({'error': 'Model is not available. Please add phishing_model.pkl and restart the app.'}), 503

    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({'error': 'Please provide a URL in JSON body with key "url".'}), 400

    url = str(data['url']).strip()
    if not url:
        return jsonify({'error': 'URL cannot be empty.'}), 400

    if not validate_url(url):
        return jsonify({'error': 'Invalid URL format. Please provide a valid http or https URL.'}), 422

    try:
        features = extract_url_features(url)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 422

    vector = [features[name] for name in URL_FEATURE_COLUMNS]
    prediction = model.predict([vector])[0]

    result = {
        'url': url,
        'prediction': int(prediction),
        'label': CLASS_LABELS.get(prediction, 'unknown'),
    }

    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba([vector])[0]
        confidence = float(max(proba))
        result['confidence'] = round(confidence, 4)

    return jsonify(result)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
