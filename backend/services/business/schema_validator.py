import json
import os
from backend.core.logger import bus_logger

class SchemaValidator:
    def __init__(self):
        self.output_dir = "outputs/business"
        # Since defining full robust JSON schemas dynamically takes quite some boilerplate,
        # we will implement a simplified schema validator check that ensures keys exist.
        
    def validate(self, files_to_check):
        bus_logger.info("Starting Schema Validation.")
        issues = []
        
        for file_name, required_keys in files_to_check.items():
            path = os.path.join(self.output_dir, file_name)
            if not os.path.exists(path):
                issues.append(f"ERROR: Missing expected file {file_name}")
                continue
                
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    
                # Basic key check
                if isinstance(data, dict):
                    missing = [k for k in required_keys if k not in data]
                    if missing:
                        issues.append(f"ERROR: {file_name} is missing keys: {missing}")
                elif isinstance(data, list):
                    if len(data) > 0 and isinstance(data[0], dict):
                        missing = [k for k in required_keys if k not in data[0]]
                        if missing:
                            issues.append(f"ERROR: Items in {file_name} missing keys: {missing}")
                            
            except Exception as e:
                issues.append(f"ERROR: Invalid JSON in {file_name}: {e}")
                
        report_path = os.path.join(self.output_dir, "schema_validation_report.md")
        with open(report_path, 'w') as f:
            f.write("# Schema Validation Report\\n\\n")
            if not issues:
                f.write("**Status:** PASSED\\n")
            else:
                f.write("**Status:** FAILED\\n\\n")
                f.write("## Issues\\n")
                for iss in issues:
                    f.write(f"- {iss}\\n")
                    
        bus_logger.info(f"Schema Validation completed with {len(issues)} issues.")
        return len(issues) == 0
