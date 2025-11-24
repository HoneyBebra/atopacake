# Main app logic API service

## Deploy

To deploy a separate service:

Create ```.env```-file like ```.env.example```

```shell
docker-compose up -d --build
```

## PostgreSQL schema:
```
        ┌──────────────────────────────────────────────────────────────────────┐
        │  (directories)                                                       │
        │----------------------------------------------------------------------│
        │ name       │ type     │ key         │ is unique │ is null  │ default │
  1:N   │----------------------------------------------------------------------│
   ┌────┤ id         │ UUID     │ primary key │ unique    │ not null │         │
   │    │ user_id    │ UUID     │             │           │ not null │         │ 
   │    │ name       │ string   │             │           │ not null │         │
   │    │ created_at │ datetime │             │           │ not null │         │
   │    │ updated_at │ datetime │             │           │ not null │         │
   │    └──────────────────────────────────────────────────────────────────────┘
   │    
   │    ┌────────────────────────────────────────────────────────────────────────────┐
   │    │  (cards)                                                                   │
   │    │----------------------------------------------------------------------------│
   │    │ name             │ type     │ key         │ is unique │ is null  │ default │
   │    │----------------------------------------------------------------------------│
   │    │ id               │ UUID     │ primary key │ unique    │ not null │         │
   └───→│ directory_id     │ UUID     │ foreign key │           │ not null │         │ 
        │ side_a           │ string   │             │           │ not null │         │
        │ side_b           │ string   │             │           │ not null │         │
        │ weight           │ float    │             │           │          │ 0.5     │
        │ random_mix_sides │ boolean  │             │           │          │ false   │
    ┌──→│ text_id          │ UUID     │ foreign key │           │          │         │
    │   │ created_at       │ datetime │             │           │ not null │         │
    │   │ updated_at       │ datetime │             │           │ not null │         │
    │   └────────────────────────────────────────────────────────────────────────────┘
    │   
    │   ┌──────────────────────────────────────────────────────────────────────┐
    │   │  (texts)                                                             │
    │   │----------------------------------------------------------------------│
    │   │ name       │ type     │ key         │ is unique │ is null  │ default │
    │   │----------------------------------------------------------------------│
    └───┤ id         │ UUID     │ primary key │ unique    │ not null │         │
   1:N  │ text       │ string   │             │           │ not null │         │ 
        │ user_id    │ UUID     │             │           │ not null │         │
        │ created_at │ datetime │             │           │ not null │         │
        │ updated_at │ datetime │             │           │ not null │         │
        └──────────────────────────────────────────────────────────────────────┘
```
