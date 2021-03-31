# Tradot

Tradot is a simple and easy to configure framework for launching e-commerce stores, that too with a really smart chatbot!

## Sample Commands
We have made it easy to test out our highlight feature, the bot.
Try some of these commands to start out:

```text
Hello
What do you sell?
Add Bagel to my cart
Checkout
```

Our chatbot can also interact with a live Question and Answer Database, which we have configured in the form of Google Sheets. Merchants can enter some of their FAQs and the bot will do all the heavy lifting for them.

As an example, paste this command into the bot to see what happens!
```What gift cards do you have?```

## Project Structure

This project has been divided into several micromodules to make the code more modular and to allow for further development.

Inside the backend,

```chatbot-server``` contains all the source code for the Dialogflow bot. It contains many useful API Endpoints, using which the functionality of the bot can be further improved. This has been written in ```Python```.

```webstore-server``` contains all the source code for our ```ExpressJS``` server. This server also acts as an API Endpoint, providing resources for user authentication among others. A ```MongoDB``` Database has been used for storing user data.

```frontend``` is the production build of our main ```React``` App. It uses the API endpoints from the other two services.


## License
[MIT](https://choosealicense.com/licenses/mit/)
