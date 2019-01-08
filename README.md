# Test-project

Please contact me if you have any questions:

	Andrew Li (acli@uwaterloo.ca)

My GitHub bot account is named "IAmGithubBot". Examples are based off this name. 

1. First you need to create a GitHub account for your bot. Once you've created a bot, go to your Settings -> Developer Settings -> Personal	access tokens and create a new access token. At the minimum, you need to add repo and write:discussion access for your token. 

2. Save your token to this folder in a file with the name of your GitHub username "IAmGithubBot", and add it to your .gitignore file (if you commit your access token, GitHub invalidates it).

3. Set up a server that can receive POST requests from GitHub. You can use Ngrok (free) but the URL changes each time you use it. Run server.py to start the server on port 8080. 

4. Set up a webhook in your repository: Go to your repo -> Settings -> Webhooks and enter the URL of your server with port 8080. 

5. Now, every time someone comments on an issue on your repo, the bot will respond to them. 