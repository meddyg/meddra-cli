import argparse
import sys
from typing import List, Optional
from config import AppConfig
from database.connection import DatabaseManager
from core.file_processor import FileProcessor
from utils.file_utils import find_meddra_files, get_file_type_from_path
from exceptions import MedDRAProcessingError, InvalidConfigurationError

class MedDRACLI:
    """Command Line Interface for MedDRA file processing."""
    
    def __init__(self):
        self.config = None
        self.db_manager = None
        self.file_processor = None
    
    def run(self) -> int:
        """Main entry point for the CLI."""
        try:
            args = self._parse_arguments()
            self._initialize_components(args)
            self._validate_setup()
            
            if args.file_path:
                return self._process_single_file(args.file_path)
            else:
                return self._process_directory(args.path)
                
        except MedDRAProcessingError as e:
            print(f"Processing error: {e}")
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 1
        finally:
            self._cleanup()
    
    def _parse_arguments(self) -> argparse.Namespace:
        """Parses command line arguments."""
        parser = argparse.ArgumentParser(
            description='Load MedDRA files into the database',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
                Examples:
                # Process a single file
                python cli.py --file-path /path/to/file.asc
                
                # Process all files in a directory
                python cli.py --path /path/to/meddra/files
                
                # Process with custom settings
                python cli.py --path /path/to/files --version 27.1 --language es --batch-size 1000
                            """
        )
        
        # File/directory options (mutually exclusive)
        file_group = parser.add_mutually_exclusive_group(required=True)
        file_group.add_argument(
            '--file-path',
            help='Path to a specific MedDRA file to process'
        )
        file_group.add_argument(
            '--path',
            help='Directory containing MedDRA .asc files'
        )
        
        # Processing options
        parser.add_argument(
            '--version',
            type=float,
            default=28.0,
            help='MedDRA version (default: 28.0)'
        )
        parser.add_argument(
            '--language',
            default='en',
            help='Language code (default: en)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=5000,
            help='Batch size for processing (default: 5000)'
        )
        
        # Additional options
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without actually processing'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose output'
        )
        
        return parser.parse_args()
    
    def _initialize_components(self, args: argparse.Namespace) -> None:
        """Initializes application components."""
        try:
            # Create configuration
            self.config = AppConfig.from_env(
                version=args.version,
                language=args.language,
                batch_size=args.batch_size
            )
            
            # Initialize database manager
            self.db_manager = DatabaseManager(self.config.database)
            
            # Initialize file processor
            self.file_processor = FileProcessor(self.db_manager, self.config.processing)
            
            if args.verbose:
                print("Configuration loaded successfully:")
                print(f"  Database URL: {self.config.database.url}")
                print(f"  Version: {self.config.processing.version}")
                print(f"  Language: {self.config.processing.language}")
                print(f"  Batch size: {self.config.processing.batch_size}")
                
        except Exception as e:
            raise InvalidConfigurationError(f"Failed to initialize components: {e}")
    
    def _validate_setup(self) -> None:
        """Validates that the setup is correct."""
        if not self.db_manager.test_connection():
            raise MedDRAProcessingError("Database connection test failed")
        
        print("Setup validation passed")
    
    def _process_single_file(self, file_path: str) -> int:
        """Processes a single file."""
        print(f"Processing single file: {file_path}")
        
        file_type = get_file_type_from_path(file_path)
        if not self.file_processor.is_file_type_supported(file_type):
            supported_types = self.file_processor.get_supported_file_types()
            print(f"Error: Unsupported file type '{file_type}'")
            print(f"Supported types: {', '.join(supported_types)}")
            return 1
        
        result = self.file_processor.process(file_path)
        
        if result.success:
            print(f"Successfully processed {result.records_processed} records")
            return 0
        else:
            print(f"Failed to process file: {result.error}")
            return 1
    
    def _process_directory(self, directory_path: str) -> int:
        """Processes all files in a directory."""
        print(f"Processing files in directory: {directory_path}")
        
        try:
            files = find_meddra_files(directory_path)
            if not files:
                print("No .asc files found in the directory")
                return 0
            
            print(f"Found {len(files)} files to process")
            
            total_records = 0
            processed_files = 0
            failed_files = []
            
            for file_path in files:
                file_type = get_file_type_from_path(file_path)
                
                if not self.file_processor.is_file_type_supported(file_type):
                    print(f"Skipping unsupported file type: {file_type}")
                    continue
                
                print(f"\n--- Processing {file_path} ---")
                result = self.file_processor.process(file_path)
                
                if result.success:
                    total_records += result.records_processed
                    processed_files += 1
                    print(f"✓ Successfully processed {result.records_processed} records")
                else:
                    failed_files.append((file_path, result.error))
                    print(f"✗ Failed to process: {result.error}")
            
            # Summary
            print(f"\n=== Processing Summary ===")
            print(f"Total files processed: {processed_files}/{len(files)}")
            print(f"Total records processed: {total_records}")
            
            if failed_files:
                print(f"Failed files ({len(failed_files)}):")
                for file_path, error in failed_files:
                    print(f"  - {file_path}: {error}")
                return 1
            else:
                print("All files processed successfully!")
                return 0
                
        except Exception as e:
            print(f"Error processing directory: {e}")
            return 1
    
    def _cleanup(self) -> None:
        """Cleans up resources."""
        if self.db_manager:
            self.db_manager.close()


def main():
    """Main entry point."""
    cli = MedDRACLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()