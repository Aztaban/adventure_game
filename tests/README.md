# Test layers

Use the narrowest test layer that can prove the behavior.

## Pure unit tests

Use for deterministic domain behavior that does not need Pygame rendering or
real demo scenes. Examples: inventory, recipes, state snapshots, item use,
item-combination, JSON loading helpers, and interaction-service decisions.

## Integration tests

Use when the real demo content or multiple runtime objects must work together.
Examples: complete demo flow, new-game reset, state snapshot round trips,
world-state persistence, and JSON content loading from files.

## Pygame adapter tests

Use for scene event translation, hit testing, target priority, modal dialogue,
hover text, and widget layout. These tests may initialize Pygame fonts, but they
should remain a minority and should avoid hiding gameplay behind large fixtures.

## Manual tests

Use for readability, layout feel, hover feel, audio, visual polish, and ending
presentation. Automated tests should still protect the underlying state changes.
