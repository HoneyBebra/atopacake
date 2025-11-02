# Atopacake

# DB scheme
[API service](atopacake_api/README.md)

[Auth service](auth/README.md)

# Architecture
```         
              ┌─NginxGateway─┐      ┌─AtopacakeAPI─────────────────────────────────────────┐
    user ───→ │              ├───┐  │  ┌─NginxAtopacakeApi─┐                               │
              └────┬─────────┘   └──┼─→│                   │                               │
                   │                │  └───────────────┬───┘                               │
                   │                │                  │                                   │
                   │                │                  ↓                                   │
                   │                │  ┌─FastApiApp─────────┐                              │
                   │                │  │ Cards schema       │       ┌─PostgresAtopacake─┐  │
                   │                │  │ Texts schema       ├─────→ │                   │  │
                   │                │  │ Directories schema │       └───────────────────┘  │
                   │                │  └────────────────────┘                              │
                   │                │                                                      │  
                   │                └──────────────────────────────────────────────────────┘
                   ↓
    ┌─Auth─────────────────────────────────┐             
    │ ┌─NginxAuth─┐                        │
    │ │           │                        │
    │ └────┬──────┘                        │
    │      ↓                               │                    
    │ ┌─FastApiApp───┐    ┌─PostgresAuth─┐ │           
    │ │ Users schema ├───→│              │ │
    │ └─────┬────────┘    └──────────────┘ │
    │       │             ┌─RedisAuth─┐    │
    │       └────────────→│           │    │
    │                     └───────────┘    │
    └──────────────────────────────────────┘                   
```
