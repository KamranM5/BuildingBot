# BuildingBot
A telegram bot with a connected MySQL database to automate the process of inspection control of construction projects.


First, you need to create a bot token in BotFather (https://t.me/BotFather) and put this information in the config.py file (first line). Here is an article on how to generate the token: https://botcreators.ru/blog/kak-sozdat-svoego-bota-v-botfather/.

After that you need to install the following libraries for the bot to work:

pip install mysql-connector-python
pip install telebot

After that you will need to create a mysql database and enter the necessary data in the functions.py file on line 4 instead of "!"
