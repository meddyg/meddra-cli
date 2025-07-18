import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
from core.base import BaseProcessor, ProcessorResult
from core.batch_processor import BatchProcessor
from utils.file_utils import validate_file_path, get_file_info, get_file_type_from_path
from models import generate_meddra_file_mappings
from exceptions import UnsupportedFileTypeError, FileProcessingError

class FileProcessor(BaseProcessor):
    """Processes individual MedDRA files."""
    
    def __init__(self, db_manager, config):
        super().__init__(db_manager, config)
        self.file_mappings = generate_meddra_file_mappings()
        self.batch_processor = BatchProcessor(db_manager, config)
    
    def process(self, file_path: str) -> ProcessorResult:
        """Processes a single MedDRA file."""
        try:
            # Validate file
            validate_file_path(file_path)
            file_info = get_file_info(file_path)
            file_type = get_file_type_from_path(file_path)
            
            # Check if file type is supported
            if file_type not in self.file_mappings:
                raise UnsupportedFileTypeError(file_type)
            
            mapping = self.file_mappings[file_type]
            
            # Log start
            self._log_start(
                f"Processing {file_type} file",
                file_path=file_path,
                file_size=file_info['size'],
                total_lines=file_info['line_count']
            )
            
            # Create progress tracker
            progress_tracker = self._create_progress_tracker(
                file_info['line_count'], 
                f"Processing {file_type}"
            )
            
            # Process file in chunks
            total_records = 0
            batch_count = 0
            
            for df_chunk in self._read_file_chunks(file_path, mapping['columns']):
                batch_count += 1
                
                # Preprocess chunk
                processed_chunk = self._preprocess_chunk(df_chunk, mapping['columns'])
                
                # Process batch
                batch_result = self.batch_processor.process_batch(
                    processed_chunk,
                    mapping['model'],
                    batch_count
                )
                
                if not batch_result.success:
                    raise batch_result.error
                
                total_records += batch_result.records_processed
                
                # Update progress
                progress_tracker.update(batch_count, len(processed_chunk), total_records)
                progress_tracker.print_progress()
            
            # Log completion
            self._log_completion(
                f"Processing {file_type} file",
                total_records=total_records,
                batches_processed=batch_count,
                elapsed_time=f"{progress_tracker.get_elapsed_time():.1f}s"
            )
            
            return ProcessorResult(
                success=True,
                records_processed=total_records,
                details={
                    'file_type': file_type,
                    'file_path': file_path,
                    'batches_processed': batch_count,
                    'elapsed_time': progress_tracker.get_elapsed_time()
                }
            )
            
        except Exception as e:
            self._log_error(f"Processing {file_path}", e)
            return ProcessorResult(success=False, error=e)
    
    def _read_file_chunks(self, file_path: str, columns: List[str]):
        """Reads file in chunks using pandas."""
        try:
            return pd.read_csv(
                file_path,
                sep=self.config.separator,
                names=columns,
                on_bad_lines='skip',
                encoding=self.config.encoding,
                chunksize=self.config.batch_size,
                index_col=False,
            )
        except Exception as e:
            raise FileProcessingError(file_path, e)
    
    def _preprocess_chunk(self, df_chunk: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Preprocesses a data chunk."""
        # Replace NaN with None
        df_chunk = df_chunk.replace({np.nan: None})
        
        # Clean string columns
        for col in df_chunk.columns:
            if df_chunk[col].dtype == 'object':
                df_chunk[col] = df_chunk[col].apply(
                    lambda x: None if pd.isna(x) or x == '' else x
                )
        
        # Add metadata columns
        df_chunk['created_at'] = datetime.now()
        df_chunk['updated_at'] = datetime.now()
        df_chunk['language'] = self.config.language
        df_chunk['version'] = self.config.version
        
        return df_chunk
    
    def get_supported_file_types(self) -> List[str]:
        """Returns list of supported file types."""
        return list(self.file_mappings.keys())
    
    def is_file_type_supported(self, file_type: str) -> bool:
        """Checks if a file type is supported."""
        return file_type in self.file_mappings