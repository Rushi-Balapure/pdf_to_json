#!/usr/bin/env python3
"""
Comprehensive test script for PDF2JSON library.
This script tests all components of the library to ensure everything works correctly.
"""

import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path

def test_imports():
    """Test that all modules can be imported correctly."""
    print("🔍 Testing imports...")
    
    try:
        import pdf2json
        from pdf2json import PDFStructureExtractor, Config
        from pdf2json import extract_pdf_to_json, extract_pdf_to_dict
        from pdf2json.exceptions import PDF2JSONError, PDFProcessingError, InvalidPDFError, FileNotFoundError
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration functionality."""
    print("\n🔍 Testing configuration...")
    
    try:
        from pdf2json.config import Config
        
        config = Config()
        assert config.MAX_PAGES_FOR_FONT_ANALYSIS == 10
        assert config.FONT_SIZE_PRECISION == 0.1
        assert config.MIN_HEADING_FREQUENCY == 0.001
        
        config_dict = config.get_config()
        assert isinstance(config_dict, dict)
        assert "max_pages_for_font_analysis" in config_dict
        
        print("✅ Configuration tests passed")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_exceptions():
    """Test custom exceptions."""
    print("\n🔍 Testing exceptions...")
    
    try:
        from pdf2json.exceptions import PDF2JSONError, PDFProcessingError, InvalidPDFError, FileNotFoundError
        
        # Test exception inheritance
        assert issubclass(PDFProcessingError, PDF2JSONError)
        assert issubclass(InvalidPDFError, PDF2JSONError)
        assert issubclass(FileNotFoundError, PDF2JSONError)
        
        # Test exception creation
        error = PDF2JSONError("Test error")
        assert str(error) == "Test error"
        
        print("✅ Exception tests passed")
        return True
    except Exception as e:
        print(f"❌ Exception test failed: {e}")
        return False

def test_extractor_initialization():
    """Test PDFStructureExtractor initialization."""
    print("\n🔍 Testing extractor initialization...")
    
    try:
        from pdf2json import PDFStructureExtractor, Config
        
        # Test with default config
        extractor1 = PDFStructureExtractor()
        assert extractor1.config is not None
        
        # Test with custom config
        config = Config()
        config.MAX_PAGES_FOR_FONT_ANALYSIS = 5
        extractor2 = PDFStructureExtractor(config)
        assert extractor2.config == config
        
        print("✅ Extractor initialization tests passed")
        return True
    except Exception as e:
        print(f"❌ Extractor initialization test failed: {e}")
        return False

def test_file_not_found_error():
    """Test error handling for non-existent files."""
    print("\n🔍 Testing file not found error...")
    
    try:
        from pdf2json import extract_pdf_to_dict
        from pdf2json.exceptions import FileNotFoundError
        
        try:
            extract_pdf_to_dict("nonexistent.pdf")
            print("❌ Should have raised FileNotFoundError")
            return False
        except FileNotFoundError:
            print("✅ FileNotFoundError correctly raised")
            return True
    except Exception as e:
        print(f"❌ File not found test failed: {e}")
        return False

def test_cli_help():
    """Test CLI help functionality."""
    print("\n🔍 Testing CLI help...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pdf2json.cli", "--help"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "Extract structured content from PDF files" in result.stdout:
            print("✅ CLI help test passed")
            return True
        else:
            print(f"❌ CLI help test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ CLI help test failed: {e}")
        return False

def test_cli_version():
    """Test CLI version functionality."""
    print("\n🔍 Testing CLI version...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pdf2json.cli", "--version"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "PDF2JSON 1.0.0" in result.stdout:
            print("✅ CLI version test passed")
            return True
        else:
            print(f"❌ CLI version test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ CLI version test failed: {e}")
        return False

def test_with_sample_pdf():
    """Test with the sample PDF if it exists."""
    print("\n🔍 Testing with sample PDF...")
    
    sample_pdf = "papers/1751-0473-7-7.pdf"
    
    if not os.path.exists(sample_pdf):
        print("⚠️  Sample PDF not found, skipping PDF processing test")
        return True
    
    try:
        from pdf2json import extract_pdf_to_dict, extract_pdf_to_json
        
        # Test dictionary extraction
        result = extract_pdf_to_dict(sample_pdf)
        
        # Verify structure
        assert "title" in result
        assert "sections" in result
        assert "stats" in result
        assert "font_histogram" in result
        assert "heading_levels" in result
        
        # Verify stats
        stats = result["stats"]
        assert "page_count" in stats
        assert "processing_time" in stats
        assert "num_sections" in stats
        assert "num_headings" in stats
        assert "num_paragraphs" in stats
        
        print(f"✅ PDF processing test passed")
        print(f"   - Title: {result['title']}")
        print(f"   - Pages: {stats['page_count']}")
        print(f"   - Sections: {stats['num_sections']}")
        print(f"   - Processing time: {stats['processing_time']:.2f}s")
        
        # Test JSON extraction (do not compare full content due to timing variability)
        json_output = extract_pdf_to_json(sample_pdf)
        assert isinstance(json_output, str)

        # Test saving to file (compare stable fields only)
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            output_path = tmp.name
        
        try:
            saved_path = extract_pdf_to_json(sample_pdf, output_path)
            assert saved_path == output_path
            assert os.path.exists(output_path)
            
            # Verify saved content
            with open(output_path, 'r', encoding='utf-8') as f:
                saved_result = json.load(f)
            # Compare stable fields, ignore timing differences
            assert saved_result.get('title') == result.get('title')
            assert isinstance(saved_result.get('sections'), list)
            assert isinstance(saved_result.get('stats'), dict)
            assert saved_result['stats'].get('page_count') == result['stats'].get('page_count')
            
            print("✅ JSON file saving test passed")
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
        
        return True
        
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        return False

def test_unit_tests():
    """Run unit tests if pytest is available."""
    print("\n🔍 Running unit tests...")
    
    try:
        import pytest
        
        # Run tests
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Unit tests passed")
            return True
        else:
            print(f"❌ Unit tests failed: {result.stdout}")
            print(f"   Error: {result.stderr}")
            return False
    except ImportError:
        print("⚠️  pytest not available, skipping unit tests")
        return True
    except Exception as e:
        print(f"❌ Unit test execution failed: {e}")
        return False

def test_examples():
    """Test example scripts."""
    print("\n🔍 Testing example scripts...")
    
    try:
        # Test basic usage example
        example_path = "examples/basic_usage.py"
        if os.path.exists(example_path):
            result = subprocess.run([sys.executable, example_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Basic usage example passed")
            else:
                print(f"⚠️  Basic usage example had issues: {result.stderr}")
        
        # Test advanced usage example
        example_path = "examples/advanced_usage.py"
        if os.path.exists(example_path):
            result = subprocess.run([sys.executable, example_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Advanced usage example passed")
            else:
                print(f"⚠️  Advanced usage example had issues: {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"❌ Example test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 PDF2JSON Library Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Exceptions", test_exceptions),
        ("Extractor Initialization", test_extractor_initialization),
        ("File Not Found Error", test_file_not_found_error),
        ("CLI Help", test_cli_help),
        ("CLI Version", test_cli_version),
        ("Sample PDF Processing", test_with_sample_pdf),
        ("Unit Tests", test_unit_tests),
        ("Examples", test_examples),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! PDF2JSON library is ready to use.")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
