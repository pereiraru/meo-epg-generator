# MEO EPG Generator

![MEO Logo](https://www.meo.pt/favicon.ico) Automatic daily XMLTV EPG from MEO Portugal

Generate XMLTV-format Electronic Program Guide (EPG) from MEO Portugal's TV guide. Automatically updates daily via GitHub Actions.

## Features

- 🎬 **200+ TV Channels**: Extracts data from all available MEO TV channels
- - 📅 **7-Day Schedule**: Complete program listings for the next 7 days
  - - 🎯 **XMLTV Format**: Compatible with UHF app on Apple TV, iOS, iPadOS, and macOS
    - - 📱 **Full Channel Info**:
      -   - Channel IDs and names
          -   - Channel numbers
              -   - Channel logos/icons
                  -   - Genre/category information
                      - - 📺 **Detailed Programs**:
                        -   - Program titles
                            -   - Start and end times
                                -   - Duration
                                    -   - Descriptions/synopses
                                        - - ⚙️ **Automated Updates**: Daily generation via GitHub Actions (runs at 02:00 UTC)
                                          - - 🔄 **Manual Trigger**: Can be run manually anytime through GitHub Actions
                                           
                                            - ## Installation
                                           
                                            - ### Prerequisites
                                           
                                            - - Python 3.8+
                                              - - pip (Python package manager)
                                               
                                                - ### Setup
                                               
                                                - 1. Clone the repository:
                                                  2. ```bash
                                                     git clone https://github.com/pereiraru/meo-epg-generator.git
                                                     cd meo-epg-generator
                                                     ```

                                                     2. Install dependencies:
                                                     3. ```bash
                                                        pip install -r requirements.txt
                                                        ```

                                                        3. Run the generator:
                                                        4. ```bash
                                                           python scraper.py
                                                           ```

                                                           This will create a `guide.xml` file with the XMLTV EPG data.

                                                           ## Usage with UHF App

                                                           ### How to Use with UHF on Apple TV/iOS/iPadOS/macOS

                                                           1. **Get the EPG URL**:
                                                           2.    - The generated `guide.xml` is automatically pushed to this repository
                                                                 -    - Raw file URL: `https://raw.githubusercontent.com/pereiraru/meo-epg-generator/main/guide.xml`
                                                                  
                                                                      - 2. **Configure UHF App**:
                                                                        3.    - Open UHF application
                                                                              -    - Go to Settings → EPG
                                                                                   -    - Add new EPG source
                                                                                        -    - Paste the URL: `https://raw.githubusercontent.com/pereiraru/meo-epg-generator/main/guide.xml`
                                                                                             -    - Save and refresh
                                                                                              
                                                                                                  - 3. **The guide will automatically update daily** at 02:00 UTC
                                                                                                   
                                                                                                    4. ## Configuration
                                                                                                   
                                                                                                    5. ### Changing the Update Schedule
                                                                                                   
                                                                                                    6. Edit `.github/workflows/generate-epg.yml`:
                                                                                                   
                                                                                                    7. ```yaml
                                                                                                       schedule:
                                                                                                         - cron: '0 2 * * *'  # Change this cron expression
                                                                                                       ```
                                                                                                       
                                                                                                       Examples:
                                                                                                       - `0 2 * * *` - Daily at 02:00 UTC
                                                                                                       - - `0 4 * * *` - Daily at 04:00 UTC
                                                                                                         - - `0 */6 * * *` - Every 6 hours
                                                                                                           - - `0 0 * * 0` - Weekly (Sunday at 00:00 UTC)
                                                                                                            
                                                                                                             - ### Changing the Number of Days
                                                                                                            
                                                                                                             - Edit `scraper.py`:
                                                                                                            
                                                                                                             - ```python
                                                                                                               generator = MEOEPGGenerator(days=7)  # Change 7 to desired number of days
                                                                                                               ```
                                                                                                               
                                                                                                               ## File Structure
                                                                                                               
                                                                                                               ```
                                                                                                               meo-epg-generator/
                                                                                                               ├── scraper.py                           # Main script to generate EPG
                                                                                                               ├── requirements.txt                     # Python dependencies
                                                                                                               ├── guide.xml                            # Generated XMLTV file (auto-updated)
                                                                                                               ├── README.md                            # This file
                                                                                                               └── .github/
                                                                                                                   └── workflows/
                                                                                                                       └── generate-epg.yml             # GitHub Actions workflow
                                                                                                               ```
                                                                                                               
                                                                                                               ## GitHub Actions
                                                                                                               
                                                                                                               The repository includes an automated workflow that:
                                                                                                               
                                                                                                               1. Runs daily at 02:00 UTC
                                                                                                               2. 2. Fetches the latest TV guide from MEO
                                                                                                                  3. 3. Generates the XMLTV EPG file
                                                                                                                     4. 4. Commits and pushes the updated `guide.xml`
                                                                                                                       
                                                                                                                        5. You can also trigger the workflow manually:
                                                                                                                       
                                                                                                                        6. 1. Go to the "Actions" tab in the repository
                                                                                                                           2. 2. Select "Generate MEO EPG" workflow
                                                                                                                              3. 3. Click "Run workflow"
                                                                                                                                
                                                                                                                                 4. ## Dependencies
                                                                                                                                
                                                                                                                                 5. - **requests** - HTTP library for web requests
                                                                                                                                    - - **beautifulsoup4** - HTML parsing
                                                                                                                                      - - **lxml** - XML processing
                                                                                                                                        - - **python-dateutil** - Date/time utilities
                                                                                                                                         
                                                                                                                                          - See `requirements.txt` for specific versions.
                                                                                                                                         
                                                                                                                                          - ## XMLTV Format
                                                                                                                                         
                                                                                                                                          - The generated `guide.xml` follows the XMLTV standard format with:
                                                                                                                                         
                                                                                                                                          - ```xml
                                                                                                                                            <?xml version="1.0" encoding="UTF-8"?>
                                                                                                                                            <tv>
                                                                                                                                              <channel id="RTP1">
                                                                                                                                                <display-name lang="pt">RTP 1</display-name>
                                                                                                                                                <icon src="https://..."/>
                                                                                                                                              </channel>
                                                                                                                                              <programme start="20240101120000 +0000" stop="20240101123000 +0000" channel="RTP1">
                                                                                                                                                <title lang="pt">Program Title</title>
                                                                                                                                                <desc lang="pt">Program description</desc>
                                                                                                                                              </programme>
                                                                                                                                              ...
                                                                                                                                            </tv>
                                                                                                                                            ```
                                                                                                                                            
                                                                                                                                            ## Troubleshooting
                                                                                                                                            
                                                                                                                                            ### The guide.xml file is not updating
                                                                                                                                            
                                                                                                                                            1. Check the "Actions" tab to see if the workflow is running
                                                                                                                                            2. 2. If it fails, check the logs for errors
                                                                                                                                               3. 3. Ensure the repository has push permissions enabled for the workflow
                                                                                                                                                 
                                                                                                                                                  4. ### UHF app not showing channels
                                                                                                                                                 
                                                                                                                                                  5. 1. Verify the EPG URL is correct and accessible
                                                                                                                                                     2. 2. Try refreshing the EPG in the UHF app settings
                                                                                                                                                        3. 3. Check that the XML file is valid (can be validated at [xmllint.com](https://www.xmllint.com/))
                                                                                                                                                          
                                                                                                                                                           4. ### Missing channels or programs
                                                                                                                                                          
                                                                                                                                                           5. - MEO might have blocked the scraper
                                                                                                                                                              - - Check if the structure of MEO's website has changed
                                                                                                                                                                - - Report an issue if you encounter this problem
                                                                                                                                                                 
                                                                                                                                                                  - ## Contributing
                                                                                                                                                                 
                                                                                                                                                                  - Contributions are welcome! Please feel free to:
                                                                                                                                                                 
                                                                                                                                                                  - - Report bugs or issues
                                                                                                                                                                    - - Suggest improvements
                                                                                                                                                                      - - Submit pull requests
                                                                                                                                                                       
                                                                                                                                                                        - ## Legal Notice
                                                                                                                                                                       
                                                                                                                                                                        - This project is for personal use only. Ensure you comply with MEO's Terms of Service and any applicable laws regarding web scraping and data usage.
                                                                                                                                                                       
                                                                                                                                                                        - ## License
                                                                                                                                                                       
                                                                                                                                                                        - This project is provided as-is for personal use.
                                                                                                                                                                       
                                                                                                                                                                        - ## Support
                                                                                                                                                                       
                                                                                                                                                                        - If you encounter issues or have questions:
                                                                                                                                                                       
                                                                                                                                                                        - 1. Check the [Issues](https://github.com/pereiraru/meo-epg-generator/issues) tab
                                                                                                                                                                          2. 2. Create a new issue with detailed information
                                                                                                                                                                             3. 3. Include any relevant error messages or logs
                                                                                                                                                                               
                                                                                                                                                                                4. ## Changelog
                                                                                                                                                                               
                                                                                                                                                                                5. ### Version 1.0.0
                                                                                                                                                                                6. - Initial release
                                                                                                                                                                                   - - Support for 200+ MEO channels
                                                                                                                                                                                     - - 7-day schedule
                                                                                                                                                                                       - - Daily automated updates via GitHub Actions
                                                                                                                                                                                         - - Full XMLTV format support
                                                                                                                                                                                          
                                                                                                                                                                                           - ---
                                                                                                                                                                                           
                                                                                                                                                                                           **Made with ❤️ for MEO TV viewers**
