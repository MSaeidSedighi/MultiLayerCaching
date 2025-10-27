# Multi-Layer Caching Service

This repository provides a flexible and robust **Multi-Layer Caching** solution built for Django. It is designed to significantly reduce latency and load on backend services by sequentially checking multiple, increasingly persistent cache layers before resorting to the original data source (e.g., a database or external API).

The entire system, including the caching services (Memcached and Redis), is **fully Dockerized** for easy setup and deployment.

---

## Features

- Configurable multi-layer caching
- Pluggable fetch function for any API or data source
- Per-layer TTLs
- Dockerized with Redis and Memcached
- Layer order can be changed via `.env`
- New cache layers can be added

## Requirements

- Python 3.10+
- Django 4+
- Docker
- Docker Compose

## Setup

### 1. Clone the repository

```bash
git clone <repo_url>
cd <repo_folder>
```

### 2. Create a `.env` file
sample `.env` file:
```.env
# ----------------------------------------------------------------------
# CACHE LAYER CONFIGURATION
# ----------------------------------------------------------------------

# Define the order of cache layers, separated by commas.
# The system checks the layers in the order specified here.
# Available layers: inapp, memcache, redis
CACHE_LAYERS=inapp,memcache,redis

# ----------------------------------------------------------------------
# TIME-TO-LIVE (TTL) IN SECONDS
# ----------------------------------------------------------------------

# Define how long (in seconds) data should persist in each layer.
# Note: Typically, the layers further down the hierarchy (Redis/Memcached) 
# have longer TTLs than the local In-Memory cache (InApp).

INAPP_TTL=10
MEMCACHE_TTL=30
REDIS_TTL=60

# ----------------------------------------------------------------------
# APPLICATION/API CONFIGURATION
# ----------------------------------------------------------------------

# This URL is used by the fetch function to retrieve the actual data 
# when a cache miss occurs across all layers.
API_URL_TO_CACHE=[https://get.taaghche.com/v2/book/](https://get.taaghche.com/v2/book/)

# ----------------------------------------------------------------------
# SERVICE CONNECTION CONFIGURATION (Defined in docker-compose.yml)
# ----------------------------------------------------------------------

REDIS_URL=redis://redis:6379/1

MEMCACHE_HOST=memcached
MEMCACHE_PORT=11211
```

Adjust TTLs, layer order, and API url as needed.

### 3. Install Python requirements (for local development)
```bash
pip install -r requirements.txt
```
## 4. Run with Docker Compose
```bash
docker-compose build
docker-compose up
```
Starts Django, Redis, and Memcached containers.
Restart containers to apply .env changes:
```bash
docker-compose down
docker-compose up
```
## Customization
- Add new layers: Create a class inheriting `CacheBase` and implement get and set.
- Change layer order: Edit `CACHE_LAYERS` in `.env`.
- Adjust TTLs: Edit `INAPP_TTL`, `MEMCACHE_TTL`, `REDIS_TTL` in `.env`.
- Use any API: Provide a custom fetch function in `build_cache_manager(fetch_func)`.


