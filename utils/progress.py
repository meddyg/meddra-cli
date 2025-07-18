from typing import Optional
from datetime import datetime

class ProgressTracker:
    """Tracks progress of batch processing operations."""
    
    def __init__(self, total_items: int, operation_name: str = "Processing"):
        self.total_items = total_items
        self.operation_name = operation_name
        self.processed_items = 0
        self.current_batch = 0
        self.start_time = datetime.now()
        
    def update(self, batch_number: int, batch_size: int, items_processed: int) -> None:
        """Updates progress tracking."""

        self.current_batch = batch_number
        self.processed_items = items_processed
        
    def get_progress_percentage(self) -> int:
        """Calculates progress percentage."""
        if self.total_items == 0:
            return 100

        return min(100, int((self.processed_items / self.total_items) * 100))
    
    def get_elapsed_time(self) -> float:
        """Gets elapsed time in seconds."""
        return (datetime.now() - self.start_time).total_seconds()
    
    def get_estimated_time_remaining(self) -> Optional[float]:
        """Estimates remaining time in seconds."""
        if self.processed_items == 0:
            return None
        
        elapsed = self.get_elapsed_time()
        rate = self.processed_items / elapsed
        remaining_items = self.total_items - self.processed_items
        
        if rate > 0:
            return remaining_items / rate
        return None
    
    def format_progress_message(self) -> str:
        """Formats a progress message."""
        percentage = self.get_progress_percentage()
        elapsed = self.get_elapsed_time()
        
        message = f"Progress: {percentage}% - Batch {self.current_batch} ({self.processed_items}/{self.total_items} records)"
        message += f" - Elapsed: {elapsed:.1f}s"
        
        eta = self.get_estimated_time_remaining()
        if eta:
            message += f" - ETA: {eta:.1f}s"
            
        return message
    
    def print_progress(self) -> None:
        """Prints current progress."""
        print(self.format_progress_message())
    
    def is_complete(self) -> bool:
        """Checks if processing is complete."""
        return self.processed_items >= self.total_items

def format_file_size(size_bytes: int) -> str:
    """Formats file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_duration(seconds: float) -> str:
    """Formats duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"