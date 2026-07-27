# Presentation Asset Guide

Status: current for the v0.11 logical-rendering contract

## Purpose

The current presentation layer includes a deliberately small set of replaceable image and sound assets. The runtime loads files by stable asset ID through `UIResources` and keeps rectangle drawing as a fallback when a file is missing or invalid.

All scene and UI art is authored for the fixed `1280 x 720` logical frame. The completed frame is scaled uniformly to fullscreen or an approved window size, so runtime assets do not need physical-resolution variants.

Do not add an asset manifest, atlas system, animation format, or external pipeline until production asset volume demonstrates the need.

## Image format

Required runtime format:

```txt
PNG
assets/images/<asset_id>.png
```

Recommendations:

- use RGB PNG for full-screen backgrounds
- use RGBA PNG with transparent backgrounds for NPCs, items, objects, and exits
- keep important artwork away from the lowest part of a sprite because the game draws a readable label strip there
- export at the recommended size or larger; the game scales the image to the target rectangle
- use standard sRGB color
- avoid baked-in text because labels are rendered by the game

### Background assets

Recommended size:

```txt
1280 x 720 pixels
```

Current IDs:

```txt
screen.title
scene.village_square
scene.forest_path
scene.tower_interior
```

Backgrounds are scaled to the complete logical `1280 x 720` frame. Keep the upper-left area readable for scene title/description text and the upper-right area relatively quiet for the inventory panel.

### Sprite and object assets

Current recommended canvas sizes:

```txt
object.notice_board       240 x 120
object.old_well           180 x 100
item.empty_cup            180 x 80 target; 128 x 128 source is acceptable
npc.retired_witch         190 x 180 target; portrait or full-body crop
exit.path                 190 x 100
npc.mushroom_guard        170 x 150
item.moon_herb            180 x 100 target; 128 x 128 source is acceptable
object.suspicious_stump   240 x 120
exit.tower_gate           220 x 100 target; wider source is acceptable
object.ancient_pedestal   320 x 180
```

The current loader scales each asset to its clickable rectangle. Preserve the approximate aspect ratio when replacing files to avoid distortion.

## Audio format

Required runtime format:

```txt
Ogg Vorbis
assets/audio/<asset_id>.ogg
```

Recommended export settings:

```txt
sample rate:       44.1 kHz
channels:          mono
sample format:     16-bit source or better
Vorbis quality:    approximately q4-q6
leading silence:   none
peak level:        below 0 dBFS
```

Current sound IDs and suggested durations:

```txt
sfx.pickup             0.15-0.35 seconds
sfx.dialogue           0.05-0.20 seconds
sfx.unlock             0.30-0.80 seconds
sfx.scene_transition   0.20-0.60 seconds
```

Sound direction:

- `sfx.pickup`: light, positive, and readable without being sharp
- `sfx.dialogue`: subtle page/tick/chime suitable for repeated dialogue lines
- `sfx.unlock`: heavier mechanical or magical confirmation
- `sfx.scene_transition`: short whoosh, step, or magical travel cue

Keep effects short because the current system plays them directly without channel management, ducking, looping, or music mixing.

## Replacing an asset

1. Keep the exact filename and extension.
2. Replace the file under `assets/images/` or `assets/audio/`.
3. Run the game and check scaling, readability, volume, and clipping.
4. Run `make check` to confirm code/tests remain unchanged.

No code change is required when the stable asset ID and file format stay the same.

## Current fallback behavior

- missing image: the entity uses its colored placeholder panel
- invalid image: the entity uses its colored placeholder panel
- missing sound: the interaction remains silent
- unavailable audio mixer: gameplay continues without sound

This fallback is intentional for development and automated tests.

## Logical-resolution and source-art guidance

The implemented display contract is:

```txt
logical composition: 1280 x 720
startup output:       fullscreen desktop
windowed presets:     1280 x 720, 1600 x 900, 1920 x 1080
aspect behavior:      uniform scaling with letterboxing/pillarboxing
```

The game draws title, Controls, gameplay, ending, and debug presentation into one logical surface. It then scales that complete surface once. Individual sprites, labels, hitboxes, and UI panels are not independently resized for the physical monitor.

For newly created backgrounds:

```txt
composition:          16:9
recommended master:  2560 x 1440 or larger
runtime PNG:          1280 x 720
```

Keep editable high-resolution source files outside the runtime asset directory. Export optimized runtime PNG files under the existing stable asset IDs.

For sprites and objects:

- keep transparent source masters at roughly twice the expected logical display size when practical
- preserve enough empty padding for hover outlines and label strips
- avoid very thin details that disappear after downscaling or fullscreen presentation
- preserve the approximate aspect ratio of the clickable logical rectangle
- do not create separate files for `1600 x 900`, `1920 x 1080`, or individual monitor sizes

For text and baked-in detail:

- avoid baking interaction labels or dialogue into scene art
- judge readability at the logical `1280 x 720` frame first
- verify the result in fullscreen and at every approved windowed size
- remember that the current presentation path uses smooth scaling for the complete frame

Asset authors should not compensate for letterboxing or physical monitor dimensions inside scene artwork. Black unused space belongs to the display presentation layer, not to background PNG files.
