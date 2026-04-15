import csv
import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from model_utils import CLASS_MAP, URL_FEATURE_COLUMNS, extract_url_features

DATA_PATH = Path('webpage_phishing_detection_dataset.csv')
MODEL_PATH = Path('phishing_model.pkl')


def load_training_data():
    X = []
    y = []
    with DATA_PATH.open(encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row.get('url', '').strip()
            label = row.get('status', '').strip().lower()
            if not url or label not in CLASS_MAP:
                continue
            features = extract_url_features(url)
            X.append([features[name] for name in URL_FEATURE_COLUMNS])
            y.append(CLASS_MAP[label])
    return X, y


def train():
    X, y = load_training_data()
    if not X:
        raise RuntimeError('No training data loaded from CSV file.')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True
    )
    model = RandomForestClassifier(n_estimators=350, random_state=42)
    model.fit(X_train, y_train)
    print('Training accuracy:', model.score(X_train, y_train))
    print('Test accuracy:', model.score(X_test, y_test))
    with MODEL_PATH.open('wb') as file:
        pickle.dump(model, file)
    print(f'Model saved to {MODEL_PATH}')


if __name__ == '__main__':
    train()
