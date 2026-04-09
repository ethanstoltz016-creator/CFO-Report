#line 23 showed 5 spaces in the middle of the email field, reading "vbe     nchl@narod.ru", record deleted
#line 4929 had no data, record deleted
#line 7320 had extra column after ip, with text "agan", record deleted
# imports
import pandas as pd
import matplotlib.pyplot as plt

#open data file
df = pd.read_csv("data\\eStoreData.csv",header=0)

#functions
def apct(pct, allvals):
    absolute = int(round(pct/100.*sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d})"

def currency_fmt(x):
    if x >= 1_000_000:
        return f'${x/1_000_000:.4f}M'
    return f'${x/1_000:.4f}K'

#################### Department Spending ####################
# Group by the 'Department' section and sum the 'Cost' sections
result = df.groupby('department')['cost'].sum().reset_index()

# 1. Create the figure
fig, ax = plt.subplots(figsize=(10, 6))

# 2. Plot without labels on the wedges (labels=None)
# Use 'pctdistance' to push the percentages further out or in
wedges, texts, autotexts = ax.pie(
    result['cost'], 
    labels=None, 
    autopct=lambda pct: apct(pct, result['cost']),
    pctdistance=0.85, 
    startangle=140
)

# Shrink the percentage text and rotate it
# This prevents them from bumping into each other in small slices
for autotext in autotexts:
    autotext.set_fontsize(7)  # Smaller font
    autotext.set_rotation(45)

# 3. Add a legend to the side
# This keeps the department names clear and organized
ax.legend(
    wedges, 
    result['department'],
    title="Departments",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1) # Moves legend outside the plot area
)

ax.set_title('Total Values by Section')
plt.tight_layout()
plt.show()
plt.close()

#Bar chart
department_costs = df.groupby('department')['cost'].sum()
x=[]
departments = df["department"].unique()
for i in range(len(departments)):
    x.append(departments[i])
y=[]
for i in range(len(departments)):
    y.append(department_costs.iloc[i])

plt.bar(x,y)
plt.ylim(1800000,2500000)
plt.show()

#################### Top/Bottom Spending ####################
# 1. Sort the Departments by spending
sortedDeps = result.sort_values(by='cost', ascending=False)

# 2. Get the top 5 departments and the bottom 5 departments in terms of spending
top5_df = sortedDeps.head(5)
bottom5_df = sortedDeps.tail(5)

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

# 3. Plot the first DataFrame on the first axis (ax1)
TopBars = ax1.bar(top5_df['department'], top5_df['cost'], color='skyblue')
ax1.bar_label(TopBars, labels=[currency_fmt(x) for x in top5_df['cost']], padding=3, rotation=45)
ax1.set_title('Top 5 Departments')
ax1.set_xlabel('Departments')
ax1.set_ylabel('Cost')
ax1.set_ylim(0, top5_df['cost'].max() * 1.25) # Added padding for rotated text

# 4. Plot the second DataFrame on the second axis (ax2)
BottomBars = ax2.bar(bottom5_df['department'], bottom5_df['cost'], color='salmon')
ax2.bar_label(BottomBars, labels=[currency_fmt(x) for x in bottom5_df['cost']], padding=3, rotation=45)
ax2.set_title('Bottom 5 Departments')
ax2.set_xlabel('Category')
ax2.set_ylabel('Cost')
ax2.set_ylim(0, bottom5_df['cost'].max() * 1.25)

# 5. Adjust layout for better spacing and display the plot
plt.tight_layout() #
plt.show()
plt.close()

#Data Cleaning
invalid_prefixes = ('0.', '192.', '127.', '255.')
df = df[~df['ip'].str.startswith(invalid_prefixes)]
showClean = input("Would you like to show the Clean data? (y/n): ")
if showClean.lower() == "y":
    print(df)

#Rerun Department and Top/Bottom Analyses
#################### Department Clean ####################
result = df.groupby('department')['cost'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))

wedges, texts, autotexts = ax.pie(
    result['cost'], 
    labels=None, 
    autopct=lambda pct: apct(pct, result['cost']),
    pctdistance=0.85, 
    startangle=140
)

for autotext in autotexts:
    autotext.set_fontsize(7)  # Smaller font
    autotext.set_rotation(45)

ax.legend(
    wedges, 
    result['department'],
    title="Departments",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1) # Moves legend outside the plot area
)

ax.set_title('Total Values by Section-Clean')
plt.tight_layout()
plt.show()
plt.close()

#################### Top/Bottom Spending - Clean ####################
# 1. Sort the Departments by spending
sortedDeps = result.sort_values(by='cost', ascending=False)

# 2. Get the top 5 departments and the bottom 5 departments in terms of spending
top5_df = sortedDeps.head(5)
bottom5_df = sortedDeps.tail(5)

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

# 3. Plot the first DataFrame on the first axis (ax1)
TopBars = ax1.bar(top5_df['department'], top5_df['cost'], color='skyblue')
ax1.bar_label(TopBars, labels=[currency_fmt(x) for x in top5_df['cost']], padding=3, rotation=45)
ax1.set_title('Top 5 Departments-Clean')
ax1.set_xlabel('Departments')
ax1.set_ylabel('Cost')
ax1.set_ylim(0, top5_df['cost'].max() * 1.25) # Added padding for rotated text

# 4. Plot the second DataFrame on the second axis (ax2)
BottomBars = ax2.bar(bottom5_df['department'], bottom5_df['cost'], color='salmon')
ax2.bar_label(BottomBars, labels=[currency_fmt(x) for x in bottom5_df['cost']], padding=3, rotation=45)
ax2.set_title('Bottom 5 Departments-Clean')
ax2.set_xlabel('Category')
ax2.set_ylabel('Cost')
ax2.set_ylim(0, bottom5_df['cost'].max() * 1.25)

# 5. Adjust layout for better spacing and display the plot
plt.tight_layout() #
plt.show()
plt.close()

#################### Student Purchases ####################
students = df[df['email'].astype(str).str.endswith('.edu')]

StudentNum = len(students)
StudentSum = students['cost'].sum()
print(f"{StudentNum} Student Purchases") 
print(f"Total Costs: {StudentSum}") 

# Group by the 'Department' section
    # sum the 'Cost' sections
    # find the total number of records in each section
studentsSorted = students.groupby('department')['cost'].agg(
    total_cost='sum', 
    purchase_count='count'
).reset_index()

# Sort by purchase count to see the busiest departments
studentsSorted = studentsSorted.sort_values(by='purchase_count', ascending=False)

print("Student Purchases by Department:")
print(studentsSorted)

# Create the figure with two side-by-side subplots
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

# --- Plot 1: Total Student Purchase Costs ---
TotalCosts = ax1.bar(studentsSorted['department'], studentsSorted['total_cost'], color='skyblue')
ax1.set_title('Total Student Purchase Costs by Department')
ax1.set_xlabel('Departments')
ax1.set_ylabel('Cost ($)')
ax1.tick_params(axis='x', rotation=45) # Rotate labels for readability
# Set y-limit slightly higher than max value for space
ax1.set_ylim(0, studentsSorted['total_cost'].max() * 1.15) 

# Add currency labels above bars
ax1.bar_label(TotalCosts, fmt='${:,.0f}', padding=3, fontsize=9)
ax1.set_ylim(0, studentsSorted['total_cost'].max() * 1.2) # Extra space for labels

# --- Plot 2: Total Student Purchase Count ---
TotalPurchases = ax2.bar(studentsSorted['department'], studentsSorted['purchase_count'], color='salmon')
ax2.set_title('Total Student Purchase Counts by Department')
ax2.set_xlabel('Departments')
ax2.set_ylabel('Number of Purchases')
ax2.tick_params(axis='x', rotation=45) # Rotate labels for readability
# Set y-limit slightly higher than max value for space
ax2.set_ylim(0, studentsSorted['purchase_count'].max() * 1.15)

# Add count labels above bars
ax2.bar_label(TotalPurchases, padding=3, fontsize=10)
ax2.set_ylim(0, studentsSorted['purchase_count'].max() * 1.2) # Extra space for labels

plt.tight_layout()
plt.show()

#################### Credit Card Analysis ####################
Visa = df['card'].astype(str).str.startswith('4')
Mastercard = df[df['card'].astype(str).str.startswith(('5', '2'))]
VRows = len(Visa)
MRows = len(Mastercard)
cardCats = ['Visa','Mastercard']
cardVals = [VRows,MRows]
plt.bar(cardCats,cardVals)
plt.title('Visa vs Mastercard Purchases')
plt.ylabel('')
plt.show()

#################### Targeted Survey ####################
Survey = df[df['state'] == 'Indiana']

pNumberList = Survey['phoneNumber'].tolist()
print(pNumberList)

surveyNum = len(Survey)
surveySum = Survey['cost'].sum()

print(f"{surveyNum} Indiana Resident Purchases") 
print(f"Total Costs: {surveySum}")

SurveySorted = Survey.groupby('department')['cost'].sum().reset_index()

print("Indiana Resident Purchases by Department")
print(SurveySorted)

plt.pie(SurveySorted['cost'], 
        labels=SurveySorted['department'], 
        autopct=lambda pct: apct(pct, SurveySorted['cost'])
)
plt.title('Indiana Resident Purchases by Department')
plt.ylabel('')
plt.show()
plt.close()

#################### Top 3 Purchasers ####################
company_totals = df.groupby('company')['cost'].sum().sort_values(ascending=False)

#  Get Names of the Top 3 Companies
top3_names = company_totals.head(3).index
top3_values = company_totals.head(3).values

# --- Top 3 Total Purchasers Pie Chart ---
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.pie(top3_values, labels=top3_names, autopct=lambda p: f'${p*sum(top3_values)/100:,.2f}')
plt.title('Top 3 Purchasers (Total)')

plt.tight_layout()
plt.show()

# Breakdown by department
# Filter original df for only these 3 companies
top3_details = df[df['company'].isin(top3_names)]
pivot_df = top3_details.groupby(['company', 'department'])['cost'].sum().unstack()

# Plot on the second subplot
ax2 = plt.subplot(1, 2, 2)
pivot_df.plot(kind='barh', ax=ax2, figsize=(10, 6), stacked=False)
plt.title('Cost Breakdown for Top 3 Companies')
plt.legend(title='Departments', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()