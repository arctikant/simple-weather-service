# Simple Weather Service with OpenWeather and AWS stack

## Considerations
- I decided to use `aiobotocore` as a compromise because of its async nature and relative maturity compared to `aioboto3` and `boto3`. If I run into any problems in the future I would look at `boto3` coupled with thread executors. If `aioboto3`. If `aioboto3` gets more popularity and community, I would consider it as a higher level and more elegant solution.
- I decided to use lookup to the DynamoDB to check the existence of cached data in S3 since S3 is not optimized for fast lookup and response. I hope this does not violate the requirements, as the presence of a log may indicate that data in S3 exists. In fact, neither S3 nor DynamoDB is not the best choice as a cache provider for high load applications. It is worth considering using an in-memory DB for this purpose
- I've slightly changed the url to `/api/v1/weather` to make it more like a production app and show versioning. Hopefully that's not a problem either.
- I've only written a few integration tests, omitting the routine unit tests to demonstrate a more complete test setup and its use. For a production application it is definitely worth covering with tests all services, repositories and storages.
- I have not provided a setup for some Reverse proxy/Load Balancer like Nginx, for example, because as I understand from the task requirements the focus is on the application itself. For production apps I should definitely use some kind of such server.

## Running the Project
1. Ensure that Docker and Docker Compose are installed on your system
2. Copy `.sample.env` into `.env` and update configuration parameters
3. Build app image `docker compose build`
4. Run server `docker compose up

## Testing, static analysis, formatting

#### Ruff
- `ruff check .` to check without fix
- `ruff check --fix .` to check and fix
- `ruff format .` to format

#### Mypy
- `mypy .` to check typing

#### PyTest
- Use `.test.env` to set configuration parameters for testing environment
- `docker compose exec app pytest` to run tests