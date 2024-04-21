# filename: google_search_2022_ecommerce_revenues.py

from googlesearch import search

# Function to perform a Google search and return the first 10 results
def google_search(query):
    return list(search(query, num_results=10))

# Search for e-commerce revenue reports for 2022
query = "2022 e-commerce revenue report"
results = google_search(query)

for i, link in enumerate(results):
    print(f"Result {i+1}: {link}")

# Note: The 'googlesearch' package should be installed for this script to work.
# If not installed, you can install it using pip:
# pip install googlesearch-python