from pathlib import Path
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN


def parse_deck_text(text: str):
    """Parse a deck text file into slide blocks.

    Example block:
      Slide 1 — Title
      - Title: My product
      - Subtitle: Something

      Speaker notes:
      Intro text
    """
    blocks = []
    current = []
    for line in text.splitlines():
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
            continue
        current.append(line.rstrip())
    if current:
        blocks.append(current)

    slides = []
    for block in blocks:
        title = None
        bullets = []
        notes = []
        for line in block:
            if line.startswith("Slide "):
                title = line.split("—", 1)[1].strip() if "—" in line else line
                continue
            if line.startswith("Speaker notes"):
                notes_started = True
                continue
            if notes_started:
                notes.append(line)
                continue
            if line.startswith("-"):
                bullets.append(line[2:].strip())
            elif line and not title:
                title = line.strip()
        slides.append({"title": title or "Untitled", "bullets": bullets, "notes": notes})
    return slides


def create_presentation_from_file(input_path: Path, output_path: Path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    deck_text = input_path.read_text(encoding="utf-8")
    slides = parse_deck_text(deck_text)

    for slide_data in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.25), Inches(12.0), Inches(0.7))
        title_tf = title_box.text_frame
        title_tf.text = slide_data["title"]
        title_tf.paragraphs[0].alignment = PP_ALIGN.LEFT

        body_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.1), Inches(11.8), Inches(4.8))
        body_tf = body_box.text_frame
        body_tf.word_wrap = True
        for i, bullet in enumerate(slide_data["bullets"]):
            p = body_tf.paragraphs[0] if i == 0 else body_tf.add_paragraph()
            p.text = bullet
            p.level = 0
            p.bullet = True

        notes_text = "\n".join(slide_data["notes"]) if slide_data["notes"] else "Speaker notes: see deck source text"
        notes_box = slide.shapes.add_textbox(Inches(0.7), Inches(5.8), Inches(12.0), Inches(1.0))
        notes_tf = notes_box.text_frame
        notes_tf.text = notes_text[:600]
        notes_tf.word_wrap = True

    prs.save(str(output_path))


def main():
    deck_dir = Path(__file__).resolve().parent.parent / "decks"
    for deck_file in sorted(deck_dir.glob("*.txt")):
        if deck_file.name.endswith(".txt"):
            output = deck_dir / deck_file.name.replace(".txt", ".pptx")
            create_presentation_from_file(deck_file, output)
            print(f"Created: {output}")


if __name__ == "__main__":
    main()
