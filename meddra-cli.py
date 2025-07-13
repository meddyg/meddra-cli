import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import traceback
import numpy as np

# Import the SQLAlchemy models
from models import generate_meddra_file_mappings

# Load environment variables for database connection
load_dotenv()

# Dictionary mapping file names to model classes and their columns
MEDDRA_FILE_MAPPINGS = generate_meddra_file_mappings()
# MEDDRA_FILE_MAPPINGS = {
#     'llt.asc': {
#         'model': MeddraLowLevelTerm,
#         'columns': [
#             'llt_code', 'llt_name', 'pt_code', 
#             'llt_whoart_code', 'llt_harts_code', 'llt_costart_sym',
#             'llt_icd9_code', 'llt_icd9cm_code', 'llt_icd10_code',
#             'llt_currency', 'llt_jart_code', 'null_field'
#         ]
#     },
#     'pt.asc': {
#         'model': MeddraPrefTerm,
#         'columns': [
#             'pt_code', 'pt_name', 'null_field', 'pt_soc_code',
#             'pt_whoart_code', 'pt_harts_code', 'pt_costart_sym',
#             'pt_icd9_code', 'pt_icd9cm_code', 'pt_icd10_code',
#             'pt_jart_code'
#         ]
#     },
#     # Add other file mappings as needed
# }

def process_meddra_file(file_path, file_type, db_url, version, language, batch_size=5000):
    """Process a MedDRA file and load it into the database"""
    if file_type not in MEDDRA_FILE_MAPPINGS:
        print(f"Error: Unsupported file type '{file_type}'")
        return
    
    mapping = MEDDRA_FILE_MAPPINGS[file_type]
    model_class = mapping['model']
    columns = mapping['columns']
    
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    
    # Count total lines for progress reporting
    with open(file_path, 'r', encoding='latin1') as f:
        total_lines = sum(1 for _ in f)
    
    # Process file in batches
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
    parser.add_argument('--file', required=True, help='Path to the MedDRA file')
    parser.add_argument('--type', required=True, choices=MEDDRA_FILE_MAPPINGS.keys(), help='Type of MedDRA file')
    parser.add_argument('--version', type=float, default=28.0, help='MedDRA version (default: 28.0)')
    parser.add_argument('--language', default='en', help='Language code (default: en)')
    parser.add_argument('--batch-size', type=int, default=5000, help='Batch size for processing (default: 5000)')
    
    args = parser.parse_args()
    
    # Database connection URL from environment variables
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("Error: DATABASE_URL environment variable not set")
        return
    
    print(f"Processing {args.type} file in batches...")
    process_meddra_file(args.file, args.type, db_url, args.version, args.language, args.batch_size)

if __name__ == "__main__":
    main()