
# Delivery Service

### Service for package managing and delivery costs calculating

Project based on FastAPI, SQLAlchemy, MySQL, Docker


## Requirements
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## Project Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PvtJoker91/delivery_service.git
   cd delivery_service

2. Install all required packages in `Requirements` section 

3. Configure your environment settings:
   - rename .env.example to .env
   - set your variables in .env

### Implemented Commands

* `make all` - up application and database/infrastructure
* `make app-logs` - follow the logs in app container
* `make down` - down application and all infrastructure
* `make db` - up only storages
* `make workers` - up redis, workers

### Most Used Django Specific Commands

* `make migrate` - make migrations to models
* `make tests` - run all tests