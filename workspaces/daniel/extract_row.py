import pandas as pd

import pandas as pd

def extract_cdc_data(df):
    """Extracts detailed information from the CDC Chronic Disease Indicators dataset.
    Parameters:
        df (DataFrame): Pandas DF containing cleaned dataset
    Returns:
        List[dict]: A list of dictionaries with detailed information from each row.
    """
    extracted_info = []

    for index, row in df.iterrows():
        info = {
            'Year': f"{row['YearStart']} - {row['YearEnd']}",
            'State': row['LocationDesc'],
            'Data Source': row['DataSource'],
            'Topic': row['Topic'],
            'Question': row['Question'],
            'Unit': row['DataValueUnit'],
            'Rate Type': row['DataValueType'],
            'Hospitalization Rate': row['DataValue'],
            'Confidence Interval': f"{row['LowConfidenceLimit']} - {row['HighConfidenceLimit']}",
            'Stratification Category': row['StratificationCategory1'],
            'Stratification Group': row['Stratification1'],
            'Geolocation': row['Geolocation'],
            'Question ID': row['QuestionID'],
            'Stratification Category ID': row['StratificationCategoryID1'],
            'Stratification ID': row['StratificationID1']
        }
        
        extracted_info.append(info)

    return extracted_info

def generate_cdc_sumamry(df):
    """Reads the CDC Chronic Disease Indicators dataset and generates a readable summary for each row.
    Parameters:
        df[DataFrame]: A cleaned Pandas DataFrame
    Returns:
        List[str]: A list of formatted summaries from each row.
    """
    summaries = []
    for index, row in df.iterrows():
        # Extract necessary data
        year = row['YearStart']
        state = row['LocationDesc']
        data_source = row['DataSource']
        topic = row['Topic']
        question = row['Question']
        unit = row['DataValueUnit']
        rate_type = row['DataValueType']
        rate = row['DataValue']
        low_conf = row['LowConfidenceLimit']
        high_conf = row['HighConfidenceLimit']
        strat_category = row['StratificationCategory1']
        strat_group = row['Stratification1']
        
        # Generate the readable summary
        summary = (
            f"In {year}, {strat_group} residents in {state} had a {question} rate of "
            f"{rate} {unit} for {topic} based on {data_source}. "
            f"This rate is reported as a {rate_type} and has a 95% confidence interval "
            f"between {low_conf} and {high_conf}, indicating the precision of this estimate."
        )
        
        summaries.append(summary)

    return summaries

# Example usage:
path = '/home/daniel.lien/dev/homework/data/cleaned_copd_data.csv'
df = pd.read_csv(path)
data_summary = extract_cdc_data(df)

# Display first 5 extracted summaries
for summary in data_summary[:5]:
    pass
    # print(summary)

cdc_summaries = generate_cdc_sumamry(df)
for summary in cdc_summaries[:5]:
    print(summary)

# print(df['Question'].unique())
# print(df['QuestionID'].unique())
# print(df.iloc[0]['Question'])
"""
What This Data Tells You:
In 2019, Hispanic residents in Arizona had a hospitalization rate of 58.19 per 1,000 people
for Chronic Obstructive Pulmonary Disease (COPD) based on CMS Part A claims data. 
This rate has a 95% confidence interval between 54.57 and 61.82, indicating the precision of this estimate.
"""




COPD_QUESTION_BANK = ['Hospitalization for chronic obstructive pulmonary disease as any diagnosis, Medicare-beneficiaries aged 65 years and older'
 'Chronic obstructive pulmonary disease mortality among adults aged 45 years and older, underlying cause'
 'Chronic obstructive pulmonary disease mortality among adults aged 45 years and older, underlying or contributing cause'
 'Chronic obstructive pulmonary disease among adults'
 'Current smoking among adults with chronic obstructive pulmonary disease'
 'Hospitalization for chronic obstructive pulmonary disease as principal diagnosis, Medicare-beneficiaries aged 65 years and older']


"""Need to create a Mapping for Question bank
"""