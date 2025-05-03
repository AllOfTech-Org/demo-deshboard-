import streamlit as st
from github import Github

from datetime import datetime
import os
import pandas as pd
import io
import traceback

# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Validate GitHub token
if not GITHUB_TOKEN:
    st.error("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
    st.stop()

# Name and folder settings
name = "Your_Company"
folder = name

# GitHub login with your personal token
try:
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    # Test the token by making a simple API call
    user.get_repos()
    st.success("GitHub token is valid and working!")
except Exception as e:
    st.error(f"GitHub token validation failed: {str(e)}")
    st.stop()

# Repository name
repo_name = "client-dashboards-data"

# Check if repository exists, if not create it
try:
    repo = user.get_repo(repo_name)
    st.success(f"Found existing repository: {repo_name}")
except Exception:
    if st.button("Create Repository"):
        try:
            repo = user.create_repo(
                repo_name,
                description="Client dashboards data repository",
                private=True
            )
            st.success(f"Created new repository: {repo_name}")
        except Exception as e:
            st.error(f"Failed to create repository: {str(e)}")
            st.stop()
    else:
        st.error(f"Repository '{repo_name}' not found. Click the button above to create it.")
        st.stop()

st.title(f"📤 {name} Upload Portal")

# Allow multiple file formats
uploaded_file = st.file_uploader("Upload your data file", type=['csv', 'xlsx', 'xls', 'txt'])

if uploaded_file and st.button("Upload to Dashboard"):
    try:
        # Get file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Read file based on extension
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        elif file_extension == 'txt':
            df = pd.read_csv(uploaded_file, sep='\t')
        else:
            st.error("Unsupported file format")
            st.stop()
            
        # Show data preview
        st.write("Data Preview (First 5 rows):")
        st.dataframe(df.head())
        
        # Show data info
        st.write("Data Information:")
        st.write(f"Total Rows: {len(df)}")
        st.write(f"Total Columns: {len(df.columns)}")
        
        # Convert the dataframe back to CSV string
        content = df.to_csv(index=False)
        
        # Calculate file size
        file_size_kb = len(content) / 1024
        st.write(f"File size: {file_size_kb:.2f} KB")
        
        # Get current date in the format "12 May 2025"
        current_date = datetime.now().strftime("%d %B %Y")
        
        # Get list of existing files to determine the next number
        try:
            contents = repo.get_contents(f"data/{folder}")
            existing_files = [file.name for file in contents if file.type == "file" and file.name.endswith('.csv')]
            
            # Extract numbers from existing files
            numbers = []
            for file in existing_files:
                try:
                    # Look for pattern "no X (" in the filename
                    num = int(file.split("no ")[1].split(" (")[0])
                    numbers.append(num)
                except:
                    continue
            
            # Get the next number in sequence
            next_number = max(numbers) + 1 if numbers else 1
        except Exception:
            next_number = 1
        
        # Create new filename
        new_filename = f"{name} no {next_number} ({current_date}).csv"
        upload_path = f"data/{folder}/{new_filename}"
        
        try:
            # First try to create the data directory if it doesn't exist
            try:
                repo.get_contents("data")
            except Exception:
                repo.create_file(
                    path="data/.gitkeep",
                    message="Create data directory",
                    content=""
                )
            
            # Create the client folder if it doesn't exist
            try:
                repo.get_contents(f"data/{folder}")
            except Exception:
                repo.create_file(
                    path=f"data/{folder}/.gitkeep",
                    message=f"Create {folder} directory",
                    content=""
                )
            
            # Create progress bar
            progress_text = "Uploading data..."
            progress_bar = st.progress(0)
            
            # Create the new file with detailed error handling
            try:
                repo.create_file(
                    path=upload_path,
                    message=f"New data upload on {datetime.now()} - {len(df)} rows",
                    content=content
                )
                progress_bar.progress(1.0)
                st.success(f"✅ File successfully uploaded with all {len(df)} rows as: {new_filename}")
            except Exception as e:
                st.error(f"GitHub API Error: {str(e)}")
                st.write("Detailed error information:")
                st.code(traceback.format_exc())
                st.stop()
            
            # Show list of all files in the directory
            try:
                contents = repo.get_contents(f"data/{folder}")
                if contents:
                    st.write("Previous uploads:")
                    for file in contents:
                        if file.type == "file" and file.name.endswith('.csv'):
                            st.write(f"- {file.name}")
            except Exception:
                pass
                
        except Exception as e:
            st.error(f"Failed to create file: {str(e)}")
            st.write("Detailed error information:")
            st.code(traceback.format_exc())
            st.stop()
            
    except Exception as e:
        st.error(f"Failed to upload file: {str(e)}")
        st.write("Detailed error information:")
        st.code(traceback.format_exc())