# Restaurant Ordering Bot

A portfolio project that simulates an online restaurant ordering
workflow through Telegram. Users can browse products and place orders,
while an administrator can manage products and orders through an admin
panel.

> This is a portfolio and learning project. It is not connected to a
> real restaurant or a payment provider.

## Features

### User Features

-   Start the bot with `/start`
-   Browse the main menu
-   View products, prices, and availability
-   Select products using Telegram inline buttons
-   Add products to the cart and choose quantities
-   View the cart and order summary
-   Place orders and check their status
-   View and manage profile information
-   Read information about the bot

### Admin Features

-   Open the admin panel with `/admin`
-   Check administrator permissions
-   Add products
-   View the product list
-   Edit and delete products
-   View and manage orders

## Tech Stack

-   **Python**
-   **aiogram 3** --- asynchronous Telegram bot framework
-   **PostgreSQL** --- relational database
-   **SQLAlchemy (Async ORM)** --- database access and ORM
-   **Alembic** --- database schema migrations
-   **Environment variables** --- application configuration and secrets

## Architecture

``` text
Telegram User
     |
     v
aiogram Router / Handler
     |
     v
Service Layer
     |
     v
SQLAlchemy AsyncSession
     |
     v
PostgreSQL
```

The layered structure separates Telegram updates, application logic, and
database operations to make the project easier to maintain and extend.

## Requirements

-   A Python version compatible with the project's dependencies
-   PostgreSQL
-   A Telegram bot created through [@BotFather](https://t.me/BotFather)

## Setup

### 1. Get the project

If the project is hosted in a Git repository:

``` bash
git clone <repository-url>
cd Resturant_bot
```

Otherwise, open a terminal in the project directory.

### 2. Create a virtual environment

``` bash
python -m venv .venv
```

Activate it on Windows:

``` powershell
.venv\Scripts\activate
```

On Linux or macOS:

``` bash
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Create the database

Create a PostgreSQL database for the project. For example:

``` sql
CREATE DATABASE restaurant_bot;
```

Make sure the database name matches the one in your `DATABASE_URL`.

### 5. Configure environment variables

If the project includes an `.env.example` file, copy it to `.env`.
Otherwise, create `.env` using the variable names expected by the
project's configuration.

Example:

``` env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_user_id
DATABASE_URL=postgresql+asyncpg://USERNAME:PASSWORD@localhost:5432/restaurant_bot
```

These values are examples. Match the variable names and connection
string format to the actual project configuration.

-   `BOT_TOKEN`: The bot token provided by BotFather.
-   `ADMIN_ID`: The administrator's numeric Telegram user ID.
-   `DATABASE_URL`: The SQLAlchemy connection URL for PostgreSQL.
    Install the asynchronous database driver used by the project.

**Security:** Never commit your `.env` file or expose your bot token or
database credentials. Make sure `.env` is listed in `.gitignore`. If the
bot token is exposed, revoke it through BotFather and generate a
replacement.

### 6. Apply database migrations

If Alembic is configured, create or update the database schema with:

``` bash
alembic upgrade head
```

### 7. Run the bot

From the project root directory, run:

``` bash
python main.py
```

Open the bot in Telegram and send `/start`. Use `/admin` to access the
admin panel with an authorized account.

## Bot Commands

  Command    Description
  ---------- -------------------------------------------------------
  `/start`   Start the bot and display the main menu
  `/admin`   Open the admin panel (authorized administrators only)

Administrative permissions should be checked on the server side for each
protected operation. Hiding admin buttons alone is not an access-control
mechanism.

## Data Models

Depending on the implemented features, the main database models may
include:

-   **User:** Telegram user information and role
-   **Product:** Product name, price, description, and availability
-   **Order:** Customer order, total price, creation time, and status
-   **OrderItem:** Products in an order, quantity, and price recorded at
    purchase time

If the shopping cart is implemented using separate models, `Cart` and
`CartItem` can store items before checkout.

## Project Status

This project was developed as a portfolio sample to demonstrate Telegram
bot development, asynchronous Python, relational database integration,
and separation of application logic.

## Development Notes

-   Verify the environment variable names and configuration paths
    against the actual source code before running the project.
-   Avoid hard-coding bot tokens and database credentials.
-   Review and test Alembic migrations before applying schema changes.
-   For production use, consider adding automated tests, structured
    logging, robust error handling, database backups, and comprehensive
    access-control checks.

## License

No license has been specified yet. If you publish this repository
publicly, choose and add a license that matches how you want others to
use the project.
