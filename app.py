import os
from os import path
from pathlib import Path
from flask import Flask, render_template
from flask_frozen import Freezer

template_folder = path.abspath('./wiki')

app = Flask(__name__, template_folder=template_folder)

# --- GITHUB PAGES ADJUSTMENTS ---
# 1. Set the Base URL to your GitHub Pages address
# Replace 'carasj' and 'WikiSandbox' with your actual username/repo name
app.config['FREEZER_BASE_URL'] = "https://carasj.github.io/"

# 2. GitHub Actions usually looks for a 'build' folder, not 'public'
app.config['FREEZER_DESTINATION'] = 'build'

app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
freezer = Freezer(app)

# 3. Add a simple freeze function so you can run 'python freeze.py'
def manual_freeze():
    freezer.freeze()

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/<page>.html') # Add .html here so the Freezer knows the filename
def pages(page):
    # This keeps the source files in the 'pages' folder 
    # but outputs them to the top level of 'build/'
    return render_template('pages/' + page.lower() + '.html')

# Main Function
if __name__ == "__main__":
    # Check if we are running inside a GitHub Action
    if os.environ.get('GITHUB_ACTIONS'):
        print("GitHub Action detected: Freezing the website...")
        freezer.freeze()
    else:
        print("Local environment detected: Starting development server...")
        app.run(port=8080, debug=True)