#!/usr/bin/env python3
"""Render PPTX slides to PNG using PowerPoint COM interface."""
import sys
import os
from pathlib import Path
import comtypes.client

def render_pptx(pptx_path, output_dir):
    """Render all slides in PPTX to PNG files."""
    pptx_path = Path(pptx_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Opening: {pptx_path}")
    print(f"Output: {output_dir}")

    # Create PowerPoint application
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1

    try:
        # Open presentation
        presentation = powerpoint.Presentations.Open(str(pptx_path), WithWindow=False)

        # Export each slide as PNG
        slide_count = presentation.Slides.Count
        for i, slide in enumerate(presentation.Slides, 1):
            output_path = output_dir / f"slide_{i:02d}.png"
            slide.Export(str(output_path), "PNG", 1600, 900)
            print(f"Rendered slide {i}/{slide_count}")

        presentation.Close()
        print(f"\nRendered {slide_count} slides to {output_dir}")

    finally:
        powerpoint.Quit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_slides.py <pptx_path> <output_dir>")
        sys.exit(1)

    render_pptx(sys.argv[1], sys.argv[2])
