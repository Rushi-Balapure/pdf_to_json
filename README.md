# Layout-Aware PDF Extraction System

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

## Overview

This project implements a **Layout-Aware PDF Extraction System** inspired by the paper:

**"Layout-Aware Text Extraction from Full-text PDF of Scientific Articles"**  
_Cartic Ramakrishnan, Abhishek Patnia, Eduard Hovy, Gully APC Burns_  
Published in Source Code for Biology and Medicine (2012)  
[Full Paper](http://www.scfbm.org/content/7/1/7)

The system extracts structured information from PDF documents while preserving document layout semantics such as headings (H1-H6) and body text, outputting the extracted content as JSON. It is optimized for high performance on CPU-only AMD64 architectures, supports multilingual text, and requires no internet access during runtime.

## Features

- **Layout-aware extraction**: Detects document structure including headings of different levels using font size and style analysis.
- **Multilingual support**: Handles Latin, Cyrillic, Asian scripts (Chinese, Japanese, Korean), Arabic, Hebrew, and other complex Unicode scripts.
- **High performance**: Processes 50-page PDFs in ≤10 seconds on modern CPUs.
- **Small footprint**: Docker image size under 200MB, no heavy ML models used.
- **Offline operation**: No internet connectivity required to run.
- **Cross-platform CPU support**: AMD64 compatible, runs purely on CPU.

## JSON Output Example
```json
{
"title": "Document Title Here",
"outline": [
{ "level": "H1", "text": "Chapter 1: Introduction" },
{ "level": "H2", "text": "1.1 Overview" },
{ "level": "content", "text": "Body text content..." }
],
"processing_time": 2.34,
"page_count": 50
}
```

## Getting Started

### Prerequisites

- Docker installed on an AMD64 machine
- PDF documents to process

### Building the Docker Image

You can build the extraction system Docker image with the provided build script:
```bash
chmod +x build.sh
./build.sh
```

This builds the Docker container optimized for CPU-only usage and minimal size.

### Running the Extraction

To extract text from a PDF, mount your PDF directory and run:
```bash
docker run --rm -v /path/to/pdfs:/pdfs pdf-extractor:latest /pdfs/document.pdf
```
The output JSON is printed to stdout. To save the output to a file:
```bash
docker run --rm -v /path/to/pdfs:/pdfs pdf-extractor:latest /pdfs/document.pdf > output.json
```

## System Architecture

The system is built using [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/) for robust text and font extraction without requiring internet or GPUs. The heading detection algorithm analyses font size histograms on initial pages to classify headings from H1 to H6.

## License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

## References

Ramakrishnan, C., Patnia, A., Hovy, E., Burns, G. A. P. C. (2012). Layout-aware text extraction from full-text PDF of scientific articles. _Source Code for Biology and Medicine, 7_(7). https://doi.org/10.1186/1751-0473-7-7

## Contact

For questions or contributions, feel free to open an issue or contact the me(rishibalapure12@gmail.com)
