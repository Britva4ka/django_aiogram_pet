# django_aiogram_pet

## Introduction
Hi, my name is Michael, also known as Britva4ka on GitHub. I graduated from Odessa National Maritime University with a degree in transportation logistics. I study Python as a hobby, but perhaps one day I will become a professional developer.

This project is a practice ground for my web development skills. I didn't have a specific plan in mind, so I decided to experiment with different technologies and functionalities. Here's what I've been working on:

### Telegram Bot
#### Implemented Features:
- Storing user information in the database.
- Allowing users to request weather information.
- Enabling users to subscribe to a daily morning weather forecast newsletter.
- Providing options for users to select the format of weather notifications and cancel subscriptions.
- Implementing antiflooding and remembering the last message sent by the bot using middleware.
- Creating a unique feature to delete last bot message without clogging the chat.
- Implementing a decorator for terminating any state, e.g., for the command `/cancel`.

#### Planned Features:
- Adding a second subscription, such as for exchange rates. Auto delete last message is cool, but I want to show u how to deal with callback query and edit messages.
- Implementing an admin area with unique capabilities.

### DJANGO APPLICATION:
#### Implemented Features:
- SQLite DB based on models.
- Running the Telegram bot by custom command.

#### Planned Features:
- Implementing an admin area.
- Creating an API using Django REST framework.
- Experimenting with HTML markup, Bootstrap, forms, etc.

## Installation
1. Clone the repository: `git clone https://github.com/Britva4ka/django_aiogram_pet.git`
2. Create a `.env` file: `touch .env`
3. Set your environment variables (refer to `env.example` for guidance).
4. Create a virtual environment: `python3 -m venv venv`
5. Activate the virtual environment: `source venv/bin/activate`
6. Install dependencies: `pip install -r requirements.txt`

## Run
- To run Django: `python3 manage.py runserver`
- To run the Telegram bot: `python3 manage.py runbot`

## Conclusion
I've been exploring various functionalities and technologies in this project. It's been a learning experience, and I'm excited to continue developing and adding new features. Feel free to explore the code and contribute if you like!
