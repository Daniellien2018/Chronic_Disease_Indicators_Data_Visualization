# Chronic Disease Indicators Data Visualization and Analytics Project
## CSE_6242 - Spring 2025 - Georgia Institute of Technology



## 📌 Setup Instructions

### 1️⃣ Clone the repository
```bash
# Clone the repository
git clone <repo-url>
cd Chronic_Disease_Indicators_Data_Visualization

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment:
# For Linux/macOS
source .venv/bin/activate

# For Windows (Command Prompt)
.venv\Scripts\activate

# For Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Test with 
python3 test.py

# To use in VS code - Select the venv created as Python Interpreter  - Restart vscode

# To use jupyter ipynb - run below to register new venv as Jupyter kernel (make globally visible) - then select - Restart vscode
python -m ipykernel install --user --name=.venv --display-name "Python (.venv)"

```


Notes:
This dataset is an aggregated health survery dataset.
Instead of viewing each row as representing a single person, each row likely represents a specific health statistic for a population subgroup
(i.e. adults in a certain location, with age group, etc)
Response Row is empty (can typically be used when participants provide categorical response)
however, it should be empty since the dataset reports numerical values, which are stored in data value 


What is being measured? (Topic, Question)
How is it measured? (DataValue, DataValueType, DataValueUnit)
Where is it measured? (LocationAbbr, LocationDesc, Geolocation)
Who is being measured? (StratificationCategory1, Stratification1, etc.)


This is not individual patient data but aggregated survey statistics.
Each row represents a health measurement for a specific location, time, and subgroup.
DataValue is likely the key variable (instead of Response).
Analysis should focus on trends over time, geographic comparisons, and subgroup differences.

Note about stratification categories 