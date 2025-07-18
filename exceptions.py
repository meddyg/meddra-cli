class MedDRAProcessingError(Exception):
    """Base exception for MedDRA processing errors."""
    pass

class UnsupportedFileTypeError(MedDRAProcessingError):
    """Raised when trying to process an unsupported file type."""
    def __init__(self, file_type: str):
        self.file_type = file_type
        super().__init__(f"Unsupported file type: '{file_type}'")

class FileProcessingError(MedDRAProcessingError):
    """Raised when file processing fails."""
    def __init__(self, file_path: str, original_error: Exception):
        self.file_path = file_path
        self.original_error = original_error
        super().__init__(f"Error processing file '{file_path}': {original_error}")

class BatchProcessingError(MedDRAProcessingError):
    """Raised when batch processing fails."""
    def __init__(self, batch_number: int, original_error: Exception):
        self.batch_number = batch_number
        self.original_error = original_error
        super().__init__(f"Error processing batch {batch_number}: {original_error}")

class DatabaseConnectionError(MedDRAProcessingError):
    """Raised when database connection fails."""
    def __init__(self, db_url: str, original_error: Exception):
        self.db_url = db_url
        self.original_error = original_error
        super().__init__(f"Error connecting to database: {original_error}")

class InvalidConfigurationError(MedDRAProcessingError):
    """Raised when configuration is invalid."""
    pass