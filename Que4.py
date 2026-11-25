
import json
import csv
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path

# Wikipedia URL
url = "https://en.wikipedia.org/wiki/List_of_Dublin_postal_districts"

# Step A: Download the webpage
response = requests.get(
    url,
    headers={
        "User-Agent": "StudentPostalDistrictScraper/1.0 (educational project)"
    },
    timeout=20
)

response.raise_for_status()

print("HTTP Status Code:", response.status_code)
print("Webpage downloaded successfully!")

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Dictionary to store postal districts
postal_districts = {}

# Extract postal districts
for heading in soup.find_all("h2"):

    title = heading.get_text(" ", strip=True)

    match = re.search(
        r"Dublin\s+\d+(?:\s+West)?\s*\((D\d+W?)\)",
        title
    )

    if not match:
        continue

    district_code = match.group(1)
    areas = []

    # Find paragraphs after each district heading
    for element in heading.find_all_next(["h2", "p"]):

        if element.name == "h2":
            break

        text = element.get_text(" ", strip=True)

        if "includes" in text.lower():

            # Remove reference citations
            for reference in element.select("sup"):
                reference.decompose()

            # Extract linked area names
            for link in element.find_all("a"):

                area = link.get_text(" ", strip=True)

                if area and area not in areas:
                    areas.append(area)

    if areas:
        postal_districts[district_code] = areas

# Verify extracted data
print("\nTotal districts found:", len(postal_districts))

if not postal_districts:
    raise RuntimeError("No postal districts extracted.")

print("Web scraping completed successfully!")

# Save files in the same folder as Que4.py
folder = Path(__file__).resolve().parent

json_path = folder / "dublin_postal.json"
csv_path = folder / "dublin_postal.csv"

# Step B: Store data in JSON file
with open(json_path, "w", encoding="utf-8") as file:
    json.dump(
        postal_districts,
        file,
        indent=4,
        ensure_ascii=False
    )

print("\nJSON file created successfully!")
print("JSON location:", json_path)

# Step C: Read JSON file
with open(json_path, "r", encoding="utf-8") as file:
    postal_data = json.load(file)

print("Data retrieved from JSON successfully!")

# Transfer JSON data to CSV
with open(csv_path, "w", newline="", encoding="utf-8-sig") as file:

    writer = csv.writer(file)

    writer.writerow(["Postal District", "Area Name"])

    for district, areas in postal_data.items():
        for area in areas:
            writer.writerow([district, area])

print("\nCSV file created successfully!")
print("CSV location:", csv_path)

# Step D: Read CSV and display data
print("\n==============================================")
print("          DUBLIN POSTAL DISTRICTS")
print("==============================================")

with open(csv_path, "r", encoding="utf-8-sig") as file:

    reader = csv.reader(file)

    for row in reader:
        print(f"{row[0]:<18} {row[1]}")

print("\nAll CSV records displayed successfully!")
print("Program completed successfully!")
