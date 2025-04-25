import streamlit as st
from github import Github
from datetime import datetime
import os
import pandas as pd
import io

# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Name and folder settings
name = "Mr.okey life data"
folder = name

# GitHub login with your personal token
g = Github(GITHUB_TOKEN)
user = g.get_user()

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
            
            # Create the new file
            repo.create_file(
                path=upload_path,
                message=f"New data upload on {datetime.now()}",
                content=content
            )
            
            st.success(f"✅ File successfully uploaded as: {new_filename}")
            
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
            st.stop()
            
    except Exception as e:
        st.error(f"Failed to upload file: {str(e)}")
