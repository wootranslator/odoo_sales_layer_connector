# Oracle Docker Infrastructure Configs

This repository contains the configuration for Docker containers running on the Oracle SSH server (`ubuntu`).

## Setup

- **Nginx**: Reverse proxy for `n8n` and other services.
- **Portainer**: Docker management interface.

## Usage

Portainer is configured to point to these stacks. Edits made here and pushed should be synchronized with the server's local copies.

To deploy manually:
```bash
docker-compose up -d
```
