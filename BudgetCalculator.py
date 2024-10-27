import pandas as pd
import re

# Function for yes or no answers
def yesOrNo(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'n']:
            return response
        else:
            print("Invalid input. Please enter y or n.")

# Function to get users input for income
def getIncome():
    income = {}
    while True:
        while True:
            incomeSource = input("What is your source of income?: ").strip().title()
            if not re.match("^[A-Za-z][A-Za-z0-9 ]+$", incomeSource):
                print('Invalid input! Please enter a valid name using letters, numbers, and space only. Input must start with a letter.')
            else:
                break
        while True:
            try:
                incomeAmount = input(f'Enter your monthly income for {incomeSource} after taxes: $').strip()
                if not re.match(r'^\d+(\.\d{1,2})?$', incomeAmount):
                    raise ValueError('Please enter a positive number in the format of $xxxx or $xxxx.xx')
                incomeAmount = float(incomeAmount)
                if incomeAmount < 0:
                    raise ValueError("Income amount cannot be negative.")
                break
            except ValueError as e:
                print(f'Invalid input: {e}')
        income[incomeSource] = incomeAmount
        otherSources = yesOrNo("Are there any other streams of income? (y/n): ")
        if otherSources == 'n':
            break
    return income

# Function to get user Input for debts
def getDebts():
    debts = {}
    while True:
        while True:
            debtName = input("Enter the name of the debt: ").strip().title()
            if not re.match("^[A-Za-z][A-Za-z0-9 ]+$", debtName):
                print('Invalid input! Please enter a valid name using letters, numbers, and space only. Input must start with a letter.')
            else:
                break
        while True:
            try:
                debtAmount = input(f"Enter the monthly payment for {debtName}: $").strip()
                if not re.match(r'^\d+(\.\d{1,2})?$', debtAmount):
                    raise ValueError('Please enter a positive number in the format of $xxxx or $xxxx.xx')
                debtAmount = float(debtAmount)
                if debtAmount < 0:
                    raise ValueError("Income amount cannot be negative.")
                break
            except ValueError as e:
                print(f'Invalid input: {e}')
        debts[debtName] = debtAmount
        moreDebt = yesOrNo("Are there other monthly debts? (y/n): ")
        if moreDebt == 'n':
            break
    return debts

# Function to get the users input for expenses
def getExpenses():
    expenses = {}
    while True:
        while True:
            expenseName = input("Enter the name of your expense: ").strip().title()
            if not re.match("^[A-Za-z][A-Za-z0-9 ]+$", expenseName):
                print('Invalid input! Please enter a valid name using letters, numbers, and space only. Input must start with a letter.')
            else:
                break
        while True:
            try:
                expenseAmount = input(f'Enter expense amount for {expenseName}: $').strip()
                if not re.match(r'^\d+(\.\d{1,2})?$', expenseAmount):
                    raise ValueError('Please enter a positive number in the format of $xxxx or $xxxx.xx')
                expenseAmount = float(expenseAmount)
                if expenseAmount < 0:
                    raise ValueError("Income amount cannot be negative.")
                break
            except ValueError as e:
                print(f'Invalid input: {e}')
        expenses[expenseName] = expenseAmount
        otherExpenses = yesOrNo('Are there any other expenses? (y/n): ')
        if otherExpenses == 'n':
            break
    return expenses

# Function to get users input for savings
def getSavings():
    savings = {}
    while True:
        while True:
            savingsSource = input("Are you saving? (If yes, enter 'Savings'. If no, enter n): ").strip().title()
            if savingsSource != 'Savings' and savingsSource != 'N':
                print('Invalid input! Please enter a valid name using letters, numbers, and space only.\nInput must start with a letter.\nIf answer is no, please enter n')
            else:
                break
        if savingsSource == 'N':
            savings['Savings'] = 0
            break
        while True:
            try:
                savingAmount = input('How much do you put into your savings a month: $').strip()
                if not re.match(r"^\d+(\.\d{1,2})?$", savingAmount):
                    raise ValueError("Amount must be a positive number with up to two decimal places.")
                savingAmount = float(savingAmount)
                if savingAmount < 0:
                    raise ValueError("Amount cannot be negative.")
                break
            except ValueError:
                print(f"Invalid input: Please enter a positive number.")
        savings[savingsSource] = savingAmount
        break
    return savings

# Function to get users input for savings goal
def getSavingsGoal():
    savingsGoal = {}
    while True:
        while True:
            savingsGoalName = input("What are you saving for?: ").strip().title()
            if not re.match("^[A-Za-z][A-Za-z0-9 ]+$", savingsGoalName):
                print('Invalid input! Please enter a valid name using letters, numbers, and space only. Input must start with a letter.')
            else:
                break
        while True:
            try:
                savingGoalAmount = input(f'Enter amount you are trying to save for {savingsGoalName}: $').strip()
                if not re.match(r'^\d+(\.\d{1,2})?$', savingGoalAmount):
                    raise ValueError('Please enter a positive number in the format of $xxxx or $xxxx.xx')
                savingGoalAmount = float(savingGoalAmount)
                if savingGoalAmount < 0:
                    raise ValueError("Income amount cannot be negative.")
                break
            except ValueError as e:
                print(f'Invalid input: {e}')
        savingsGoal[savingsGoalName] = savingGoalAmount
        otherSavings = yesOrNo('Is there anything else you would like to save for? (y/n): ')
        if otherSavings == 'n':
            break    
    return savingsGoal

# Function to calculate budget
def getBudget(income, debts, expenses, savings):
    totalIncome = sum(income.values())
    totalDebts = sum(debts.values())
    totalExpenses = sum(expenses.values())
    totalSavings = sum(savings.values())
    totalRemaining = totalIncome - (totalDebts + totalExpenses + totalSavings)
    return totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining

# Function to calculate time to reach saving goals
def timeToGoal(totalSavings, savingsGoal, totalIncome):
    if totalSavings == 0:
        totalSavings = round(totalIncome * 0.20, 2)
        print(f'No savings was detected. Applying mothly savings to 20% of total income: ${totalSavings}')
    monthsToGoal = {goal: amount / totalSavings for goal, amount in savingsGoal.items() if totalSavings != 0}
    return monthsToGoal

# Function to create an Excel file with all the details and embed the graph
def createBudgetFile(filename, income, debts, expenses, savings, savingsGoal, totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining, monthsToGoal):
    # Create dataframes for different sections
    incomeDf = pd.DataFrame(list(income.items()), columns=["Income Source", "Monthly Income"])
    incomeDf.loc[len(incomeDf)] = ['Total Income', totalIncome] 

    debtsDf = pd.DataFrame(list(debts.items()), columns=["Debt Name", "Monthly Payment"])
    debtsDf.loc[len(debtsDf)] = ['Total Debts', totalDebts] 

    expensesDf = pd.DataFrame(list(expenses.items()), columns=["Expense Name", "Monthly Amount"])
    expensesDf.loc[len(expensesDf)] = ['Total Expenses', totalExpenses]  

    savingsDf = pd.DataFrame(list(savings.items()), columns=["Savings Source", "Monthly Amount"])
    savingsDf.loc[len(savingsDf)] = ['Total Savings', totalSavings]

    savingsGoalAndMonthsDf = pd.DataFrame({
        "Savings Goal": list(savingsGoal.keys()),
        "Goal Amount": list(savingsGoal.values()),
        "Months to Goal": list(monthsToGoal.values())
    })

    # Create a summary of totals for the blocks (Total Income, Total Expenses, etc.)
    summary_data = {
        "Monthly Totals": ["Total Income", "Total Debts", "Total Expenses", "Total Savings", "Remaining Budget"],
        "Amount": [totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining]
    }
    summaryDf = pd.DataFrame(summary_data)

    # Create the Excel writer object
    with pd.ExcelWriter(f"{filename}.xlsx", engine='xlsxwriter') as writer:
        # Write the summary data first (this will be the main table on the first page)
        summaryDf.to_excel(writer, sheet_name='Budget Overview', startrow=2, index=False)

        # Write the detailed tables below the summary
        incomeDf.to_excel(writer, sheet_name='Budget Overview', startrow=10, index=False)
        expensesDf.to_excel(writer, sheet_name='Budget Overview', startrow=10 + len(incomeDf) + 2, index=False)
        savingsDf.to_excel(writer, sheet_name='Budget Overview', startrow=10 + len(incomeDf) + len(expensesDf) + 4, index=False)
        debtsDf.to_excel(writer, sheet_name='Budget Overview', startrow=10 + len(incomeDf) + len(expensesDf) + len(savingsDf) + 6, index=False)
        savingsGoalAndMonthsDf.to_excel(writer, sheet_name='Budget Overview', startrow=10 + len(incomeDf) + len(expensesDf) + len(savingsDf) + len(debtsDf) + 8, index=False)

        # Access the xlsxwriter objects to add more customization
        workbook = writer.book
        worksheet = writer.sheets['Budget Overview']

        # Set column widths for proper spacing
        worksheet.set_column('A:A', 25)  # Adjust A column for better spacing
        worksheet.set_column('B:C', 18)  # Set column widths for B and C (Income, Expenses, etc.)

        # Add formats for header blocks and table headers
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#DDEBF7', 'border': 1})
        money_format = workbook.add_format({'num_format': '$#,##0', 'border': 1})

        # Merge cells and write Total Income, Total Expenses, Left to Spend blocks
        worksheet.merge_range('I2:J2', 'Left to Spend', header_format)
        worksheet.merge_range('I3:J3', totalRemaining, money_format)
        worksheet.merge_range('K2:L2', 'Total Income', header_format)
        worksheet.merge_range('K3:L3', totalIncome, money_format)
        worksheet.merge_range('M2:N2', 'Total Expenses', header_format)
        worksheet.merge_range('M3:N3', totalExpenses, money_format)

        # Add the title "Your Monthly Budget"
        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center', 'valign': 'vcenter'})
        worksheet.merge_range('A1:J1', 'Your Monthly Budget', title_format)

        # Add a pie chart to show all relevant totals
        pie_chart = workbook.add_chart({'type': 'pie'})
        pie_chart.add_series({
            'categories': ['Budget Overview', 2, 0, 6, 0],  # All totals
            'values':     ['Budget Overview', 2, 1, 6, 1],
            'data_labels': {'percentage': True},
        })
        pie_chart.set_title({'name': 'Budget Breakdown'})

        # Insert pie chart in the first sheet
        worksheet.insert_chart('D5', pie_chart)

        # Add a bar chart for Savings Goal Progress
        bar_chart = workbook.add_chart({'type': 'column'})
        bar_chart.add_series({
            'categories': ['Budget Overview', 10 + len(incomeDf) + len(expensesDf) + len(savingsDf) + len(debtsDf) + 9, 0,
                           10 + len(incomeDf) + len(expensesDf) + len(savingsDf) + len(debtsDf) + 8 + len(savingsGoalAndMonthsDf), 0],
            'values':     ['Budget Overview', 10 + len(incomeDf) + len(expensesDf) + len(savingsDf) + len(debtsDf) + 9, 2,
                           10 + len(incomeDf) + len(expensesDf) + len(savingsDf) + len(debtsDf) + 8 + len(savingsGoalAndMonthsDf), 2],
            'name': 'Months to Goal',
        })
        bar_chart.set_title({'name': 'Savings Goal Progress'})

        # Insert bar chart right below the pie chart
        worksheet.insert_chart('L5', bar_chart)

    print(f"Budget details saved to {filename}.xlsx")

# Main function
def main():
    income = getIncome()
    debts = getDebts()
    expenses = getExpenses()
    savings = getSavings()
    savingsGoal = getSavingsGoal()
    
    totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining = getBudget(income, debts, expenses, savings)
    monthsToGoal = timeToGoal(totalSavings, savingsGoal, totalIncome)
    
    filename = input("Enter the name for your Excel file (without extension): ")
    createBudgetFile(filename, income, debts, expenses, savings, savingsGoal, totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining, monthsToGoal)

if __name__ == "__main__":
    main()