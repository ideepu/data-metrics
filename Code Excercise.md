# Assignment

Data metric dashboard service

## Getting Started

Ensure you have the following installed on your system:

- python3.13

The project uses uv package manager, install it from [the uv webiste](https://docs.astral.sh/uv/).

## TODO List

1. Config management per environment

    Resolving the config per the environment dynamically based on an environment variable identifier example dev, test, prod, etc. This wil allow us to avoid hardcoding the values and also keep the secrets safe from leaking.
    Any secure information can be injected into the cotainers as env vars and we can possibly use a third party module or implement a custom wrapper to read the required environment variables.
2. Context Management

    A context layer can be build to store the information in the memory and make it accessible thoughout the system. This will let us transfer the information between the layers of the application seemlessly.
    Essentially this will also helps us in the logging and tracing.
3. User Session handling

    Temporary cache storage to persist the information across the request context such as user info, authentication, etc. Avoiding making calls to the database would give us the performance benefits.
4. Database Cache layer

    Caching the retrived information from database in memory unless the invalidated. This is to avoid making calls to the database for the frequently accessed data. The cache layer is invalidated whenever the data is updated and subsequest call to database will cache the results again.
5. Docker image
6. Rate limiting

    Helps us reduce the abuse usage of the endpoints and also let's us track the usage of the system so we can deal with the incoming traffic.
7. CSRF and Security

    This is to protect our application from web attacks such XSS and SQL injections. Enforces that we receieve the traffic over a secured protocal and from trusted domains.
8. Pre commit hooks and linters
9. Gunicorn
    Server for running the application in production.
