#!/usr/bin/env python3
"""
UEFA Mobile Auto-Processor - Scheduled Background Service
Automatically detects and processes new mobile JSON files every hour
"""

import json
import os
import glob
import time
import logging
from datetime import datetime, timedelta
import subprocess
import sys
import threading
from pathlib import Path

# Configuration
CHECK_INTERVAL = 3600  # Check every hour (3600 seconds)
PROCESSED_MARKER_FILE = "last_processed_mobile.json"

# Setup logging
log_file = "mobile_auto_processor.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class MobileAutoProcessor:
    def __init__(self):
        self.running = False
        self.last_processed_files = self.load_processed_files()
        
    def load_processed_files(self):
        """Load list of already processed files"""
        try:
            if os.path.exists(PROCESSED_MARKER_FILE):
                with open(PROCESSED_MARKER_FILE, 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_files', []))
        except Exception as e:
            logger.warning(f"Could not load processed files list: {e}")
        return set()
    
    def save_processed_files(self):
        """Save list of processed files"""
        try:
            data = {
                'processed_files': list(self.last_processed_files),
                'last_check': datetime.now().isoformat()
            }
            with open(PROCESSED_MARKER_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save processed files list: {e}")
    
    def find_new_mobile_files(self):
        """Find new mobile JSON files that haven't been processed"""
        patterns = [
            "uefa_mobile_results_*.json",
            "mobile/uefa_mobile_results_*.json"
        ]
        
        all_files = []
        for pattern in patterns:
            all_files.extend(glob.glob(pattern))
        
        # Filter out already processed files
        new_files = []
        for file_path in all_files:
            abs_path = os.path.abspath(file_path)
            if abs_path not in self.last_processed_files:
                new_files.append(file_path)
        
        # Sort by modification time (newest first)
        new_files.sort(key=os.path.getmtime, reverse=True)
        return new_files
    
    def load_mobile_results(self, json_file):
        """Load results from mobile JSON export"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            logger.info(f"Loaded {data['total_results']} results from {json_file}")
            return data['results']
            
        except Exception as e:
            logger.error(f"Error loading {json_file}: {e}")
            return []
    
    def update_fixtures_data(self, results, source_file):
        """Update the fixtures data JSON file"""
        try:
            with open('uefa_fixtures_data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            logger.error("uefa_fixtures_data.json not found!")
            return False
        
        updated_count = 0
        scotland_count = 0
        
        for result in results:
            # Find matching fixture
            fixture_found = False
            for fixture_id, fixture_data in data['fixtures'].items():
                home_match = fixture_data['home_team'].lower() == result['home_team'].lower()
                away_match = fixture_data['away_team'].lower() == result['away_team'].lower()
                
                if home_match and away_match:
                    if 'results' not in data:
                        data['results'] = {}
                    
                    # Determine result code
                    if result['home_goals'] > result['away_goals']:
                        result_code = 'H'
                    elif result['away_goals'] > result['home_goals']:
                        result_code = 'A'
                    else:
                        result_code = 'D'
                    
                    data['results'][fixture_id] = {
                        'home_goals': result['home_goals'],
                        'away_goals': result['away_goals'],
                        'result': result_code,
                        'notes': f"Auto-processed from {os.path.basename(source_file)} - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                        'completed_at': datetime.now().isoformat()
                    }
                    
                    data['fixtures'][fixture_id]['status'] = 'completed'
                    
                    if result['is_scotland']:
                        scotland_count += 1
                    
                    updated_count += 1
                    fixture_found = True
                    logger.info(f"Updated: {result['result_text']}")
                    break
            
            if not fixture_found:
                logger.warning(f"Could not find fixture for: {result['result_text']}")
        
        # Save updated data
        data['last_updated'] = datetime.now().isoformat()
        
        with open('uefa_fixtures_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Updated {updated_count} fixtures ({scotland_count} Scotland matches)")
        return updated_count > 0
    
    def run_analysis(self):
        """Run the enhanced team range analysis"""
        try:
            logger.info("Running enhanced team range analysis...")
            result = subprocess.run([sys.executable, 'enhanced_team_range_analysis.py'], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("Analysis completed successfully!")
                return True
            else:
                logger.error(f"Analysis failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Analysis timed out after 5 minutes")
            return False
        except Exception as e:
            logger.error(f"Error running analysis: {e}")
            return False
    
    def update_mobile_reports(self):
        """Update mobile HTML reports"""
        try:
            logger.info("Updating mobile reports...")
            result = subprocess.run([sys.executable, 'simple_mobile_analyzer.py'], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logger.info("Mobile reports updated!")
                return True
            else:
                logger.warning(f"Mobile report update failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Mobile report update timed out")
            return False
        except Exception as e:
            logger.warning(f"Error updating mobile reports: {e}")
            return False
    
    def archive_processed_file(self, json_file):
        """Move processed JSON file to archive"""
        try:
            archive_dir = "processed_mobile_results"
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)
            
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            archive_name = f"{base_name}_auto_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            archive_path = os.path.join(archive_dir, archive_name)
            
            # Copy instead of move to preserve original
            import shutil
            shutil.copy2(json_file, archive_path)
            logger.info(f"Archived processed file: {archive_path}")
            
        except Exception as e:
            logger.warning(f"Could not archive file: {e}")
    
    def process_file(self, json_file):
        """Process a single mobile JSON file"""
        logger.info(f"Processing new mobile results file: {json_file}")
        
        # Load results
        results = self.load_mobile_results(json_file)
        if not results:
            logger.error(f"No valid results found in {json_file}")
            return False
        
        scotland_results = sum(1 for r in results if r['is_scotland'])
        other_results = len(results) - scotland_results
        
        logger.info(f"Processing {len(results)} results ({scotland_results} Scotland, {other_results} other)")
        
        # Update fixtures
        if self.update_fixtures_data(results, json_file):
            # Run analysis
            analysis_success = self.run_analysis()
            
            # Update mobile reports
            mobile_success = self.update_mobile_reports()
            
            if analysis_success:
                logger.info("🎉 Successfully processed mobile results!")
                logger.info(f"✅ Updated {len(results)} fixtures")
                logger.info(f"✅ Scotland results: {scotland_results}")
                logger.info(f"✅ Rankings analysis completed")
                if mobile_success:
                    logger.info("✅ Mobile reports updated")
                
                # Archive the file
                self.archive_processed_file(json_file)
                
                # Mark as processed
                self.last_processed_files.add(os.path.abspath(json_file))
                self.save_processed_files()
                
                return True
            else:
                logger.error("Analysis failed but fixtures were updated")
                return False
        else:
            logger.error("Failed to update fixtures data")
            return False
    
    def check_and_process(self):
        """Check for new files and process them"""
        logger.info("Checking for new mobile results files...")
        
        new_files = self.find_new_mobile_files()
        
        if not new_files:
            logger.info("No new mobile results files found")
            return
        
        logger.info(f"Found {len(new_files)} new file(s) to process")
        
        processed_count = 0
        for json_file in new_files:
            try:
                if self.process_file(json_file):
                    processed_count += 1
                    logger.info(f"✅ Successfully processed: {json_file}")
                else:
                    logger.error(f"❌ Failed to process: {json_file}")
                    
            except Exception as e:
                logger.error(f"❌ Error processing {json_file}: {e}")
        
        if processed_count > 0:
            logger.info(f"🎉 Auto-processing complete! Processed {processed_count} file(s)")
        else:
            logger.warning("⚠️ No files were successfully processed")
    
    def run_forever(self):
        """Run the auto-processor continuously"""
        logger.info("🚀 UEFA Mobile Auto-Processor started")
        logger.info(f"⏰ Checking for new files every {CHECK_INTERVAL//60} minutes")
        logger.info(f"📂 Monitoring: uefa_mobile_results_*.json and mobile/uefa_mobile_results_*.json")
        logger.info(f"📄 Logs: {log_file}")
        
        self.running = True
        
        try:
            while self.running:
                try:
                    self.check_and_process()
                except Exception as e:
                    logger.error(f"Error during check cycle: {e}")
                
                # Wait for next check
                logger.info(f"⏳ Next check in {CHECK_INTERVAL//60} minutes...")
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("🛑 Auto-processor stopped by user")
        except Exception as e:
            logger.error(f"🛑 Auto-processor stopped due to error: {e}")
        finally:
            self.running = False
            logger.info("🛑 UEFA Mobile Auto-Processor stopped")
    
    def run_once(self):
        """Run the processor once and exit"""
        logger.info("🔄 Running mobile auto-processor (single check)")
        self.check_and_process()
        logger.info("✅ Single check completed")
    
    def status(self):
        """Show processor status"""
        print("📊 UEFA Mobile Auto-Processor Status")
        print("=" * 40)
        
        # Show processed files
        if os.path.exists(PROCESSED_MARKER_FILE):
            try:
                with open(PROCESSED_MARKER_FILE, 'r') as f:
                    data = json.load(f)
                    last_check = data.get('last_check', 'Never')
                    processed_files = data.get('processed_files', [])
                    
                    print(f"📅 Last check: {last_check}")
                    print(f"📂 Processed files: {len(processed_files)}")
                    
                    if processed_files:
                        print("\n📄 Recent processed files:")
                        for file in processed_files[-5:]:  # Show last 5
                            print(f"   • {os.path.basename(file)}")
            except Exception as e:
                print(f"❌ Error reading status: {e}")
        else:
            print("📄 No processing history found")
        
        # Check for pending files
        new_files = self.find_new_mobile_files()
        if new_files:
            print(f"\n🔔 {len(new_files)} new file(s) waiting for processing:")
            for file in new_files:
                mtime = datetime.fromtimestamp(os.path.getmtime(file))
                print(f"   • {file} ({mtime.strftime('%Y-%m-%d %H:%M')})")
        else:
            print("✅ No new files waiting for processing")

def main():
    processor = MobileAutoProcessor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'start':
            processor.run_forever()
        elif command == 'once':
            processor.run_once()
        elif command == 'status':
            processor.status()
        else:
            print("❌ Unknown command")
            print("Usage:")
            print("  python mobile_auto_processor.py start   # Run continuously")
            print("  python mobile_auto_processor.py once    # Run once and exit")
            print("  python mobile_auto_processor.py status  # Show status")
    else:
        print("🤖 UEFA Mobile Auto-Processor")
        print("=" * 35)
        print("Automatically processes mobile UEFA results files")
        print()
        print("Commands:")
        print("  start   - Run continuously (check every hour)")
        print("  once    - Run once and exit")
        print("  status  - Show current status")
        print()
        print("Examples:")
        print("  python mobile_auto_processor.py start")
        print("  python mobile_auto_processor.py once")
        print("  python mobile_auto_processor.py status")

if __name__ == "__main__":
    main()