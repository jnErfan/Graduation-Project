# Render Deployment Guide

This Flask application is ready to deploy on Render.

## 1. Add a Procfile

The project already includes a `Procfile` in the root:

```text
web: gunicorn app:create_app()
```

This tells Render how to start the app.

## 2. Push your repository to GitHub

Render deploys directly from a Git repository.

1. Initialize Git if needed:
   ```bash
git init
git add .
git commit -m "Initial commit"
```
2. Push to GitHub:
   ```bash
git remote add origin <your-git-repo-url>
git push -u origin main
```

## 3. Create a new Web Service on Render

1. Go to https://render.com.
2. Sign in and select **New** > **Web Service**.
3. Connect your GitHub repository.
4. Choose the repository for this project.

## 4. Configure build and start commands

Use these settings:

- **Environment**: Python 3
- **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  gunicorn app:create_app()
  ```
- **Publish Directory**: leave blank

## 5. Set environment variables

Render needs database and secret key settings for production.

In the Render dashboard for your service, add:

- `SECRET_KEY` = `<a strong secret>`
- `DATABASE_URL` = `mysql://USER:PASSWORD@HOST:PORT/DATABASE`

If you do not use `DATABASE_URL`, configure instead:

- `MYSQL_HOST`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DB`
- `MYSQL_PORT`

Example:

```text
DATABASE_URL=mysql://render_user:password@aws-us-east-1-1.cleardb.net:3306/university_portal
SECRET_KEY=super-secret-key
```

## 6. Add a MySQL database service

Render does not provide MySQL directly in all plans, so you can use:

- ClearDB
- PlanetScale
- Amazon RDS
- Render External Database

Then connect your database by setting `DATABASE_URL` or the individual `MYSQL_*` vars.

## 7. Use `render.yaml` (recommended)

The project now includes a `render.yaml` file in the root. This is the recommended Render configuration for the service.

```yaml
services:
  - type: web
    name: university-portal
    env: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:create_app()
```

You should still configure secrets and database connection details in Render’s dashboard or environment settings.

## 8. Verify and deploy

After deployment, open the service URL provided by Render.

If the app fails to connect, confirm:

- `DATABASE_URL` is correct
- MySQL is accessible from Render
- the database schema is imported from `schema.sql`

## 9. Local development command

To run locally while developing:

```bash
source venv/bin/activate
python app.py
```

---

### Notes

- Your app already binds to `0.0.0.0` and reads `PORT` from the environment.
- The Flask app is configured in `app.py` using `create_app()`, so `gunicorn app:create_app()` is the correct Render start command.
