import streamlit as st
from github import Github
from datetime import datetime
import os
import base64

def set_custom_style(background_image_path, sidebar_image_path):
    with open(background_image_path, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    with open(sidebar_image_path, "rb") as sidebar_img:
        sidebar_encoded = base64.b64encode(sidebar_img.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid=stSidebar] {{
        background-image: url("data:image/png;base64,{sidebar_encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    .stSidebar .sidebar-content {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(5px);
        padding: 1rem;
        border-radius: 10px;
    }}

    .main {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set page configuration
st.set_page_config(
    page_title="Mr.okey life data Upload Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set custom style
set_custom_style("assets/background.png", "assets/sidebar.png")

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

uploaded_file = st.file_uploader("Upload your data file (CSV)", type="csv")

if uploaded_file and st.button("Upload to Dashboard"):
    try:
        content = uploaded_file.read().decode("utf-8")
        
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
