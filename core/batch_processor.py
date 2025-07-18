import pandas as pd
from typing import List, Type, Any
from core.base import BaseProcessor, ProcessorResult
from exceptions import BatchProcessingError

class BatchProcessor(BaseProcessor):
    """Processes data in batches and saves to database."""
    
    def process_batch(self, df_chunk: pd.DataFrame, model_class: Type, batch_number: int) -> ProcessorResult:
        """Processes a single batch of data."""
        try:
            records = self._create_records_from_dataframe(df_chunk, model_class)
            
            with self.db_manager.session_scope() as session:
                session.bulk_save_objects(records)
                # Commit happens automatically due to session_scope
            
            return ProcessorResult(
                success=True,
                records_processed=len(records),
                details={
                    'batch_number': batch_number,
                    'model_class': model_class.__name__
                }
            )
            
        except Exception as e:
            error = BatchProcessingError(batch_number, e)
            return ProcessorResult(success=False, error=error)
    
    def _create_records_from_dataframe(self, df: pd.DataFrame, model_class: Type) -> List[Any]:
        """Creates model instances from dataframe rows."""
        records = []
        
        for _, row in df.iterrows():
            # Get the original column names (without metadata)
            original_columns = [col for col in df.columns if col not in 
                              ['created_at', 'updated_at', 'language', 'version']]
            
            # Create record data with original columns
            record_data = {col: row[col] for col in original_columns if col in row}
            
            # Add metadata
            record_data.update({
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'language': row['language'],
                'version': row['version']
            })
            
            # Create model instance
            record = model_class(**record_data)
            records.append(record)
        
        return records
    
    def process(self, *args, **kwargs) -> ProcessorResult:
        """Main process method - delegates to process_batch."""
        return self.process_batch(*args, **kwargs)