import json
import io
import os
import sys
import time
from typing import Dict, List, Any, Optional
import fitz  # PyMuPDF
from dataclasses import dataclass
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FontInfo:
    size: float
    name: str
    flags: int

@dataclass
class TextSpan:
    text: str
    font_info: FontInfo
    bbox: tuple
    level: Optional[str] = None

class PDFStructureExtractor:
    """
    High-performance PDF structure extractor optimized for CPU processing.
    Supports multilingual text extraction and heading detection based on font analysis.
    """

    def __init__(self):
        self.font_size_histogram = defaultdict(int)
        self.heading_levels = {}

    def analyze_font_sizes(self, doc: fitz.Document) -> Dict[float, int]:
        """Analyze font sizes across the document to determine heading levels."""
        font_histogram = defaultdict(int)
        total_chars = 0

        for page_num in range(min(len(doc), 10)):  # Sample first 10 pages for speed
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["text"].strip():
                            font_size = round(span["size"], 1)
                            char_count = len(span["text"])
                            font_histogram[font_size] += char_count
                            total_chars += char_count

        # Determine heading levels based on frequency and size
        sorted_fonts = sorted(font_histogram.items(), key=lambda x: x[0], reverse=True)

        # Main text is likely the most frequent font size
        if sorted_fonts:
            main_font_size = max(font_histogram.items(), key=lambda x: x[1])[0]

            heading_levels = {}
            level = 1

            for font_size, count in sorted_fonts:
                # Consider as heading if font is larger than main text and not too rare
                if font_size > main_font_size and count > total_chars * 0.001:
                    heading_levels[font_size] = f"H{min(level, 6)}"
                    level += 1

        return font_histogram, heading_levels

    def extract_text_with_structure(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract text with hierarchical structure from PDF.
        Returns JSON format with title and outline.
        """
        start_time = time.time()

        try:
            doc = fitz.open(pdf_path)

            # Analyze font sizes for heading detection
            font_histogram, heading_levels = self.analyze_font_sizes(doc)

            # Extract document title (usually from first page, largest non-body font)
            title = self._extract_title(doc, heading_levels)

            # Extract structured content
            outline = []
            current_section = None

            for page_num in range(len(doc)):
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]

                for block in blocks:
                    if "lines" not in block:
                        continue

                    for line in block["lines"]:
                        line_text = ""
                        line_font_size = 0

                        for span in line["spans"]:
                            if span["text"].strip():
                                line_text += span["text"]
                                line_font_size = max(line_font_size, span["size"])

                        if line_text.strip():
                            # Determine if this is a heading
                            rounded_size = round(line_font_size, 1)
                            level = heading_levels.get(rounded_size)

                            if level:
                                outline.append({
                                    "level": level,
                                    "text": line_text.strip()
                                })
                            else:
                                # Regular text - could be added to content if needed
                                if current_section is None:
                                    current_section = {
                                        "level": "content",
                                        "text": line_text.strip()
                                    }
                                    outline.append(current_section)
                                else:
                                    if current_section.get("level") == "content":
                                        current_section["text"] += " " + line_text.strip()

            doc.close()

            processing_time = time.time() - start_time
            logger.info(f"Processing completed in {processing_time:.2f} seconds")

            return {
                "title": title,
                "outline": outline,
                "processing_time": processing_time,
                "page_count": len(doc)
            }

        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            return {
                "title": "Error extracting title",
                "outline": [{"level": "error", "text": str(e)}],
                "processing_time": time.time() - start_time,
                "page_count": 0
            }

    def _extract_title(self, doc: fitz.Document, heading_levels: Dict[float, str]) -> str:
        """Extract document title from first page."""
        if len(doc) == 0:
            return "Untitled Document"

        first_page = doc[0]
        blocks = first_page.get_text("dict")["blocks"]

        # Look for the largest text on the first page
        largest_text = ""
        largest_size = 0

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"].strip() and span["size"] > largest_size:
                        largest_size = span["size"]
                        largest_text = span["text"].strip()

        return largest_text if largest_text else "Untitled Document"

def main():
    """Main function to process PDF and return JSON."""
    if len(sys.argv) != 2:
        print("Usage: python pdf_extractor.py <pdf_file_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found")
        sys.exit(1)

    extractor = PDFStructureExtractor()
    result = extractor.extract_text_with_structure(pdf_path)

    # Output as JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()