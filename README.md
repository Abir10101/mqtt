# Sensor Monitoring System

The Sensor Monitoring System is designed to simulate sensor behavior, monitor their readings, and provide APIs to retrieve data based on specific criteria. This system employs MQTT communication for data transmission, MongoDB for data storage, Redis for in-memory data management, and FastAPI for API endpoints.

## Table of Contents
- [Components](#components)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Components
- **MQTT Broker (EMQX):** Deployed using Docker to facilitate communication between services using the MQTT (Message Queuing Telemetry Transport) protocol.
- **MQTT Publisher:** Python MQTT client that simulates sensor readings and publishes them to specific topics.
- **MQTT Subscriber:** Python MQTT client that subscribes to MQTT topics, stores messages in MongoDB, and caches the latest data using Redis.
- **MongoDB:** Used to store MQTT messages.
- **Redis:** Utilized for caching the latest ten sensor readings of specific sensor id.
- **FastAPI:** Provides API endpoints for retrieving sensor data.

## Requirements
- Docker
- Docker Compose

## Installation
1. Clone this repository. `git clone https://github.com/Abir10101/mqtt.git`
2. Navigate to the project directory: `cd mqtt`
3. Start the system using Docker Compose: `docker-compose up --build -d`

## Usage
1. Run publisher to simulates message posting to MQTT broker: `docker-compose start publisher`
2. Access FastAPI documentation to interact with API endpoints: `http://localhost:5000/docs`
3. Access MongoDB web UI to visualize the data: `http://localhost:8081`
4. Access Redis Cli client to check cache stored: `docker-compose start redis-client`
