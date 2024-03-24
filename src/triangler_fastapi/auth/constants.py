HASH_SALT_N_BYTES = 32
HASH_ALGORITHM = "sha256"
HASH_ITERATIONS = 100_000

# openssl rand -hex 32
# TODO: This should come from an environment variables (config module).
JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # noqa: S105
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
