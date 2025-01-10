# Gaming LeaderBoard Management System

## Project Description:
The Gaming Leaderboard System is a project designed to manage players, games, scores, and rankings within a gaming ecosystem. It enables seamless operations such as adding players, recording scores, and retrieving game rankings. Built using Python, Flask, and Oracle Database, the system ensures a robust backend for efficient data management and interaction.

## Key Features
1.Player Management: The system allows adding, retrieving, and deleting player records, enabling efficient management of participants in the gaming ecosystem.

2.Game Management: Users can retrieve a list of all available games stored in the database to track and manage supported games.

3.Score Recording: The platform supports recording player scores with details like match ID, game name, and achievement dates to ensure accurate performance tracking.

4.Rankings: Rankings are dynamically generated based on players' scores, allowing users to retrieve and view leaderboards for specific games.

5.RESTful APIs: The system includes well-structured APIs for managing players, games, scores, and rankings, providing seamless interaction and integration capabilities.

6.Database Integration: It leverages an Oracle Database to securely store and manage players, games, scores, and rankings, ensuring data consistency and reliability.


## Technologies Used
1.Backend:
Python: Core programming language.
Flask: Lightweight web framework for building APIs.
Database:

2.Oracle Database: Reliable relational database for data storage.
Libraries:

3.oracledb: For Oracle database connectivity.
requests: For HTTP requests to interact with APIs.


## How It Works
1.Database Connectivity:
Connects to an Oracle database using credentials provided via environment variables.
Stores data for players, games, scores, and rankings.
RESTful API Endpoints:

2.Enables operations like adding players, fetching games, recording scores, and retrieving rankings.
Users can interact with these endpoints programmatically or via tools like Postman.
Rankings Calculation:

3.Rankings for a game are dynamically generated based on scores and stored in the database for quick retrieval.

The Gaming Leaderboard System provides an efficient and scalable solution for managing gaming data, making it ideal for tournaments, esports, or analytics-focused applications. 
It serves as a strong foundation for expanding into more advanced gaming management features.


