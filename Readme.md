# Member Remover Bot

---

- ## Requirements:

    - This program needs python version 3.11 or higher to run.
    - ### Guide for Linux:

        - Open your terminal and cd to the directory where you have the extracted files.
        - Create a virtual environment by running `python3 -m venv venv`.
        - activate the environment by running `source venv/bin/activate`
        - Install the requirements by running `pip install -r requirements.txt`
        - Open the `.env` file and fill it with your telegram `api_id`, `api_hash`, `bot_token`.
        - You can get your Telegram api credential by registering an app here: https://my.telegram.org/
    
    - ### How to create Google service account?
        - Open google cloud console
        - Create a project
        - Inside that project enable Google Sheets API
        - Then go to credentials and create a service account, set the access as editor
        - Download the json key of the service account
    
    - ### Why the bot can't access the sheet?
        - You'll need to share the sheet with the service account's email as editor

- ## Starting the program:

    - Run the program by using `python3 main.py`.
    - It will prompt you that your admin id is invalid, unless you have replaced the default value with a correct id.
    - ### Setting up admin id:

        - Add the bot to a group
        - Make the bot an admin of the group
        - Send `/admin` in the group to mark the group as admin chat

    - ### Commands:

        - /start - Shows the current status of the bot and also shows some helpful tips.
        - /admin - To mark a group as admin chat, can be marked once
        - /auth - To authorize a google service account
        - /sheet - To set up a google sheet
        - /worker - To connect a telegram account into the bot
        - /refresh - To manually trigger the member count task


Hire me at

[![Hire concaption on upwork: https://www.upwork.com/freelancers/concaption](https://img.shields.io/badge/UpWork-6FDA44?style=for-the-badge&logo=Upwork&logoColor=white)](https://www.upwork.com/freelancers/concaption)
