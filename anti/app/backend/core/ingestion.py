import os
from pypdf import PdfReader
from typing import List, Dict

class IngestionService:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_file(self, file_path: str) -> str:
        """Loads content from a file (PDF or TXT)."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.lower().endswith(".pdf"):
            return self._read_pdf(file_path)
        elif file_path.lower().endswith(".txt"):
            return self._read_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

    def _read_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            extract = page.extract_text()
            if extract:
                text += extract + "\n"
        return text

    def _read_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def clean_text(self, text: str) -> str:
        """Basic text cleaning."""
        # Remove excessive newlines and whitespace
        text = " ".join(text.split())
        return text

    def chunk_text(self, text: str) -> List[str]:
        """Splits text into chunks with overlap."""
        if not text:
            return []

        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk = " ".join(chunk_words)
            if chunk:
                chunks.append(chunk)
                
        return chunks

if __name__ == "__main__":
    # Test
    service = IngestionService()
    print("Ingestion Service Initialized")
