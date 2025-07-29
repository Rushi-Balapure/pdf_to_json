# PDF Extraction System Usage Examples

## Basic Usage
```bash
# Build the container
chmod +x build.sh
./build.sh

# Extract from a single PDF
docker run --rm -v $(pwd)/pdfs:/pdfs pdf-extractor:latest /pdfs/document.pdf

# Process multiple PDFs with output redirection
docker run --rm -v $(pwd)/pdfs:/pdfs pdf-extractor:latest /pdfs/document.pdf > output.json
```

## Batch Processing
```bash
# Process all PDFs in a directory
for pdf in pdfs/*.pdf; do
    echo "Processing: $pdf"
    docker run --rm -v $(pwd)/pdfs:/pdfs pdf-extractor:latest "/pdfs/$(basename "$pdf")" > "output/$(basename "$pdf" .pdf).json"
done
```

## Performance Testing
```bash
# Test with a 50-page PDF
time docker run --rm -v $(pwd)/test:/test pdf-extractor:latest /test/50-page-document.pdf
```

## Expected Output Format
```json
{
  "title": "Document Title Here",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction"
    },
    {
      "level": "H2", 
      "text": "1.1 Overview"
    },
    {
      "level": "content",
      "text": "This is the main body text content..."
    }
  ],
  "processing_time": 2.34,
  "page_count": 50
}
```
