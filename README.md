<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Streamlit Deployment Guide</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%);
            color: #f0f2f6;
            line-height: 1.6;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(24, 28, 39, 0.9);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        }
        
        header {
            background: linear-gradient(90deg, #ff4b4b 0%, #ff7c7c 100%);
            padding: 30px 20px;
            text-align: center;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .card {
            background: rgba(38, 43, 58, 0.6);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 25px;
            border-left: 4px solid #ff4b4b;
        }
        
        h2 {
            color: #ff7c7c;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        h2 i {
            margin-right: 10px;
        }
        
        p {
            margin-bottom: 15px;
        }
        
        ul, ol {
            margin-left: 20px;
            margin-bottom: 20px;
        }
        
        li {
            margin-bottom: 10px;
        }
        
        code {
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
        
        pre {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            line-height: 1.4;
        }
        
        .note {
            background: rgba(255, 215, 0, 0.1);
            border-left: 4px solid gold;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        
        .troubleshooting {
            background: rgba(255, 75, 75, 0.1);
            border-left: 4px solid #ff4b4b;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        
        .success {
            background: rgba(75, 255, 100, 0.1);
            border-left: 4px solid #4bff64;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        
        .platforms {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px 0;
        }
        
        .platform {
            flex: 1;
            min-width: 200px;
            background: rgba(38, 43, 58, 0.8);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .platform h3 {
            color: #ff7c7c;
            margin-bottom: 10px;
        }
        
        footer {
            text-align: center;
            padding: 20px;
            background: rgba(24, 28, 39, 1);
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .platforms {
                flex-direction: column;
            }
            
            h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Streamlit App Deployment Guide</h1>
            <p class="subtitle">Step-by-step instructions to deploy your Streamlit application</p>
        </header>
        
        <div class="content">
            <div class="card">
                <h2>Understanding the Problem</h2>
                <p>When you see a "file not found" error with Streamlit, it's typically because:</p>
                <ul>
                    <li>Your app is looking for a file in the wrong location</li>
                    <li>The working directory is different than expected</li>
                    <li>File paths are hardcoded and don't work in deployment</li>
                    <li>Required files aren't included in your deployment</li>
                </ul>
            </div>
            
            <div class="card">
                <h2>Step 1: Fix File Path Issues</h2>
                <p>Always use relative paths and the <code>__file__</code> attribute to construct paths correctly:</p>
                <pre>
import os
import streamlit as st

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute path to your data file
data_path = os.path.join(script_dir, 'data', 'your_data.csv')

# Use this path to load your data
try:
    df = pd.read_csv(data_path)
    st.write("Data loaded successfully!")
except FileNotFoundError:
    st.error("Data file not found. Please check the file path.")
                </pre>
                <div class="note">
                    <p><strong>Note:</strong> Avoid hardcoding absolute paths like <code>C:/Users/Name/Project/data.csv</code> as these won't work when deployed.</p>
                </div>
            </div>
            
            <div class="card">
                <h2>Step 2: Prepare Your App for Deployment</h2>
                <p>Before deploying, make sure your project is well-organized:</p>
                <ol>
                    <li>Place all required data files in a folder within your project</li>
                    <li>Create a <code>requirements.txt</code> file with all dependencies</li>
                    <li>Test your app locally to ensure it works with relative paths</li>
                    <li>Make sure you're not using any localhost/127.0.0.1 references</li>
                </ol>
                
                <p>Example requirements.txt:</p>
                <pre>
streamlit==1.22.0
pandas==1.5.3
numpy==1.24.3
plotly==5.13.1
                </pre>
            </div>
            
            <div class="card">
                <h2>Step 3: Choose a Deployment Platform</h2>
                <p>Streamlit apps can be deployed on several platforms:</p>
                
                <div class="platforms">
                    <div class="platform">
                        <h3>Streamlit Community Cloud</h3>
                        <p>Official hosting by Streamlit</p>
                        <p>Free for public apps</p>
                    </div>
                    
                    <div class="platform">
                        <h3>Heroku</h3>
                        <p>Platform as a Service</p>
                        <p>Free tier available</p>
                    </div>
                    
                    <div class="platform">
                        <h3>AWS/Azure/GCP</h3>
                        <p>Cloud providers</p>
                        <p>More configuration needed</p>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>Step 4: Deploy to Streamlit Community Cloud</h2>
                <ol>
                    <li>Push your code to a GitHub repository</li>
                    <li>Go to <a href="https://share.streamlit.io/" style="color: #ff7c7c;">share.streamlit.io</a></li>
                    <li>Sign in with your GitHub account</li>
                    <li>Click "New app" and select your repository, branch, and main file</li>
                    <li>Advanced settings: Add your Python version if needed</li>
                    <li>Click "Deploy" and wait for the process to complete</li>
                </ol>
                
                <div class="success">
                    <p><strong>Success:</strong> Your app will be available at <code>https://your-app-name.streamlit.app</code></p>
                </div>
            </div>
            
            <div class="card">
                <h2>Troubleshooting Common Issues</h2>
                <div class="troubleshooting">
                    <p><strong>ModuleNotFoundError:</strong> Add missing packages to your requirements.txt</p>
                    <p><strong>FileNotFoundError:</strong> Use the path construction method shown in Step 1</p>
                    <p><strong>App crashes on launch:</strong> Check your requirements.txt for version conflicts</p>
                    <p><strong>App deploys but shows error:</strong> Check the logs in your deployment platform</p>
                </div>
                
                <p>For advanced debugging, you can add debug information to your app:</p>
                <pre>
import os
st.sidebar.write("Current working directory:", os.getcwd())
st.sidebar.write("Files in directory:", os.listdir())
# Remember to remove these after debugging
                </pre>
            </div>
        </div>
        
        <footer>
            <p>Need more help? Check out the <a href="https://docs.streamlit.io/" style="color: #ff7c7c;">Streamlit Documentation</a></p>
            <p>© 2023 Streamlit Deployment Guide</p>
        </footer>
    </div>

    <script>
        // Simple text animation for headers
        document.addEventListener('DOMContentLoaded', function() {
            const headers = document.querySelectorAll('h2');
            headers.forEach(header => {
                header.innerHTML = '<i>▶</i> ' + header.textContent;
                header.addEventListener('click', function() {
                    const content = this.nextElementSibling;
                    while(content && content.classList && !content.classList.contains('card')) {
                        if (content.style.display === 'none') {
                            content.style.display = 'block';
                            this.querySelector('i').textContent = '▶';
                        } else {
                            content.style.display = 'none';
                            this.querySelector('i').textContent = '▼';
                        }
                        content = content.nextElementSibling;
                    }
                });
            });
        });
    </script>
</body>
</html>
