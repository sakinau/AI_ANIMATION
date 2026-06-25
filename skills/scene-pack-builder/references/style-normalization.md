# Style Normalization

Use this reference when ComfyUI outputs do not match the current animation library style.

## Current Strategy

Do not replace the whole asset library with ComfyUI output yet. Use ComfyUI to fill gaps first:

- new backgrounds;
- close-up inserts;
- props;
- foreground occlusion layers;
- style exploration candidates.

Every generated file must pass through:

```text
incoming/comfyui/raw
  -> candidates
  -> selected
  -> normalize
  -> register_asset
  -> preview
  -> validate
```

## Style Baseline

Choose one explicit baseline before batch generation:

- **Current free-library baseline**: match `public/免费素材库` as closely as possible.
- **New ComfyUI baseline**: regenerate full scene packs and eventually characters/props in one style.

For the current project, prefer the free-library baseline until a better unified ComfyUI style is proven.

## Prompt Requirements

For backgrounds that must blend with the free library:

```text
2D cutout animation background, flat readable shapes, clean cartoon line art,
moderate detail, simple shadows, muted colors, no characters, no text,
not photorealistic, not 3D render
```

For props:

```text
single object, 2D cutout animation prop, transparent background,
clean thick outline, simple flat colors, centered, no hand, no person,
no text unless requested
```

Negative prompt:

```text
photo, realistic, 3d, complex painterly rendering, noisy texture, character,
people, watermark, logo, text, blurry, low quality, over-detailed
```

## Preferred Generation Modes

Use these in order:

1. **Reference-guided img2img**: use an existing approved background or prop as style reference.
2. **Lineart/Canny controlled generation**: preserve simple geometry and readable silhouettes.
3. **txt2img exploration**: use only for rough candidates or when no reference exists.
4. **post-process normalization**: resize, crop, flatten color, sharpen outlines, and remove background.

## Acceptance Checks

Reject or regenerate assets when:

- line density is much higher than the baseline;
- color temperature clashes with existing characters;
- perspective is too extreme for reusable staging;
- prop shapes are fused into background;
- props lack transparent alpha;
- image contains accidental text or characters;
- foreground occlusion layer includes floor/wall/background that should stay transparent.

## Scene-Pack Rule

Never register a raw ComfyUI output directly into production keys such as `wide` or `phone.table` unless it has been previewed against characters and existing props.

Use exploratory keys first:

```yaml
backgrounds:
  comfy_school_wide: backgrounds/comfy_school_wide.png
```

Promote it to `wide` only after visual review.
