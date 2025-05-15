# TODO

## Rearchitecture

- One GoPro object; not wired and wireless
- Connections can be added / removed at any time; not just configured at instantiation
- all constants, protos, settings, etc. should come from one import
- create per-endpoint, etc operations that mux between BLE and HTTP
  - same for settings. HTTP should be able to get an individual setting.
- Inject database interface to remove TinyDB dependency