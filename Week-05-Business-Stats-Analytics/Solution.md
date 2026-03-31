# Solution Guide: Vibe Coding Data Cleaning Challenge

## Expected Final Answers

Based on comprehensive analysis of the Ask A Manager 2021 salary survey:

1. **Median salary for Software Engineers in US:** $133,000
2. **US state with highest average tech salary:** California ($154,294 average)
3. **Salary increase per year of experience in tech:** ~$1,493 per year
4. **Industry with highest median salary (non-tech):** Law ($95,800 median)

**Bonus Questions:**
5. **Gender salary gap in tech:** Varies by cleaning approach, typically 10-20% gap
6. **Master's vs Bachelor's salary difference:** Typically $10-20K higher for Master's

## Key Data Cleaning Challenges Students Will Face

**Cleaning approach:**
```python
def clean_salary(salary_str, currency):
    # Remove formatting, handle ranges, convert currencies
    # Filter reasonable ranges (e.g., $1K-$1M)
    # Return numeric value in USD
```


Students' answers should fall within these ranges:

1. **Software Engineer median:** $125K - $140K ✓
2. **Top tech state:** California, Washington, or New York ✓
3. **Experience increase:** $1K - $2.5K per year ✓
4. **Top non-tech industry:** Law, Finance/Banking, or Consulting ✓

## Some code I wrote, I vibe coded the rest and made sure it all makes sense

```python
import pandas as pd
import numpy as np


df = pd.read_csv('../Week-02-Pandas-Part-2-and-DS-Overview/data/Ask A Manager Salary Survey 2021 (Responses) - Form Responses 1.tsv', sep='\t')


df = df.rename(columns={
    "What is your annual salary? (...)": "salary",
    "Please indicate the currency": "currency",
    "Job title": "job_title",
    "What industry do you work in?": "industry",
    "What country do you work in?": "country",
    "If you're in the U.S., what state do you work in?": "us_state",
    "How many years of professional work experience do you have overall?": "experience"
})

def clean_salary(salary_str, currency):
    if pd.isna(salary_str) or pd.isna(currency):
        return np.nan
    
    salary_str = str(salary_str).replace('$', '').replace(',', '').strip()
    
    if '-' in salary_str:
        try:
            parts = salary_str.split('-')
            salary = (float(parts[0]) + float(parts[1])) / 2
        except:
            return np.nan
    else:
        try:
            salary = float(salary_str)
        except:
            return np.nan

    if currency == 'GBP':
        salary *= 1.38
    elif currency == 'CAD':
        salary *= 0.81
    elif currency == 'EUR':
        salary *= 1.18
    elif currency not in ['USD', 'US']:
        return np.nan

    if salary < 1000 or salary > 1000000:
        return np.nan
        
    return salary

df['salary_clean'] = df.apply(lambda row: clean_salary(row['salary'], row['currency']), axis=1)

def is_software_engineer(title):
    if pd.isna(title):
        return False
    title_lower = title.lower()
    keywords = ['software engineer', 'developer', 'programmer']
    return any(keyword in title_lower for keyword in keywords)

df['is_software_engineer'] = df['job_title'].apply(is_software_engineer)


df_us = df[df['country'].str.contains('United States|US|USA', na=False, case=False)]


print("1. Software Engineer median salary:")
se_salaries = df_us[df_us['is_software_engineer'] & df_us['salary_clean'].notna()]
print(f"${se_salaries['salary_clean'].median():,.0f}")

tech_workers = df_us[df_us['industry'].str.contains('Computing|Tech|Technology', na=False) & df_us['salary_clean'].notna()]
state_avg = tech_workers.groupby('us_state')['salary_clean'].agg(['mean', 'count'])
state_avg = state_avg[state_avg['count'] >= 5]
top_state = state_avg.sort_values('mean', ascending=False).iloc[0]
print(f"{top_state.name}: ${top_state['mean']:,.0f}")
```

This exercise is designed to:
1. **Force problem-solving:** No step-by-step hints means students must think and problem solve through each decision. For example, they need to be careful before just doing "average", they should ask the LLM: "Should I use mean or median for average salary? What are the pros and cons of each? How do outliers affect each measure?" This kind of critical thinking dialogue with AI is essential vibe coding.

2. **Teach real skills:** Data cleaning decisions mirror real world work, there's rarely one "correct" approach, but there are better and worse approaches that require justification.

3. **Build AI collaboration:** Students learn to prompt effectively through iteration, they can't just say "find the average" but must engage in nuanced conversations about methodology, validation, and business logic.

4. **Validate systematically:** Multiple approaches can lead to correct answers, but students must validate their decisions at each step and ensure their final results make business sense.

The key is that students must make their own cleaning decisions while arriving at approximately correct final answers.


**Sample Size Filtering (`count >= 5`):** For statistical validity, I only include states with at least 5 tech workers. States with 1-2 respondents aren't reliable for comparison - students should discuss this threshold with AI.

**Currency Conversion Rates:** Used 2021 historical rates (GBP: 1.38, CAD: 0.81, EUR: 1.18). Students need to research these, not guess.

**Salary Range Handling:** Taking midpoint of ranges like "$50,000-$60,000" is a reasonable approach, but students could argue for other methods (minimum, maximum, weighted average).

**Outlier Filtering:** $1K-$1M range removes obvious data entry errors. Students should validate this makes business sense and discuss edge cases.

**Job Title Matching:** Using `any(keyword in title_lower)` catches variations like "Senior Software Engineer" and "Software Developer". Students need to decide what counts as "software engineer."

**Industry Classification:** "Computing|Tech|Technology" is one approach, but students might include/exclude different industries. The key is being consistent across all questions.

**Mean vs Median Choice:** Code uses median for salary comparisons (more robust to outliers) but mean for state averages (as requested). Students should understand when to use each.