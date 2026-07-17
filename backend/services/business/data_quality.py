import json
import os
import glob
from backend.core.logger import bus_logger

class DataQualityValidator:
    def __init__(self):
        self.output_dir = "outputs/business"
        
    def validate(self):
        bus_logger.info("Starting Data Quality Validation.")
        issues = []
        
        # We check the raw outputs from Phase 1 and 2 that feed Phase 3
        timeline_files = glob.glob("outputs/behavior/timeline/*_timeline.json")
        zone_files = glob.glob("outputs/analytics/*_zone_analytics.json")
        
        if not timeline_files:
            issues.append("CRITICAL: No timeline JSON files found.")
            
        if not zone_files:
            issues.append("CRITICAL: No zone analytics JSON files found.")
            
        for tf in timeline_files:
            try:
                with open(tf, 'r') as f:
                    data = json.load(f)
                    
                for ev in data:
                    if 'behavior' not in ev or not ev['behavior']:
                        issues.append(f"WARNING: Empty behavior in {tf} for track {ev.get('track_id')}")
                    if ev.get('end_time', 0) < ev.get('start_time', 0):
                        issues.append(f"ERROR: Invalid timestamps (end < start) in {tf}")
            except Exception as e:
                issues.append(f"ERROR: Could not read timeline file {tf}: {e}")
                
        # Generate Data Quality Report
        report_path = os.path.join(self.output_dir, "data_quality_report.md")
        with open(report_path, 'w') as f:
            f.write("# Data Quality Validation Report\\n\\n")
            if not issues:
                f.write("**Status:** PASSED (No issues detected)\\n")
            else:
                f.write("**Status:** ISSUES DETECTED\\n\\n")
                f.write("## Issues\\n")
                for iss in issues:
                    f.write(f"- {iss}\\n")
                    
        bus_logger.info(f"Data Quality Validation completed with {len(issues)} issues.")
        return len(issues) == 0
