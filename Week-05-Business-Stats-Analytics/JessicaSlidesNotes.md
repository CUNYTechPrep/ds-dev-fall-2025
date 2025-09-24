# INSTRUCTOR GUIDE: Vibe Coding Data Cleaning Exercise

## For Jessica and TAs - What Students Need to Know (Put in Slides)

## CRITICAL CONCEPTS FOR SLIDES (What I Removed from Exercise)

### 1. **Data Cleaning Fundamentals

**Numbers That Aren't Numbers:**
- Salary data contains commas: "55,000" vs 55000
- Dollar signs and formatting: "$55,000" 
- **CATCH:** Ranges like "$50,000 - $60,000" (need midpoint)
- **CATCH:** Different currencies need conversion (USD, GBP, CAD, EUR)

**Inconsistent Categories:**
- Job titles: "Software Engineer" vs "software engineer" vs "SWE" vs "Developer"
- Location variations: "NY" vs "New York" vs "New York State"  
- **CATCH:** Case sensitivity matters in string matching

**Mixed Units/Scales:**
- All numbers must have same unit/currency for fair comparison
- Experience in ranges: "5-7 years" vs "21-30 years" vs "1 year or less"
- **CATCH:** Can't compare salaries in different currencies directly

### 2. **Vibe Coding Best Practices

**Work in Small Increments:**
- Clean ONE thing at a time, then validate
- Don't try to fix everything in one massive prompt
- **Example flow:** Load data → Check one column → Clean that column → Validate → Move to next

**Effective Prompting Strategies:**
```
GOOD PROMPTS:
- "Show me how to identify missing values in the salary column"
- "Write code to standardize job titles containing 'engineer' variations"  
- "Help me extract numeric values from salary text with commas and dollar signs"
- "Create a function to convert experience ranges to numeric years"

BAD PROMPTS (warn against these):
- "Clean my data" (too vague)
- "Fix everything" (not specific)
- "Make it work" (no direction)
```

**Validation is KEY:**
- Always check: "Do these numbers make business sense?"
- After cleaning salaries: "Are values in reasonable range ($20K-$500K)?"
- After filtering: "Do I have enough data points for valid analysis?"
- **CATCH:** AI can make mistakes - students must verify outputs

### 3. **Business Logic Decisions **

**What Counts as "Software Engineer"?**
- Must decide which job titles qualify
- Should include variations: Developer, Programmer, SWE, etc.
- **CATCH:** Exact string matching won't work

**What Defines "Tech Workers"?**
- Industry categorization required
- Must exclude consulting/finance that mentions "tech"
- Need consistent definition across questions

**Statistical Considerations:**
- **CATCH:** Some states have 1 respondent, others have 500+ 
- Need minimum sample sizes for valid comparisons
- Decide: Mean vs Median for "average"?

---

## DATA CHALLENGES THEY WILL FACE (DONT DIRECTLY PUT IN SLIDES JUST FOR YOU TO KNOW)

### Currency Conversion Challenge
- Dataset has: USD (majority), GBP, CAD, EUR, others
- **Must convert to same currency** for fair comparison
- Need 2021 exchange rates (approximately):
  - GBP to USD: ×1.38
  - CAD to USD: ×0.81  
  - EUR to USD: ×1.18

### Experience Data Parsing
- Text ranges: "5-7 years", "8-10 years", "21-30 years"
- Special cases: "1 year or less", "41 years or more"
- **Must convert to numbers** for correlation analysis

### Outlier Handling
- Some salaries: $15, $5000000, clearly wrong entries
- **Business judgment needed:** What's reasonable range?
- Suggestion: $10K - $500K for most roles

### Location Standardization  
- US identification: "United States", "USA", "US", "America"
- State variations: "DC", "D.C.", "Washington DC", "District of Columbia"
- **CATCH:** Inconsistent formatting requires mapping