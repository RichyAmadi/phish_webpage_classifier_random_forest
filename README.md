# Phishing Webpage Classifier

This repository contains a Flask web application that classifies URLs as either `phishing` or `legitimate` using a trained RandomForest model.

## Run locally

1. Install dependencies:
   ```bash
   py -m pip install -r requirements.txt
   ```

2. Start the app:
   ```bash
   py app.py
   ```

3. Open in browser:
   ```text
   http://127.0.0.1:5000
   ```

## Deploy as a standalone site

### Option 1: Deploy with Docker

Build the Docker image:
```bash
docker build -t phishing-webpage-classifier .
```

Run the container:
```bash
docker run -p 5000:5000 phishing-webpage-classifier
```

Then visit:
```text
http://127.0.0.1:5000
```

### Option 2: Deploy to a platform using Procfile

This repo includes a `Procfile` so it can be deployed to services like Heroku, Railway, or Render.

- Add the repo to the service
- Set the build command to install dependencies
- The platform will use `Procfile` to start the web process

### Push this repo to GitHub from Windows

1. Create a new empty repository on GitHub.
2. Run the helper script in PowerShell:
   ```powershell
   .\push_to_github.ps1
   ```
3. Paste the repository URL when prompted.

If you prefer manual commands:
```powershell
git init
git add -A
git commit -m 'Initial commit'
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git branch -M main
git push -u origin main
```

### Deploy with Railway CLI

If you want to deploy directly via Railway CLI, first install it from https://railway.app/cli.

Then run:
```powershell
.\deploy_to_railway.ps1
```

If you prefer the raw commands:
```powershell
railway login
railway init --name phishing-webpage-classifier
railway up
```

If Railway cannot detect the project automatically, use the start command:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
```

### Option 3: One-click deploy to Render

### Option 3: One-click deploy to Render

If your repository is hosted on GitHub, you can deploy directly using Render.

1. Push this repository to GitHub.
2. Open Render and click **New +** → **Web Service**.
3. Connect your GitHub account and select this repository.
4. Use the default build command:
   ```bash
   pip install -r requirements.txt
   ```
5. Set the start command to:
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
   ```
6. Deploy the service.

If you want a GitHub button, use this template and replace `YOUR-GITHUB-USER/REPO`:

```markdown
[![Deploy to Render](https://github.com/render-examples/deploy-buttons/raw/master/buttons/deploy-button-blue.svg)](https://render.com/deploy?repo=https://github.com/YOUR-GITHUB-USER/REPO)
```

### Option 4: One-click deploy to Railway

Railway also supports quick GitHub deployment.

1. Push this repository to GitHub.
2. Sign in to Railway and click **Create Project**.
3. Choose **Deploy from GitHub**.
4. Select the repository and connect it.
5. Railway will detect the Flask app.
6. If needed, set the start command to:
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
   ```

Railway automatically provisions a URL after deployment.

### Deployment support files

This repository includes platform configuration files to make setup automatic:

- `render.yaml` — Render service definition
- `railway.json` — Railway service definition

These files can be used by Render and Railway to detect the app settings and start command automatically.

### Notes

- `phishing_model.pkl` is included in the repository, so the app is ready to serve immediately.
- If you want to redeploy with a retrained model, run:
  ```bash
  py train_model.py
  ```
