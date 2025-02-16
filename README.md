# 🚖 Taxi Fare System

## Table of Contents
- [Introduction](#introduction)
- [Description](#description)
- [Objective](#objective)
- [Libraries Used](#libraries-used)
- [Folder Structure](#folder-structure)
    - [🟢 Basic Level](#basic-level)
    - [🟡 Intermediate Level](#intermediate-level)
- [Roadmap](#roadmap)
- [Development Status](#development-status)
- [Contact](#contact)

---

## Introduction

This repository contains a Taxi Fare System developed in Python. The project is divided into two levels:

1. **Basic Level**: A simple CLI-based system where the user can start a ride, calculate fares for both moving and stationary taxi, and end a ride.
2. **Intermediate Level**: This level adds logging, unit tests, and a history of past trips for enhanced functionality.

The goal is to gradually improve the system, making it more robust and feature-rich.

---
## 👀 Description

The **Taxi Fare System** is a Python-based program designed to simulate the calculation of taxi fares during a ride. The system is intended to be used in real-time scenarios where a user can track their ride, whether the taxi is stationary or moving. 

It aims to provide a simple yet effective CLI tool for managing taxi fares, focusing on real-time calculations and easy-to-use features. In its **Essential Level**, the program offers a simple ride simulation with basic fare tracking. In the **Intermediate Level**, additional features such as logging, unit testing, and historical ride tracking are added to make the system more scalable and reliable.

This system is ideal for anyone looking to create a simple taxi fare program or develop a more robust solution with additional features as they learn more about Python and software development.

---
## 🔍 Objective

The primary **objective** of this project is to build a scalable and easy-to-use taxi fare system that can grow with additional features and improvements over time. 

**Key objectives include**:

- **Real-time Fare Calculation**: Allow the system to calculate taxi fares dynamically as the taxi moves or stays stationary.
- **Customizable Fare Settings**: Enable users to adjust fare configurations according to demand and various factors.
- **Logging and History**: Implement logging for tracking system activity and storing ride history for future reference.
- **Unit Testing**: Use testing frameworks to ensure the system is bug-free and performs as expected.
- **Scalability**: Design the system to be easily extensible, allowing for future features such as a GUI, user authentication, and web-based access.

The goal is to create a well-documented, modular, and easily maintainable codebase that will serve as both a learning tool and a foundation for future development.

---

## 📚 Libraries Used
 
The following libraries have been used in this project:

- **time**: To handle time-related operations, like calculating duration.
- **datetime**: For timestamping and date-related functionality.
- **json**: Used for saving and loading configuration data, and storing historical records.
- **os**: For interacting with the operating system, such as creating or managing files.
- **logging**: To implement logging and track system events.
- **pytest**: For running unit tests to ensure code correctness.
- **unittest.mock**: For mocking objects in unit tests.

---

## 📂 Folder Structure

The project is organized into two main folders:

### Essential Level
- **`essential_level/`**: Contains the basic functionality of the Taxi Fare System.
  - **`taximeter_essential_level.ipynb`**: A Jupyter notebook where the basic CLI functionality is demonstrated.

### Intermediate Level
- **`intermediate_level/`**: Includes the more advanced features like logging and historical records.
  - **`main_taximeter_intermediate_level.py`**: Python script for handling the core logic of the taxi fare system.
  - **`rates.json`**: JSON file containing the fare configuration.
  - **`logs_ride.log`**: Log file for tracking system events.
  - **`history_ride.json`**: JSON file for storing the historical data of previous rides.

---

  ## 🟢 Essential Level

  The **Esential Level** contains the essential features of the Taxi Fare System:

  1. **Welcome Message**: When the program starts, it will greet the user and provide a brief explanation of how it works.
  2. **Start a Ride**: The user can initiate a ride and begin tracking the taxi's movement.
  3. **Fare Calculation**:
      - When the taxi is **stationary**, it charges 2 cents per second.
      - When the taxi is **moving**, it charges 5 cents per second.
  4. **End the Ride**: When the ride ends, the program will show the total fare in euros.
  5. **New Ride**: After completing a ride, the user can start a new ride without closing the program.

  ---

  ## 🟡 Intermediate Level

  The **Intermediate Level** introduces more advanced features to enhance the system:

  1. **Logging**: A logging system is added to track various events such as the start and end of rides.
  2. **Unit Testing**: Using `pytest` and `unittest.mock`, the code is tested to ensure correctness and reliability.
  3. **Historical Records**: All past rides are stored in a JSON file for future reference.
  4. **Fare Configuration**: Users can modify fare settings in the `rates.json` file to adapt to demand changes (e.g., peak hours).

---

## 📍Roadmap

### 🔜 Future Features (Development Phase)
#### 🟠 Advanced Level
The **Advanced Level** will introduce the following enhancements to further improve the system:

1. **Refactor Code with OOP**: Refactor the existing code using Object-Oriented Programming (OOP) principles to improve maintainability, scalability, and readability.
2. **Authentication System**: Implement a password-based authentication system to protect access to the program, ensuring that only authorized users can use it.
3. **Graphical User Interface (GUI)**: Develop a user-friendly graphical interface to make the program more intuitive and accessible.

#### 🔴 Expert Level
The **Expert Level** will take the project to the next level with more advanced features:

1. **Database Integration**: Integrate a database to store and manage historical ride records, improving scalability and data management.
2. **Dockerization**: Dockerize the application to make it easy to deploy and portable across different environments.
3. **Web Application**: Develop a web-based version of the Taxi Fare System, making it accessible via a browser and enabling internet-based access.
---

## Development Status

🚧 **Work in Progress** 🚧 

The project is currently in development, and focusing on expanding the system to include more advanced features. Stay tuned for future updates!


---

## Contact

If you have any questions or would like to contribute to the project, feel free to reach out to me:

[LinkedIn Yael Parra](https://www.linkedin.com/in/yael-parra/)
