from langchain.tools import tool
from finasistant_app.config.settings import settings

import os


@tool
def save_streamlit_page_code(python_code: str) -> str:
    """
    Save the generated Streamlit page code to a file with an incrementing number.

    This function saves the provided Python code for a Streamlit page in the
    ui/pages/ folder.

    Args:
        python_code (str): The Python code to be saved.

    Returns:
        str: The path of the saved file.
    """
    output_dir = settings.project_root / "finasistant_app" / "ui" / "pages"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create the filename with the incremented number
    file_name = "generated_analytics.py"
    file_path = output_dir / file_name

    # Write the Python code to the file
    try:
        with open(file_path, "w") as f:
            f.write(python_code)
        return f"{file_path}"
    except OSError as e:
        return f"Error saving Streamlit page: {str(e)}"


tools = [save_streamlit_page_code]
