# Deployment Guide for HubSpot Ticket Parser

## Quick Start with Render

### 1. Prepare Your Repository

1. **Create a private GitHub repository**
   ```bash
   # Initialize git if not already done
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit: HubSpot Ticket Parser"
   
   # Add your GitHub remote (replace with your repo URL)
   git remote add origin https://github.com/yourusername/hubspot-ticket-parser.git
   
   # Push to GitHub
   git push -u origin main
   ```

### 2. Deploy to Render

1. **Go to [Render Dashboard](https://dashboard.render.com)**

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your private repository

3. **Configure the Service**
   - **Name**: `hubspot-ticket-parser`
   - **Region**: Oregon (or your preferred region)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Plan**: Free (or paid for better performance)

4. **Environment Variables**
   - Click "Advanced"
   - Add environment variable:
     - Key: `SECRET_KEY`
     - Value: Click "Generate" to auto-generate

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build and deployment (5-10 minutes)

### 3. Access Your App

Once deployed, you'll get a URL like:
```
https://hubspot-ticket-parser.onrender.com
```

## Alternative: Manual Environment Variables

If you prefer to set your own secret key:

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

Use the output as your `SECRET_KEY` environment variable.

## Health Check

After deployment, test these URLs:

- **Main App**: `https://your-app.onrender.com/`
- **Health Check**: `curl -I https://your-app.onrender.com/`

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` is in root directory
   - Verify Python version compatibility
   - Check Render build logs

2. **App Won't Start**
   - Ensure `app.py` is in root directory
   - Check start command: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - Review application logs in Render dashboard

3. **Import Errors**
   - Verify all dependencies are in `requirements.txt`
   - Check that `utils/` directory has `__init__.py`

### Render Logs

To debug issues:
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. Review build and runtime logs

## Production Considerations

### Security
- ✅ Secret key is environment-based
- ✅ No data persistence (all in memory)
- ✅ CSRF protection via Flask sessions
- ✅ Input validation and sanitization

### Performance
- Flask app handles single requests synchronously
- For high traffic, consider upgrading Render plan
- Memory usage scales with data size (all in-memory processing)

### Monitoring
- Use Render's built-in monitoring
- Check application logs regularly
- Monitor memory usage for large datasets

## Local Development

For local testing before deployment:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Test in browser
open http://localhost:5000
```

## Updates

To update the deployed app:

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push origin main
```

Render will automatically rebuild and redeploy.

---

**Security Note**: This guide assumes a private repository. Never commit sensitive data or credentials to version control.
