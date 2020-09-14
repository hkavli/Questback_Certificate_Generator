## Certificate Generator for Questback

This app helps Questback employees create certificates for customers that become "Certified Essentials Users"

## Tech/framework used

- ReportLab PDF Generator for Python
- Dropbox API

<b>Built with</b>

- [Python](https://www.python.org/)

## Installation

- Python 3, PIP, ReportLab
- Retrieve an API key from your desired Dropbox folder (to be stored in an .env file)
- Update the .env file with a mail adress (e.g.@gmail.com*) and a password to the mail client. [Google has a setting that allow apps external access](https://myaccount.google.com/lesssecureapps)

## API Reference

[ReportLab](https://www.reportlab.com/docs/reportlab-userguide.pdf)
[Dropbox API](https://dropbox-sdk-python.readthedocs.io/en/latest/)

## How to use?

- Store course participants for a given (new) course in a .csv file in the /participants folder
  Accepted formats are:
- "name,company,emailadress,dateCourse1,nameCourse1,city,dateCourse2,nameCourse2"
- "name,company,emailadress,dateCourse1,nameCourse1,city"

## License

MIT © [hkavli]()
# Questback_Certificate_Generator
