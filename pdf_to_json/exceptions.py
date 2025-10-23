"""
Custom exceptions for pdf-to-json library.
"""

class PdfToJsonError(Exception):
    """Base exception for pdf-to-json library."""
    pass

class PDFProcessingError(PdfToJsonError):
    """Raised when PDF processing fails."""
    pass

class InvalidPDFError(PdfToJsonError):
    """Raised when the PDF file is invalid or corrupted."""
    pass

class FileNotFoundError(PdfToJsonError):
    """Raised when the PDF file is not found."""
    pass
