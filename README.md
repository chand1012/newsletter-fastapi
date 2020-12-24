# FastAPI Newsletter Management

This is a small Python application, designed for the [Deta](https://www.deta.sh/) platform, that will manage [my blog's](https://chand1012.dev) Newsletter. If you would rather host this yourself via Docker, or on Heroku via Docker, you still need a [Deta Base](https://tinyurl.com/y7q38aek), which is a small NoSQL Database. You can sign up [here](https://web.deta.sh/) and get 2GB of storage for free. 

# Why?

I needed a simple way to have users sign up to my email subscription, and this method allows me host it myself (or rather have someone else host it for me). I can also set up the form on my own web page, and just send a Form `POST` request to the `/subscribe` endpoint and it will return a relative redirect to `/confirmation` if successful.

# .env

The `.env` file has four attributes: `SENDGRID_API_KEY`, `SENDGRID_SEND_EMAIL`, `API_KEY`, and `BASE_URL`. 

 - `SENDGRID_API_KEY` is your API key for the [SendGrid](https://sendgrid.com/) platform to send emails.
 - `SENDGRID_SEND_EMAIL` is the email from which your emails will be coming from. SendGrid will walk you through setting this up on your account.
 - `API_KEY` is a password so bots can't use the `/new_post` endpoint as that's just for you. You can pass it with the header `X-Api-Key`.
 - `BASE_URL` is the base URL of the application. This is usually a DNS record preceded by `https://`. 

After you've created your Deta Micro and populated these attributes in the file `.env`, you can upload them to your project with `deta update -e .env`.

# Hosting on Heroku

If you would rather use Heroku, you can host this application with the Dockerfile. You will have to set all of the variables found in the `.env` file as Config Vars on Heroku, as well as the additional variable `DETA_PROJECT_KEY` with your Deta Project Key, which is used to access the Deta Base. More information on how to set up your Deta Base can be found [here](https://tinyurl.com/y9nnxpqe).