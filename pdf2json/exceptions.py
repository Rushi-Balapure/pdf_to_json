"""
Custom exceptions for PDF2JSON library.
"""

class PDF2JSONError(Exception):
    """Base exception for PDF2JSON library."""
    pass

class PDFProcessingError(PDF2JSONError):
    """Raised when PDF processing fails."""
    pass

class InvalidPDFError(PDF2JSONError):
    """Raised when the PDF file is invalid or corrupted."""
    pass

class FileNotFoundError(PDF2JSONError):
    """Raised when the PDF file is not found."""
    pass
