import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def url_to_txt(url: str, output_dir: str = "docs") -> str:
    """
    Converts a webpage to a cleaned text file and saves it in the specified folder.

    Args:
        url (str): The webpage URL to scrape.
        output_dir (str): Folder to save the text file in (default: 'docs').

    Returns:
        str: Path to the saved text file.
    """
    try:
        # Get the absolute path to ensure we save in the right location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        full_output_dir = os.path.join(project_root, output_dir)
    
        
        # Create output directory if it doesn't exist
        os.makedirs(full_output_dir, exist_ok=True)
        
        # Fetch the webpage
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags (scripts, styles, etc.)
        for tag in soup(["script", "style", "noscript", "header", "footer", "svg", "img"]):
            tag.decompose()

        # Extract visible text
        text = soup.get_text(separator="\n")
        cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        # Generate filename from URL
        domain = urlparse(url).netloc.replace(".", "_")
        filename = f"{domain}.txt"
        output_path = os.path.join(full_output_dir, filename)

        # Save to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"✅ Text extracted and saved to: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error: {e}")
        return ""

if __name__ == "__main__":
    # Example usage
    test_url = input("Enter a website URL: ").strip()
    url_to_txt(test_url)
