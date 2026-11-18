## 1.1.0

Added optional automatic join tone matching. Connect the encoded previous segment to `tone_reference` and Lokken measures the brightness step at the join, then brightens or darkens the incoming segment during H.264 encoding.

- Preserves frame timing, chroma, and audio.
- Existing workflows keep their current encoding behavior when the new input is unused.
- No new dependencies.
