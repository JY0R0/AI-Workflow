from drive import authenticate_drive, list_pdfs_from_folder, download_pdf
from sheets import authenticate_sheets, insert_into_sheet
from parser import pdf_to_text, extract_experience

def flatten_experience_json(data):
    name = data.get("name", "")
    experiences = data.get("experiences", [])
    row = [name]

    for i in range(3):
        if i < len(experiences):
            exp = experiences[i]
            row.extend([
                exp.get("company", ""),
                exp.get("title", ""),
                exp.get("start_date", ""),
                exp.get("end_date", "")
            ])
        else:
            row.extend(["", "", "", ""])
    return row


def main(folder_id, sheet_id):
    drive_service = authenticate_drive()
    sheet_service = authenticate_sheets()

    HEADER = [
        "Name",
        "Company 1", "Title 1", "Start Date 1", "End Date 1",
        "Company 2", "Title 2", "Start Date 2", "End Date 2",
        "Company 3", "Title 3", "Start Date 3", "End Date 3"
    ]
    sheet_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Sheet1!A1",
        valueInputOption="RAW",
        body={"values": [HEADER]}
    ).execute()

    files = list_pdfs_from_folder(drive_service, folder_id)
    for file in files:
        print(f"📄 Processing {file['name']}...")
        pdf_path = f"./{file['name']}"
        download_pdf(drive_service, file['id'], pdf_path)
        text = pdf_to_text(pdf_path)

        response = extract_experience(text)

        if not response:
            print(f"⚠️ Skipping {file['name']} due to empty or invalid LLaMA response.")
            continue

        try:
            row = flatten_experience_json(response)
            insert_into_sheet(sheet_service, sheet_id, row)
        except Exception as e:
            print("❌ Error parsing or inserting data:", e)


if __name__ == "__main__":
    FOLDER_ID = "1YkLK3Ags8WzZIXcINbU6xArkBzjEHQhz"
    SHEET_ID = "1Nd1MqsHJV8LjHvzKXVujz2qUMqi-4OmwXZnxe-MfooE"
    main(FOLDER_ID, SHEET_ID)
