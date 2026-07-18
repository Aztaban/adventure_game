# Presentation Asset Guide

Status: v0.10 placeholder asset contract

## Purpose

The v0.10 presentation pass includes a deliberately small set of replaceable image and sound assets. The runtime loads files by stable asset ID through `UIResources` and keeps the existing rectangle drawing as a fallback when a file is missing or invalid.

Do not add an asset manifest, atlas system, animation format, or external pipeline for this milestone.

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

Backgrounds are scaled to the complete window. Keep the upper-left area readable for scene title/description text and the upper-right area relatively quiet for the inventory panel.

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

## Preparing source art for future display scaling

The current runtime contract remains `1280 x 720`, but v0.11 is planned to present that logical resolution at larger physical window sizes and fullscreen.

For newly created backgrounds:

```txt
composition:          16:9
recommended master:  2560 x 1440 or larger
current runtime PNG: 1280 x 720
```

Keep editable high-resolution source files outside the runtime asset directory. Export optimized runtime PNG files under the existing stable asset IDs.

For sprites and objects:

- keep transparent source masters at roughly twice the expected runtime display size when practical
- preserve enough empty padding for hover outlines and label strips
- avoid very thin details that disappear when the logical surface is scaled down
- do not create separate files for every physical screen resolution

The display layer should scale the complete logical composition uniformly. Asset authors should not compensate for letterboxing or physical window dimensions inside scene artwork.
