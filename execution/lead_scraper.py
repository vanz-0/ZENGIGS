import csv
import os
import argparse

def standardize_leads(input_csv, output_csv="execution/leads.csv"):
    """
    Standardizes a raw lead export (e.g. from Apollo.io or LinkedIn) into the required format
    for the cold email sender.
    Required output columns: FirstName, Email, Company, Niche, PainPoint
    """
    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} not found.")
        return

    standardized_leads = []
    
    with open(input_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Add mapping logic here based on your export format
            # For this boilerplate, we'll assume the input already has some fields
            first_name = row.get("First Name", row.get("FirstName", ""))
            email = row.get("Email", "")
            company = row.get("Company", "")
            niche = row.get("Industry", "content creation") # Default or mapped
            
            # This painpoint can be customized per niche
            painpoint = "tech setup and social media management" 

            if first_name and email:
                standardized_leads.append({
                    "FirstName": first_name,
                    "Email": email,
                    "Company": company,
                    "Niche": niche,
                    "PainPoint": painpoint
                })

    with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["FirstName", "Email", "Company", "Niche", "PainPoint"])
        writer.writeheader()
        writer.writerows(standardized_leads)
        
    print(f"Standardized {len(standardized_leads)} leads and saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standardize lead exports.")
    parser.add_argument("--input", required=True, help="Path to raw CSV export")
    args = parser.parse_args()
    
    standardize_leads(args.input)
