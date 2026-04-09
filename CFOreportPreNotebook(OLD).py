#line 23 showed 5 spaces in the middle of the email field, reading "vbe     nchl@narod.ru", record deleted
#line 4929 had no data, record deleted
#line 7320 had extra column after ip, with text "agan", record deleted
#imports
import pandas as pd
import matplotlib.pyplot as plt   #graphing utility
import math
#import numpy as np

def func(pct, allvals):
    absolute = int(round(pct/100.*sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d})"

def currency_fmt(x):
    if x >= 1_000_000:
        return f'${x/1_000_000:.4f}M'
    return f'${x/1_000:.4f}K'
#open data file
df = pd.read_csv("data\\eStoreData.csv",header=0)

#Department Spending
# Group by the 'Department' section and sum the 'Cost' sections
result = df.groupby('department')['cost'].sum().reset_index()

plt.pie(result['cost'], 
        labels=result['department'], 
        autopct=lambda pct: func(pct, result['cost'])
)

plt.title('Total Values by Section')
plt.ylabel('') # Hides the 'Value' label on the side
plt.show()
plt.cla()

#Top/Bottom
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

#Clean
invalid_prefixes = ('0.', '192.', '127.', '255.')
df = df[~df['ip'].str.startswith(invalid_prefixes)]

#Rerun Department and Top/Bottom Analyses
result = df.groupby('department')['cost'].sum().reset_index()
#we can reuse the function from earlier
plt.pie(result['cost'], 
        labels=result['department'], 
        autopct=lambda pct: func(pct, result['cost'])
)
plt.title('Total Values by Section-Clean')
plt.ylabel('')
plt.show()
plt.cla()
########################Top/Bottom Clean######################################
#Top/Bottom
sortedDeps = result.sort_values(by='cost', ascending=False)

top5_df = sortedDeps.head(5)
bottom5_df = sortedDeps.tail(5)

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

#set labels for bar values
TopBars = plt.bar(top5_df['department'], top5_df['cost'], color='skyblue')
BottomBars = plt.bar(bottom5_df['department'], bottom5_df['cost'], color='skyblue')

# 3. Plot the first DataFrame on the first axis (ax1)
ax1.bar(top5_df['department'], top5_df['cost'], color='skyblue')
ax1.bar_label(TopBars, padding=5)
ax1.set_title('Top 5 Departments')
ax1.set_xlabel('Departments')
ax1.set_ylabel('Cost')

# 4. Plot the second DataFrame on the second axis (ax2)
ax2.bar(bottom5_df['department'], bottom5_df['cost'], color='salmon')
ax2.bar_label(BottomBars, padding=5)
ax2.set_title('Bottom 5 Departments')
ax2.set_xlabel('Category')
ax2.set_ylabel('Cost')

# 5. Adjust layout for better spacing and display the plot
plt.tight_layout() #
plt.show()

#Student Purchases
student = df.groupby('department')['cost'].sum().reset_index()

#Credit Card Analysis
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
plt.cla()
#Target Survey

#Top Purchasers
top3purchasers = sortedDeps.head(3)
plt.pie(top3purchasers['cost'], 
        labels=top3purchasers['department'], 
        autopct=lambda pct: func(pct, top3purchasers['cost'])
)
plt.title('Top 3 Purchaser')
plt.ylabel('') # Hides the 'Value' label on the side
plt.show()
plt.cla()