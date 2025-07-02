import pandas as pd
import os

# Input and output paths
csv_path = "resources/data/hr/hr_data.csv"  # replace with your filename
md_path = "resources/data/hr/hr_employee_data.md"

# Load CSV
df = pd.read_csv(csv_path)

# Ensure HR data folder exists
os.makedirs(os.path.dirname(md_path), exist_ok=True)

# Open markdown file for writing
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# HR Employee Records Summary\n\n")

    for _, row in df.iterrows():
        f.write(f"## {row['full_name']} ({row['role']})\n")
        f.write(f"- **Department:** {row['department']}\n")
        f.write(f"- **Email:** {row['email']}\n")
        f.write(f"- **Location:** {row['location']}\n")
        f.write(f"- **Date of Birth:** {row['date_of_birth']}\n")
        f.write(f"- **Date of Joining:** {row['date_of_joining']}\n")
        f.write(f"- **Manager ID:** {row['manager_id']}\n")
        f.write(f"- **Salary:** ₹{row['salary']:,.2f}\n")
        f.write(f"- **Leave Balance:** {row['leave_balance']} days\n")
        f.write(f"- **Leaves Taken:** {row['leaves_taken']} days\n")
        f.write(f"- **Attendance %:** {row['attendance_pct']}%\n")
        f.write(f"- **Performance Rating:** {row['performance_rating']}/5\n")
        f.write(f"- **Last Review Date:** {row['last_review_date']}\n")
        f.write("\n---\n\n")
