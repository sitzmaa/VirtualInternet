# Virtual Internet Emulation For Cybersecurity Training

## Project Overview

The Virtual Internet project provides comprehensive cybersecurity training in a safe, stable, and self-contained environment. Utilizing the open-source SEED Emulator, it emulates real-world network devices and communications, offering a robust training ground for cybersecurity education.

## Vision Statement

Designed for Western Washington University (WWU) students, this project allows for safe and practical cybersecurity labs and exercises. By integrating with WWU’s Cyber Range and abstracting setup processes through the SEED Emulator, students can focus on learning and practicing cybersecurity tasks.

## Technology Utilized

- **Debian-based Linux distribution**
- **Python3**
- **Docker**
- **SEED Emulator**

## Hardware Requirements

- **8GB RAM**
- **20GB SSD/HDD**
- **4 or more cores on Intel 7th-gen or AMD 2000-series or newer processor**
- **Ubuntu Horizon Platform**: Hosting lab images on the cyber range

## Project Outcomes

### Added Features

- **Automated User Manual**: A script opens a User Manual upon VM launch, providing terminal commands for various labs.
- **Optimized Bash Scripts**: Aliased commands run optimized bash scripts managing SEED Emulator's launch process.
- **New Labs**: Implementation of BGP Attack and Botnet labs.
- **Updated Network Build Script**: Extensible and explanatory Python script for network building.

## Architecture

### System Architecture

- **SEED Emulator Integration**: Python scripts within the SEED framework generate Docker Containers representing network devices.
- **Cyber Range Interaction**: Hosted on WWU’s Cyber Range, with lab images on the Ubuntu Horizon Platform.

### Deployment and Configuration

- **Component Connections**: Docker networks enable communication between virtual devices.
- **Deployment Requirements**: Systems must meet specified hardware requirements and have Docker and Python environments set up.
- **Dependencies**: SEED Emulator, Docker, and Python libraries.
- **Security Mechanisms**: Isolated virtual environment, secure communication protocols.

## Areas for Future Work

- **Netbuild.py Script**: Enable creation of asymmetrical and complex networks, integrate SEED’s DNS server, webserver, blockchain simulation, and VPN simulation.
- **Expand SEED Labs**: Develop and publish additional labs to the Cyber Range.
- **Cross VM Interactions**: Enable interactions across virtual machines via the Cyber Range Virtual Internet Sub network.


