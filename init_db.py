import os
import sqlite3
from pathlib import Path
import shutil

instance_dir = Path('instance')
instance_dir.mkdir(exist_ok=True)

db_file = instance_dir / 'agriculture_assistant.db'

if db_file.exists():
    db_file.unlink()

conn = sqlite3.connect(str(db_file))
conn.close()

import stat
os.chmod(str(db_file), stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
os.chmod(str(instance_dir), stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | 
                            stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | 
                            stat.S_IROTH | stat.S_IXOTH)

print(f"Database initialized at: {db_file.absolute()}")
print("Database permissions set. Run 'python generate_sample_data.py' to add sample data.") 