from abc import ABC, abstractmethod
from typing import List, Dict, Any
from config import ProcessingConfig
from database.connection import DatabaseManager
from utils.progress import ProgressTracker

class BaseProcessor(ABC):
    """Abstract base class for all processors."""
    
    def __init__(self, db_manager: DatabaseManager, config: ProcessingConfig):
        self.db_manager = db_manager
        self.config = config
        self.progress_tracker = None
        
    @abstractmethod
    def process(self, *args, **kwargs) -> Dict[str, Any]:
        """Main processing method to be implemented by subclasses."""
        pass
    
    def _create_progress_tracker(self, total_items: int, operation_name: str) -> ProgressTracker:
        """Creates a progress tracker for the operation."""
        self.progress_tracker = ProgressTracker(total_items, operation_name)
        return self.progress_tracker
    
    def _log_start(self, operation_name: str, **details) -> None:
        """Logs the start of an operation."""
        print(f"Starting {operation_name}...")
        for key, value in details.items():
            print(f"  {key}: {value}")
    
    def _log_completion(self, operation_name: str, **details) -> None:
        """Logs the completion of an operation."""
        print(f"Completed {operation_name}")
        for key, value in details.items():
            print(f"  {key}: {value}")
    
    def _log_error(self, operation_name: str, error: Exception) -> None:
        """Logs an error during operation."""
        print(f"Error during {operation_name}: {error}")
    
    def validate_prerequisites(self) -> None:
        """Validates that all prerequisites are met before processing."""
        if not self.db_manager.test_connection():
            raise ConnectionError("Database connection test failed")

class ProcessorResult:
    """Represents the result of a processing operation."""
    
    def __init__(self, success: bool, records_processed: int = 0, 
                 error: Exception = None, details: Dict[str, Any] = None):
        self.success = success
        self.records_processed = records_processed
        self.error = error
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.success:
            return f"Success: {self.records_processed} records processed"
        else:
            return f"Failed: {self.error}"