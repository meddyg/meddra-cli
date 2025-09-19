# MedDRA File Loader

A robust tool for loading MedDRA files into a database with batch processing support.

## Features

- ✅ Efficient batch processing
- ✅ Robust error handling
- ✅ File and configuration validation
- ✅ Meddra multi-language and version support
- ✅ Modular and extensible architecture
- ✅ Detailed logging

## Project Structure

```
meddra_loader/
├── __init__.py
├── meddra-cli.py                    # CLI entry point
├── config.py                 # Configuration and environment variables
├── exceptions.py             # Custom exceptions
├── models.py                 # Database models (existing)
├── processors/
│   ├── __init__.py
│   ├── base.py              # Abstract base processor
│   ├── file_processor.py    # File processing logic
│   └── batch_processor.py   # Batch processing logic
├── database/
│   ├── __init__.py
│   ├── connection.py        # Database connection management
│   └── operations.py        # Database operations
├── utils/
│   ├── __init__.py
│   ├── file_utils.py        # File handling utilities
│   └── progress.py          # Progress tracking utilities
└── README.md
```

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd meddra-loader
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/meddra_db
```

### Additional Configuration

The `config.py` file allows configuration of:

- **MedDRA Version**: Default 28.0
- **Language**: Default 'en'
- **Batch Size**: Default 5000
- **Encoding**: Default 'UTF-8'
- **Separator**: Default '$'

### Database DDL

This version requires your database tables to match the structure defined in `models.py`. Custom table structures are not supported yet.

To create the necessary tables in your database, simply run:

```bash
python3 models.py
```

This will initialize your database with the correct schema for the loader to work properly.

Ensure your database connection is correctly set up in the `.env` file before running this command.

## Usage

### Basic Commands

#### Process a single file

```bash
python meddra-cli.py --file-path /path/to/file.asc
```

#### Process all files in a directory

```bash
python meddra-cli.py --path /path/to/meddra/files
```

#### Custom configuration

```bash
python meddra-cli.py --path /path/to/files \
    --version 27.1 \
    --language es \
    --batch-size 1000 \
    --verbose
```

<!-- #### Dry-run mode

```bash
python meddra-cli.py --path /path/to/files --dry-run
``` -->

## Command Line Options

| Option         | Type   | Default | Description                     |
| -------------- | ------ | ------- | ------------------------------- |
| `--file-path`  | string | -       | Path to a specific MedDRA file  |
| `--path`       | string | -       | Directory containing .asc files |
| `--version`    | float  | 28.0    | MedDRA version                  |
| `--language`   | string | en      | Language code                   |
| `--batch-size` | int    | 5000    | Batch size for processing       |
| `--verbose`    | flag   | false   | Enable detailed output          |

## Supported File Types

Supported file types are defined in `models.py` through the `generate_meddra_file_mappings()` function. Common MedDRA files include:

- `pt.asc` - Preferred Terms
- `llt.asc` - Lowest Level Terms
- `hlt.asc` - High Level Terms
- `hlgt.asc` - High Level Group Terms
- `soc.asc` - System Organ Class
- `smq_list.asc` - Standardised MedDRA Queries
- And more...

## Usage Examples

### Example 1: Basic Processing

Process all MedDRA files in the standard directory:

```bash
python meddra-cli.py --path /data/meddra/28.0/MedAscii
```

**Output:**

```
Setup validation passed
Processing files in directory: /data/meddra/28.0/MedAscii
Found 15 files to process

--- Processing /data/meddra/28.0/MedAscii/pt.asc ---
Starting Processing pt file...
  file_path: /data/meddra/28.0/MedAscii/pt.asc
  file_size: 15728640
  total_lines: 75000
Progress: 20% - Batch 1 (5000/75000 records) - Elapsed: 2.3s - ETA: 9.2s
Progress: 40% - Batch 2 (10000/75000 records) - Elapsed: 4.6s - ETA: 6.9s
...
✓ Successfully processed 75000 records

=== Processing Summary ===
Total files processed: 15/15
Total records processed: 850000
All files processed successfully!
```

### Example 2: Custom Configuration

Process files with specific version and language:

```bash
python meddra-cli.py --path /data/meddra/27.1/MedAscii \
    --version 27.1 \
    --language es \
    --batch-size 2000 \
    --verbose
```

**Output:**

```
Configuration loaded successfully:
  Database URL: postgresql://user:***@localhost:5432/meddra_db
  Version: 27.1
  Language: es
  Batch size: 2000
Setup validation passed
Processing files in directory: /data/meddra/27.1/MedAscii
...
```

### Example 3: Process Specific File

Process only the Preferred Terms file:

```bash
python meddra-cli.py --file-path /data/meddra/28.0/MedAscii/pt.asc
```

**Output:**

```
Processing single file: /data/meddra/28.0/MedAscii/pt.asc
Starting Processing pt file...
  file_path: /data/meddra/28.0/MedAscii/pt.asc
  file_size: 15728640
  total_lines: 75000
Progress: 100% - Batch 15 (75000/75000 records) - Elapsed: 23.5s
✓ Successfully processed 75000 records
```

## Error Handling

The application handles various types of errors gracefully:

### Configuration Errors

```bash
$ python meddra-cli.py --path /data/meddra
Processing error: DATABASE_URL environment variable not set
```

### File Errors

```bash
$ python meddra-meddra-cli.py --file-path /nonexistent/file.asc
Processing error: Error processing file '/nonexistent/file.asc': File not found
```

### Database Errors

```bash
$ python meddra-meddra-cli.py --path /data/meddra
Processing error: Database connection test failed
```

### Unsupported File Types

```bash
$ python meddra-meddra-cli.py --file-path /data/unknown_file.asc
Error: Unsupported file type 'unknown_file'
Supported types: pt, llt, hlt, hlgt, soc, smq_list, mdhier, intl_ord
```

## Progress Tracking

The application provides detailed progress information:

- **Real-time progress**: Percentage completion and current batch
- **Performance metrics**: Records processed per second
- **Time estimates**: Elapsed time and estimated time remaining
- **Memory usage**: Current memory consumption
- **Batch information**: Current batch number and size

## Database Schema

The application expects your database models to have the following standard fields:

- `created_at`: Timestamp when record was created
- `updated_at`: Timestamp when record was last updated
- `language`: Language code (e.g., 'en', 'es', 'fr')
- `version`: MedDRA version (e.g., 28.0, 27.1)

## Development

### Adding New Processors

1. Create a new class inheriting from `BaseProcessor`:

```python
from processors.base import BaseProcessor, ProcessorResult

class CustomProcessor(BaseProcessor):
    def process(self, *args, **kwargs) -> ProcessorResult:
        # Your processing logic here
        return ProcessorResult(success=True, records_processed=count)
```

2. Register the processor in the appropriate factory or configuration.

### Adding New Utilities

1. Create functions in the appropriate `utils` module:

```python
def new_utility_function(param):
    """Description of what this function does."""
    # Implementation
    return result
```

2. Add to the module's `__all__` list for proper imports.

## Troubleshooting

### Common Issues

1. **Database Connection Issues**

   - Verify DATABASE_URL is correct
   - Check database server is running
   - Ensure user has proper permissions

2. **File Encoding Problems**

   - MedDRA files typically use 'UTF-8' encoding
   - Try different encodings if processing fails

3. **Memory Issues with Large Files**

   - Reduce batch size using `--batch-size`
   - Monitor system memory usage

4. **Permission Errors**
   - Ensure read permissions on input files
   - Check write permissions for log files

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
python meddra-cli.py --path /data/meddra --verbose
```

## Performance Optimization

### Batch Size Tuning

- **Small files** (< 10MB): Use batch size 1000-2000
- **Medium files** (10-100MB): Use batch size 5000 (default)
- **Large files** (> 100MB): Use batch size 10000-20000

## Changelog

### Version 1.0.0

- Initial release
- Basic file processing functionality
- Batch processing support
- Progress tracking
- Error handling
- CLI interface

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

### 📚 About MedDRA®

This software requires structured data from the MedDRA® dictionary, which is the property of the MSSO (Maintenance and Support Services Organization) and the ICH.

**⚠️ This repository does not distribute or include any MedDRA® files.**

To use `meddra-cli`, you must have a valid MedDRA license and download the official files from: [https://www.meddra.org](https://www.meddra.org)

This software is not affiliated with or endorsed by the MSSO or ICH.
