✅ Setup Instructions

1. Install Python and Required Packages (Required)
	1.	Navigate to the project folder.
	2.	Double-click setup_environment.bat.
➝ This will automatically install Python and all required packages.

⸻

2. Schedule Daily Scraping (⚙️ Optional)

To run scrapers every day automatically:

Step-by-Step Guide
	1.	Press Win + R, type taskschd.msc, and press Enter.
	2.	In Task Scheduler, click Create Basic Task… (right panel).
	3.	Name the task: Run Daily Scrapers.
	4.	Trigger: choose Daily, set start date & time (e.g. 09:00 AM Bulgarian time).
	5.	Action: choose Start a program, then browse to run_crawlers.bat inside the kosta_hristov_project folder.
	6.	Click Finish.

⸻

3. Export to Google Sheets (⚙️ Optional)
	1.	Follow this guide 👉 Scrapfly – Google Sheets Setup.
	2.	Save the credentials JSON file as:
kosta_hristov_credentials.json
	3.	Place it directly in the kosta_hristov_project folder.
	4.	Share the target Google Sheet with the service account email (ends with @<your-project>.iam.gserviceaccount.com).

⸻

4. Export to Excel + Google Drive (⚙️ Alternative)

If you don’t want to use Google Sheets API:
	1.	Install Google Drive for Desktop and sign in.
	2.	A Google Drive folder will appear on your computer.
	3.	Save your Excel file (Escape Rooms - Statuses.xlsx) inside that folder.
	4.	It will sync automatically to your Google Drive.

⸻

5. Run Scrapers Manually

To run scrapers yourself:
	1.	Open the kosta_hristov_project folder.
	2.	Double-click run_crawlers.bat.
💡 (Optional: create a desktop shortcut for quick access).