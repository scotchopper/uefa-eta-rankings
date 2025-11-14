#!/usr/bin/env python3
"""
Setup Windows Task Scheduler for UEFA Mobile Auto-Processor
Creates a scheduled task that runs the auto-processor continuously
"""

import os
import sys
import subprocess
from pathlib import Path

def create_scheduled_task():
    """Create a Windows scheduled task for the auto-processor"""
    
    # Get current directory and Python executable
    current_dir = os.path.abspath(os.path.dirname(__file__))
    python_exe = sys.executable
    script_path = os.path.join(current_dir, "mobile_auto_processor.py")
    
    # Task details
    task_name = "UEFA_Mobile_Auto_Processor"
    
    # Create the scheduled task XML
    task_xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2025-11-14T12:00:00</Date>
    <Author>UEFA ETA System</Author>
    <Description>Automatically processes mobile UEFA results files every hour</Description>
  </RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <StartBoundary>2025-11-14T12:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <Repetition>
        <Interval>PT1H</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
    </TimeTrigger>
    <BootTrigger>
      <Enabled>true</Enabled>
      <Delay>PT5M</Delay>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions>
    <Exec>
      <Command>"{python_exe}"</Command>
      <Arguments>"{script_path}" once</Arguments>
      <WorkingDirectory>{current_dir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""
    
    # Save XML to temp file
    xml_file = "uefa_auto_processor_task.xml"
    with open(xml_file, 'w', encoding='utf-16') as f:
        f.write(task_xml)
    
    try:
        # Delete existing task if it exists
        subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'], 
                      capture_output=True, check=False)
        
        # Create the scheduled task
        result = subprocess.run([
            'schtasks', '/create', '/xml', xml_file, '/tn', task_name
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully created scheduled task: {task_name}")
            print(f"📅 Task runs every hour and on system startup")
            print(f"📂 Working directory: {current_dir}")
            print(f"🐍 Python executable: {python_exe}")
            print(f"📄 Script: {script_path}")
            
            # Clean up XML file
            os.remove(xml_file)
            
            print("\n🎯 Task Management:")
            print(f"   View:    schtasks /query /tn {task_name}")
            print(f"   Run:     schtasks /run /tn {task_name}")
            print(f"   Stop:    schtasks /end /tn {task_name}")  
            print(f"   Delete:  schtasks /delete /tn {task_name} /f")
            
            return True
        else:
            print(f"❌ Failed to create scheduled task: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating scheduled task: {e}")
        return False
    finally:
        # Clean up XML file if it exists
        if os.path.exists(xml_file):
            os.remove(xml_file)

def check_task_status():
    """Check if the scheduled task exists and is running"""
    task_name = "UEFA_Mobile_Auto_Processor"
    
    try:
        # Query the task
        result = subprocess.run([
            'schtasks', '/query', '/tn', task_name, '/fo', 'LIST'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Scheduled task '{task_name}' exists")
            
            # Parse the output to get status
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Status:' in line:
                    status = line.split(':', 1)[1].strip()
                    print(f"📊 Status: {status}")
                elif 'Next Run Time:' in line:
                    next_run = line.split(':', 1)[1].strip()
                    print(f"⏰ Next run: {next_run}")
                elif 'Last Run Time:' in line:
                    last_run = line.split(':', 1)[1].strip()
                    print(f"📅 Last run: {last_run}")
            
            return True
        else:
            print(f"❌ Scheduled task '{task_name}' not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking task status: {e}")
        return False

def main():
    print("🕰️ UEFA Mobile Auto-Processor Scheduler Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'create':
            if create_scheduled_task():
                print("\n🎉 Scheduled task created successfully!")
                print("The auto-processor will now run every hour automatically.")
        elif command == 'status':
            check_task_status()
        else:
            print("❌ Unknown command")
            print("Usage:")
            print("  python setup_scheduler.py create  # Create scheduled task")
            print("  python setup_scheduler.py status  # Check task status")
    else:
        print("This script sets up Windows Task Scheduler to run the")
        print("UEFA Mobile Auto-Processor automatically every hour.")
        print()
        print("Commands:")
        print("  create  - Create the scheduled task")
        print("  status  - Check current task status")
        print()
        print("Examples:")
        print("  python setup_scheduler.py create")
        print("  python setup_scheduler.py status")
        print()
        
        choice = input("❓ Create scheduled task now? (y/n): ").lower().strip()
        if choice == 'y':
            if create_scheduled_task():
                print("\n🎉 Setup complete! The auto-processor will run every hour.")
            else:
                print("\n❌ Setup failed. You may need to run as administrator.")

if __name__ == "__main__":
    main()