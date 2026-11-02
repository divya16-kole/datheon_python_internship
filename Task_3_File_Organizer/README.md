# File Organizer

A PySide6 desktop utility that organizes files directly inside a selected
folder into `Documents`, `Images`, `Videos`, `Archives`, and `Code` categories.
It leaves unsupported file types and subfolders in place, does not follow
symbolic links, and renames a destination collision with a numeric suffix
(for example, `report_1.txt`) instead of replacing the existing file.

## Run

From this directory, install the dependency and start the application:

```powershell
py -3.14 -m pip install -r requirements.txt
py -3.14 organizer.py
```

Select a folder and choose **Organize Files**. The activity log shows moved,
skipped, and failed files; the final summary reports the scan totals.
Existing files already inside category folders are counted separately from
files moved during the current run.

Use the same `py -3.14` launcher for both installation and running so the
dependency is installed into the same Python environment that starts the app.
