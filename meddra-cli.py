import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import traceback
import numpy as np

from models import generate_meddra_file_mappings

load_dotenv()

MEDDRA_FILE_MAPPINGS = generate_meddra_file_mappings()

def process_meddra_files(folder_path: str, db_url: str, version: float, language: str, batch_size: int = 5000):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.asc'):
            file_path = os.path.join(folder_path, file_name)

            process_meddra_file(
                file_path=file_path,
                file_type=file_name,
                db_url=db_url,
                version=version,
                language=language,
                batch_size=batch_size
            )

def process_meddra_file(
    file_path: str, 
    file_type: str,
    db_url: str, 
    version: float,
    language: str,
    batch_size=5000
):
    """
    Processes and loads a MedDRA-formatted file into a database in batches.
    Args:
        file_path (str): Path to the MedDRA file to be processed.
        file_type (str): Type of MedDRA file (must be a key in MEDDRA_FILE_MAPPINGS).
        db_url (str): SQLAlchemy-compatible database URL for data insertion.
        version (float): MedDRA version to associate with the records.
        language (str): Language code for the records.
        batch_size (int, optional): Number of records to process per batch. Defaults to 5000.
    Returns:
        None
    Raises:
        Prints error messages for unsupported file types or batch loading errors.
        Raises and prints traceback for exceptions during batch processing.
    """
    if file_type not in MEDDRA_FILE_MAPPINGS:
        print(f"Error: Unsupported file type '{file_type}'")
        return
    
    mapping = MEDDRA_FILE_MAPPINGS[file_type]
    model_class = mapping['model']
    columns = mapping['columns']
    
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    
    with open(file_path, 'r', encoding='latin1') as f:
        total_lines = sum(1 for _ in f)
    
    batch_count = 0
    records_count = 0
    
    for df_chunk in pd.read_csv(
        file_path, 
        sep='$', 
        names=columns,
        on_bad_lines='skip',
        encoding='latin1',
        chunksize=batch_size,
        index_col=False,
    ):
        df_chunk = df_chunk.replace({np.nan: None})
        
        batch_count += 1
        
        for col in df_chunk.columns:
            if df_chunk[col].dtype == 'object':
                df_chunk[col] = df_chunk[col].apply(lambda x: None if pd.isna(x) or x == '' else x)
        
        df_chunk['created_at'] = datetime.now()
        df_chunk['updated_at'] = datetime.now()
        df_chunk['language'] = language
        df_chunk['version'] = version
        
        session = Session()
        try:
            records = []
            for _, row in df_chunk.iterrows():
                record_data = {col: row[col] for col in columns if col in row}

                record_data.update({
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    'language': row['language'],
                    'version': row['version']
                })
                record = model_class(**record_data)
                records.append(record)
            
            session.bulk_save_objects(records)
            session.commit()
            records_count += len(records)
            
            progress = min(100, int((batch_count * batch_size / total_lines) * 100))
            print(f"Progress: {progress}% - Loaded batch {batch_count} ({records_count} records so far)")
            
        except Exception as e:
            session.rollback()
            print(f"Error loading batch {batch_count}: {e}")
            raise traceback.format_exc()
        
        finally:
            session.close()
    
    print(f"Finished loading {records_count} {file_type} records")

def main():
    parser = argparse.ArgumentParser(description='Load MedDRA files into the database')
    parser.add_argument('--file-path', required=False, help='Path to the MedDRA file to be processed. Optional if you want to process specific files.')
    parser.add_argument('--folder-path', required=False, help='Path where .asc files are located')
    parser.add_argument('--version', type=float, default=28.0, help='MedDRA version (default: 28.0)')
    parser.add_argument('--language', default='en', help='Language code (default: en)')
    parser.add_argument('--batch-size', type=int, default=5000, help='Batch size for processing (default: 5000)')
    
    args = parser.parse_args()
    db_url = os.getenv("DATABASE_URL")
    
    if not args.file_path and not args.folder_path:
        print("Error: Either --file-path or --folder-path must be provided")
        return
    
    if not db_url:
        print("Error: DATABASE_URL environment variable not set")
        return
    
    if args.file_path:
        print(f"Processing single file: {args.file_path}")
        process_meddra_file(
            file_path=args.file_path,
            file_type=os.path.basename(args.file_path).split('.')[0],
            db_url=db_url,
            version=args.version,
            language=args.language,
            batch_size=args.batch_size
        )
        return
    
    print(f"Processing files in path: {args.folder_path}")
    process_meddra_files(
        folder_path=args.folder_path,
        db_url=db_url,
        version=args.version,
        language=args.language,
        batch_size=args.batch_size
    )

if __name__ == "__main__":
    main()