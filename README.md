# Backdated Repository: January 2024 - July 2024
# User Management System (UMS)

## Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Modules](#api-modules)
- [Contributing](#contributing)
- [License](#license)

---

## About

The **User Management System (UMS)** is a backend application designed to manage users, roles, resources, actions, and their interrelations. Built for scalability and modularity, UMS integrates core user-management functionalities that are essential for modern applications, including role-based access control, API key management, and robust resource management.

---

## Features

- **User and Role Management:** Create, update, and manage users and their assigned roles.
- **Resource-Action Relationships:** Define and associate resources and actions for granular permissions.
- **Role-Based Access Control (RBAC):** Easily implement permission-based access policies.
- **API Key Management:** Securely generate and validate API keys for integration.
- **Modular Design:** Seamlessly extend the functionality with well-organized modules and reusable code.
- **Kubernetes Support:** Helm charts for deployment in Kubernetes clusters.

---

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd UMS-Backend
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Set up the environment:
    ```bash
    Copy the example environment file:
    cp .env.example .env
    ```
    Edit the .env file with your configuration.
4. Apply database migrations:
    ```bash
    alembic upgrade head
    ```
5. Start the application:
    ```bash
    python -m ums
    ```

## API Modules

### Overview
The `ums/api/modules` directory contains modular implementations for managing the relationships between users, roles, resources, and actions.

#### Key Modules:
1. **Users**: Create, update, and manage users.
2. **Roles**: Assign and manage roles.
3. **Resources**: Define application-specific resources.
4. **Actions**: Set actions such as "read," "write," and "delete" for resources.
5. **Resource-Action Relationships**: Establish granular permission mappings between roles and resources.
6. **User-Resource-Action Relationships**: Establish granular permission mappings between users, roles and resources. These are additional permissions that are not part of the role-based access control which are granted to users.

Refer to `ums/api/modules/*` for detailed implementation.
