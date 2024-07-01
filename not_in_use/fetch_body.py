from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_body(query):
    # Perform the search
    search_results = search(query, num_results=1)

    # Get the first result
    first_result = next(search_results, None)

    # Initialize an empty list to store paragraphs
    paragraphs = []
    # Check if the first result exists
    if first_result:
        # Make a request to the first result URL
        response = requests.get(first_result)

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find and store all <p> elements
            for paragraph in soup.find_all('p'):
                paragraphs.append(paragraph.get_text())
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return query  # Return the input query if there is an error
    else:
        print("No results found.")
        return query  # Return the input query if no results found

    # Combine the paragraphs into a single string
    paragraphs_combined = "\n".join(paragraphs)

    return paragraphs_combined

# Example usage
query = "cyber secuirty"
combined_paragraphs = get_body(query)
print(combined_paragraphs)
