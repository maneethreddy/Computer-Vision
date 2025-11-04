import pandas as pd
import os
from datetime import datetime

def view_attendance(attendance_file="attendance.csv"):
    """View and analyze attendance records"""
    if not os.path.exists(attendance_file):
        print(f"Attendance file '{attendance_file}' not found!")
        return
    
    try:
        # Read CSV
        df = pd.read_csv(attendance_file)
        
        print("=" * 70)
        print("ATTENDANCE RECORDS")
        print("=" * 70)
        print()
        
        # Display all records
        print("All Records:")
        print("-" * 70)
        print(df.to_string(index=False))
        print()
        
        # Statistics
        print("=" * 70)
        print("STATISTICS")
        print("=" * 70)
        print()
        
        # Total records
        print(f"Total Attendance Records: {len(df)}")
        print()
        
        # By date
        print("Attendance by Date:")
        date_counts = df['Date'].value_counts().sort_index()
        for date, count in date_counts.items():
            print(f"  {date}: {count} record(s)")
        print()
        
        # By person
        print("Attendance by Person:")
        person_counts = df['Name'].value_counts()
        for name, count in person_counts.items():
            print(f"  {name}: {count} record(s)")
        print()
        
        # Today's attendance
        today = datetime.now().strftime("%Y-%m-%d")
        today_records = df[df['Date'] == today]
        print(f"Today's Attendance ({today}):")
        if len(today_records) > 0:
            print(today_records.to_string(index=False))
        else:
            print("  No attendance marked today.")
        print()
        
        # Export options
        print("=" * 70)
        export = input("Export to Excel? (y/n): ").strip().lower()
        if export == 'y':
            excel_file = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(excel_file, index=False)
            print(f"✓ Exported to {excel_file}")
        
    except Exception as e:
        print(f"Error reading attendance file: {e}")

if __name__ == "__main__":
    view_attendance()

