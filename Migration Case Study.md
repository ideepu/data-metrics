# Migration Case Study

Currently, API tokens are stored as plain text in the `api_key` field of the `User` model. The goal of this migration is to phase out plain text API tokens and transition to a more secure, flexible system for generating and managing API tokens.

## Key Considerations

1. At present, each user can have only one API key. The new design should allow users to create and manage multiple API keys.
2. Since plain text API tokens are still actively used in production, the new system must maintain compatibility and continue to support them during the transition.

**Current Model:**

```python
class User:
    api_key: str # Plain text keys
    ...
```

## Migration Plan

1. Introduce a new `Token` model to store API tokens in a dedicated `token` table, separating token management from the `User` table and decoupling the `api_key` field from the user model.

    ```python
    from enum import Enum

    class TokenStatus(Enum):
        LEGACY = 'legacy'
        ACTIVE = 'active'
        REVOKED = 'revoked'

    class TokenTargetType(Enum):
        USER = 'user'

    class Token:
        __tablename__: str = 'token'

        id: int
        name: str
        target_type: Enum = mapped_column(index=True)
        target_id: int = mapped_column(index=True)
        api_key: str = mapped_column(index=True)  # Hashed API key
        status: TokenStatus =  mapped_column(index=True)
        expires_at: datetime
        created_at: datetime
        updated_at: datetime
    ```

    - `name`: A user-defined, human-readable label for the token. This allows users to easily distinguish between multiple tokens they have generated, for example, "CI/CD Pipeline Key" or "Personal Key".
    - `target_type`: Specifies the entity to which the token is associated. In the current implementation, this is set to `user`, meaning tokens are only issued for users. This field is designed for future extensibility, allowing tokens to be bound to other entities (such as teams or services) if needed.
    - `target_id`: The unique identifier of the entity (currently a user) that the token is associated with. This links the token to its owner in the database.
    - `api_key`: The API token value, which is stored as a securely hashed string. The raw token is generated randomly and only shown to the user at creation time; it is never stored in plain text. This ensures that tokens remain confidential and can only be validated by comparing hashes, following best practices for secure credential management.
    - `status`: Indicates the current state of the token. Possible values include:
        - `LEGACY`: Token migrated from the old system, still valid for backward compatibility.
        - `ACTIVE`: Token is valid and can be used for authentication.
        - `REVOKED`: Token has been invalidated and can no longer be used.
    - `expires_at`: The date and time when the token will expire. After this timestamp, the token becomes invalid and cannot be used for authentication. This allows for time-limited access and improves security by reducing the risk of long-lived tokens.
    - `created_at`: Timestamp indicating when the token was created. Useful for auditing and tracking the lifecycle of tokens.
    - `updated_at`: Timestamp of the last update to the token record. This is updated whenever any attribute of the token (such as status or expiration) is changed, providing a history of modifications for auditing purposes.

2. Retain the `api_key` field in the `User` model temporarily to ensure backward compatibility. Simultaneously, migrate all existing API keys from the `User` table into the new `Token` table, marking their status as `LEGACY`.
3. Update the authentication logic so that when an API token is presented, the system first attempts to validate it against the new hashed `api_key` entries in the `Token` table. If no match is found, it should then check for a legacy (plain-text) `api_key`, where the token's status is set to `LEGACY`. This approach ensures both new and legacy tokens are supported from a single source during the migration period.
4. Once the migration and transition period is complete, remove the `api_key` field from the `User` model and eliminate any related legacy code.
5. Update the user interface to allow users to create and manage API tokens using the new system. Users should be able to generate new server API tokens, optionally set expiration times during creation, view metadata (such as name, creation date, and expiration date) for their tokens, and revoke tokens as needed.

## Legacy Token Migration and Cleanup

1. Inform users currently utilizing legacy tokens, advising them to rotate their keys and transition to the new API token system.
2. Once legacy tokens are no longer in use, delete them from the `token` table and remove any associated legacy support code.
