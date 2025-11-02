# Auth service

## Deploy

To deploy a separate service:

Create ```.env```-file like ```.env.example```

```shell
docker-compose up -d --build
```

## PostgreSQL schema:
```
    ┌──────────────────────────────────────────────────────────────────────────────────┐
    │  (users)                                                                         │
    │----------------------------------------------------------------------------------│
    │ name                   │ type     │ key         │ is unique │ is null  │ default │
    │----------------------------------------------------------------------------------│
    │ id                     │ UUID     │ primary key │ unique    │ not null │         │  
    │ login                  │ string   │             │           │ not null │         │
    │ password               │ string   │             │           │ not null │         │
    │ encrypted_phone_number │ string   │             │ unique    │ nullable │         │
    │ phone_number_hash      │ string   │             │ unique    │ nullable │         │
    │ encrypted_email        │ string   │             │ unique    │ nullable │         │
    │ email_hash             │ string   │             │ unique    │ nullable │         │
    │ created_at             │ datetime │             │           │ not null │         │
    │ updated_at             │ datetime │             │           │ not null │         │
    └──────────────────────────────────────────────────────────────────────────────────┘
```
