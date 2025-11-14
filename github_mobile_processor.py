#!/usr/bin/env python3
"""
GitHub Actions Mobile Results Processor
Optimized for cloud-based automated processing
"""

import json
import os
import sys
import glob
from datetime import datetime
from pathlib import Path

class GitHubMobileProcessor:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.fixtures_file = self.base_dir / "uefa_fixtures_data.json"
        self.mobile_dir = self.base_dir / "mobile"
        self.archive_dir = self.base_dir / "processed_exports"
        
        # Ensure directories exist
        self.mobile_dir.mkdir(exist_ok=True)
        self.archive_dir.mkdir(exist_ok=True)
        
    def find_mobile_results_files(self):
        """Find all mobile results JSON files"""
        patterns = [
            "mobile_results_*.json",
            "mobile/mobile_results_*.json", 
            "mobile/*.json"
        ]
        
        files = []
        for pattern in patterns:
            files.extend(glob.glob(str(self.base_dir / pattern)))
        
        # Filter out processed files
        files = [f for f in files if not f.startswith(str(self.archive_dir))]
        
        print(f"📁 Found {len(files)} mobile results files")
        for file in files:
            print(f"   📄 {os.path.basename(file)}")
            
        return files
    
    def load_fixtures_data(self):
        """Load current fixtures data"""
        if self.fixtures_file.exists():
            with open(self.fixtures_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("⚠️ No fixtures data file found")
            return []
    
    def process_mobile_results(self, results_file):
        """Process a single mobile results file"""
        print(f"🔄 Processing: {os.path.basename(results_file)}")
        
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                mobile_data = json.load(f)
                
            fixtures = self.load_fixtures_data()
            updates_made = 0
            
            # Process each result in the mobile data
            for result in mobile_data.get('results', []):
                fixture_id = result.get('fixture_id')
                home_score = result.get('home_score')
                away_score = result.get('away_score')
                
                if fixture_id is None or home_score is None or away_score is None:
                    continue
                
                # Find and update the fixture
                for fixture in fixtures:
                    if fixture.get('id') == fixture_id:
                        # Only update if not already set
                        if fixture.get('home_score') is None:
                            fixture['home_score'] = int(home_score)
                            fixture['away_score'] = int(away_score)
                            fixture['result_updated'] = datetime.now().isoformat()
                            updates_made += 1
                            print(f"✅ Updated: {fixture['home_team']} {home_score}-{away_score} {fixture['away_team']}")
                        break
            
            # Save updated fixtures
            if updates_made > 0:
                with open(self.fixtures_file, 'w', encoding='utf-8') as f:
                    json.dump(fixtures, f, indent=2, ensure_ascii=False)
                print(f"💾 Saved {updates_made} fixture updates")
            else:
                print("ℹ️ No new results to process")
                
            return updates_made
            
        except Exception as e:
            print(f"❌ Error processing {results_file}: {e}")
            return 0
    
    def archive_processed_file(self, file_path):
        """Move processed file to archive with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        archived_name = f"processed_{timestamp}_{filename}"
        archived_path = self.archive_dir / archived_name
        
        try:
            os.rename(file_path, archived_path)
            print(f"📦 Archived: {filename} → {archived_name}")
        except Exception as e:
            print(f"⚠️ Failed to archive {filename}: {e}")
    
    def generate_github_summary(self, total_updates):
        """Generate GitHub Actions step summary"""
        fixtures = self.load_fixtures_data()
        completed = sum(1 for f in fixtures if f.get('home_score') is not None)
        total = len(fixtures)
        
        summary = f"""
## 📊 UEFA Mobile Processing Results

**📅 Processing Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
**🔄 Updates Made:** {total_updates} fixtures
**📊 Current Status:** {completed}/{total} fixtures completed
**📈 Progress:** {(completed/total*100):.1f}% complete

### 🎯 Quick Stats
- **World Cup Qualifiers:** {sum(1 for f in fixtures if f.get('competition') == 'World Cup Qualifier')} fixtures
- **Friendlies:** {sum(1 for f in fixtures if f.get('competition') == 'Friendly')} fixtures
- **Remaining:** {total - completed} fixtures

---
*Next processing: Automatic hourly via GitHub Actions*
"""
        
        # Write to GitHub step summary if running in Actions
        if os.getenv('GITHUB_STEP_SUMMARY'):
            with open(os.getenv('GITHUB_STEP_SUMMARY'), 'a') as f:
                f.write(summary)
        
        print(summary)
    
    def run(self):
        """Main processing function"""
        print("🚀 GitHub Actions UEFA Mobile Processor")
        print("=" * 50)
        
        # Find mobile results files
        results_files = self.find_mobile_results_files()
        
        if not results_files:
            print("ℹ️ No mobile results files found")
            self.generate_github_summary(0)
            return
        
        total_updates = 0
        
        # Process each file
        for file_path in results_files:
            updates = self.process_mobile_results(file_path)
            total_updates += updates
            
            # Archive the processed file
            if updates > 0:
                self.archive_processed_file(file_path)
        
        # Generate summary
        self.generate_github_summary(total_updates)
        
        if total_updates > 0:
            print(f"✅ Successfully processed {total_updates} fixture updates")
        else:
            print("ℹ️ No new updates processed")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("GitHub Actions UEFA Mobile Results Processor")
        print("Usage: python github_mobile_processor.py")
        print("Environment: Optimized for GitHub Actions cloud processing")
        return
    
    processor = GitHubMobileProcessor()
    processor.run()

if __name__ == "__main__":
    main()