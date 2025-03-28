# Project Name

Green Neighbor Forum is a simple forum web application specifically designed for discussion around neighborhood tree-related issues.

## Project Features Overview

The system includes three user roles: member, moderator, and admin. The table below outlines the corresponding features for each user role:

| **Functionality**            | **Visitor** | **Voter** | **Scrutineer** | **Admin** |
| ---------------------------- | ----------- | --------- | -------------- | --------- |
| Registration                 | ✔️          |           |                |           |
| Login                        |             | ✔️        | ✔️             | ✔️        |
| Logout                       |             | ✔️        | ✔️             | ✔️        |
| Update My Profile            |             | ✔️        | ✔️             | ✔️        |
| Change Password              |             | ✔️        | ✔️             | ✔️        |
| Competition Settings         |             |           |                | ✔️        |
| Surfing Spot Management      |             |           |                | ✔️        |
| View Current Voting          | ✔️          | ✔️        | ✔️             | ✔️        |
| Voting                       |             | ✔️        |                |           |
| Backend User Management      |             |           |                | ✔️        |
| Voter User Management        |             |           | ✔️             | ✔️        |
| View Announcement            | ✔️          | ✔️        | ✔️             | ✔️        |
| Announcement Management      |             |           | ✔️             | ✔️        |
| Scrutineering                |             |           | ✔️             | ✔️        |
| Competition Results Overview | ✔️          | ✔️        | ✔️             | ✔️        |
| Competition Results Details  |             | ✔️        | ✔️             | ✔️        |

## Project Structure

-   **app/**: Project root directory.
    -   **voteapp/**: Contains the main source code of the application.
        -   **controller/**: Manages Flask routes and handles HTTP requests.
        -   **model/**: Defines entity classes for the database tables.
        -   **dao/**: Manages database access operations.
        -   **static/**: Stores static files like images, CSS, and JavaScript.
        -   **templates/**: Contains HTML templates for rendering views.
        -   **utils/**: Includes utility functions such as session management and hashing.
    -   **README.md**: Documentation file providing an overview, installation instructions, and usage guidelines.
    -   **requirements.txt**: Lists the dependencies required for the project.
    -   **run.py**: The entry point for starting the Flask application.
    -   **Create_Database.sql**: SQL script for creating the initial database schema.
    -   **Populate_Database.sql**: SQL script for populating the database with initial data.

## Coding Standards

### Naming Conventions

-   **Variable Names**: Use lowercase letters with words separated by underscores (snake_case).

    -   **Example**: `user_name`, `password_hash`, `voting_start_date`

-   **Function Names**: Use lowercase letters with words separated by underscores (snake_case).

    -   **Example**: `get_user_by_id()`, `update_password()`, `calculate_vote_ratio()`

-   **Class Names**: Use PascalCase, where each word starts with an uppercase letter.

    -   **Example**: `User`, `VoteManager`, `CompetitionSettings`

-   **Constant Names**: Use uppercase letters with words separated by underscores (UPPER_SNAKE_CASE).
    -   **Example**: `MAX_LOGIN_ATTEMPTS`, `DEFAULT_TIMEZONE`, `DATABASE_URL`

### Code Formatting

-   **Extension**: Install the Black Formatter extension in VSCode to ensure proper code style.

## Definition of Done (DoD)

1. **Functionality**: User stories meet the standards defined by Acceptance Criteria (AC).

2. **Code Quality**: Code has been reviewed and tested, following coding standards.

3. **Testing**:

    - **Local Testing**: Local tests pass before submission.
    - **Local Integration Testing**: Tests pass after merging remote code.
    - **Release Testing**: Tests pass on the PythonAnywhere server after merging into the main branch.

4. **Acceptance**: Product Manager reviews and accepts the functionality.

## Web Application Deployment

### 1. Clone the Project

First, clone the project code to your local machine:

```
git clone <repository URL>
cd <project directory>
```

### 2. Create a Virtual Environment

```
python -m venv venv
```

### 3. Activate the Virtual Environment

#### On macOS/Linux:

```
source venv/bin/activate
```

#### On Windows:

```
venv\Scripts\activate
```

### 4. Install Dependencies

With the virtual environment activated, install the project dependencies:

```
pip install -r requirements.txt
```

### 5. Run the Application

```
python run.py
```

## Database Deployment

### 1. Create the Database

```
mysql -h <host> -u <username> -p <database> < Create_Database.sql
```

### 2. Initialize the Database

```
mysql -h <host> -u <username> -p <database> < Populate_Database.sql
```

### 3. Initial User Information

#### Voter Role

| User name | Password    |
| --------- | ----------- |
| voter1    | voter1pass  |
| voter2    | voter2pass  |
| voter3    | voter3pass  |
| voter4    | voter4pass  |
| voter5    | voter5pass  |
| voter6    | voter6pass  |
| voter7    | voter7pass  |
| voter8    | voter8pass  |
| voter9    | voter9pass  |
| voter10   | voter10pass |
| voter11   | voter11pass |
| voter12   | voter12pass |
| voter13   | voter13pass |
| voter14   | voter14pass |
| voter15   | voter15pass |
| voter16   | voter16pass |
| voter17   | voter17pass |
| voter18   | voter18pass |
| voter19   | voter19pass |
| voter20   | voter20pass |
| voter21   | voter21pass |
| voter22   | voter22pass |
| voter23   | voter23pass |
| voter24   | voter24pass |
| voter25   | voter25pass |
| voter26   | voter26pass |
| voter27   | voter27pass |
| voter28   | voter28pass |
| voter29   | voter29pass |
| voter30   | voter30pass |

#### Site Admin Role

| User name  | Password       |
| ---------- | -------------- |
| siteadmin1 | siteadmin1pass |
| siteadmin2 | siteadmin2pass |




