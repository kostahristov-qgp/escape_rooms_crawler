✅ Setup Instructions

1. Install Python and Required Packages

To set up the environment:
 • Double-click the setup_environment.bat file.
 • This will automatically install Python and all required packages.

⸻

2. Schedule Daily Scraping (Optional)

To run the scrapers automatically every day:

🔧 Step-by-Step Guide
 1. Open Task Scheduler
  • Press Win + R, type taskschd.msc, and press Enter.
 2. Create a New Basic Task
  • In the right pane, click Create Basic Task…
  • Name it something like: Run Daily Crawlers.
 3. Set the Trigger
  • Choose Daily.
  • Set the start date.
  • Set the time: 09:00:00 (9 AM Bulgarian time).
 4. Set the Action
  • Choose Start a program.
  • Browse to and select the run_crawlers.bat file inside the kosta_hristov_project directory.
 5. Finish
  • Click Finish to create the scheduled task.

⸻

3. Export to Google Sheets (Optional)

To enable export of data to Google Sheets, you need to configure access to your Google account:
 • Follow this guide:
👉 Setting up Google Sheets for web scraping - https://scrapfly.io/blog/web-scraping-to-google-sheets/#setting-up-google-sheets-for-web-scraping

📌 Important
 • Save the downloaded JSON credentials file as:
  kosta_hristov_credentials.json
 • Place it directly inside the kosta_hristov_project directory.
 • Share the target Google Sheet with the service account email found in the credentials file — it usually ends with @<your-project>.iam.gserviceaccount.com.

⸻

4. Export to Excel + Google Drive (Alternative to Sheets)

If you prefer exporting to Excel instead of using the Google Sheets API, you can sync it to Google Drive automatically:

📁 Use Google Drive as a Synced Folder on Windows

 1. Install Google Drive for Desktop.
 2. After installation, sign in with your Google account.
 3. Google Drive will appear as a drive (e.g., G:\My Drive) or a folder under C:\Users\YourName\Google Drive.
 4. Save your Excel file (e.g., Escape Rooms - Statuses.xlsx) directly into a synced folder.
 5. The file will be automatically uploaded and synced to your Google Drive cloud storage.

💡 This method avoids Google Sheets API usage and still makes your data accessible in Google Drive.

⸻

5. Run Scrapers Manually (Without Scheduler)

To run scrapers manually:
 • Navigate to the kosta_hristov_project directory.
 • Double-click the run_crawlers.bat file.

💡 You can also create a desktop shortcut to run_crawlers.bat for easier access.