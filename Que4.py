import json
import csv
import requests
from bs4 import BeautifulSoup
import re

# Wikipedia URL
url = "https://en.wikipedia.org/wiki/List_of_Dublin_postal_districts"

# Download the webpage
response = requests.get(
    url,
    headers={"User-Agent": "StudentPostalDistrictScraper/1.0 (educational project)"},
    timeout=20
)
response.raise_for_status()

print("Webpage downloaded successfully!")

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Dictionary to store postal districts
postal_districts = {}

# Find all district headings
for heading in soup.find_all("h2"):

    title = heading.get_text(" ", strip=True)

    match = re.fullmatch(
        r"Dublin\s+(\d+)(?:\s+West)?\s*\((D\d+W?)\)",
        title
    )

    if not match:
        continue

    district_code = match.group(2)
    areas = []

    # Read paragraphs after the heading
    for element in heading.next_siblings:

        if getattr(element, "name", None) == "h2":
            break

        if getattr(element, "name", None) != "p":
            continue

        text = element.get_text(" ", strip=True)

        # Collect linked area names from the district description
        if "includes" in text.lower():
            for link in element.find_all("a"):
                area = link.get_text(" ", strip=True)

                if area and area not in areas:
                    areas.append(area)

    postal_districts[district_code] = areas

# Display extracted results
for code, areas in postal_districts.items():
    print(f"\nPostal District: {code}")
    print("Areas:", ", ".join(areas))

print("\nTotal districts found:", len(postal_districts))
# Save scraped postal districts to JSON file
with open("dublin_postal.json", "w", encoding="utf-8") as file:
    json.dump(postal_districts, file, indent=4, ensure_ascii=False)

print("\nPostal districts saved successfully to JSON!")

# Read the JSON file to verify the saved data
with open("dublin_postal.json", "r", encoding="utf-8") as file:
    saved_data = json.load(file)

print("Total districts in JSON:", len(saved_data))

# Read CSV file and display all postal districts

print("\n==============================================")
print("       DUBLIN POSTAL DISTRICTS")
print("==============================================")

# Read JSON file
with open("dublin_postal.json", "r", encoding="utf-8") as file:
    postal_data = json.load(file)

# Create CSV file
with open("dublin_postal.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    writer.writerow(["Postal District", "Area Name"])

    for district, areas in postal_data.items():
        for area in areas:
            writer.writerow([district, area])

print("CSV file created successfully!")