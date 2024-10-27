import pandas as pd
# import matplotlib.pyplot as plt
# import xlsxwriter
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
            expenseName = input("Enter the name of your expense: ")
            if not re.match("^[A-Za-z][A-Za-z0-9 ]+$", expenseName):
                print('Invalid input! Please enter a valid name using letters, numbers, and space only. Input must start with a letter.')
            else:
                break
        while True:
            try:
                expenseAmount = input(f'Enter expense amount for {expenseName}: $')
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
                savingAmount = input('How much do you put into your savings a month: $')
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
            savingsGoalName = input("What are you saving for?: ")
            if not re.match("^[A-Za-z][A-Za-z0-9 ]+$", savingsGoalName):
                print('Invalid input! Please enter a valid name using letters, numbers, and space only. Input must start with a letter.')
            else:
                break
        while True:
            try:
                savingGoalAmount = input(f'Enter amount you are trying to save for {savingsGoalName}: $')
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
        totalSavings = totalIncome * 0.20
        print(f'No savings was detected. Applying mothly savings to 20% of total income: ${totalSavings}')
    monthsToGoal = {goal: amount / totalSavings for goal, amount in savingsGoal.items() if totalSavings != 0}
    return monthsToGoal

# Function to create an Excel file with all the details and embed the graph
def createBudgetFile(filename, income, debts, expenses, savings, savingsGoal, totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining, monthsToGoal):
    data = {
        "Description": ["Total Income", "Total Debts", "Total Expenses", "Total Savings", "Remaining Budget"],
        "Amount": [totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining]
    }
    df = pd.DataFrame(data)
    
    # Convert dictionaries to DataFrames
    # incomeDf = pd.DataFrame(list(income.items()), columns=["Income Source", "Monthly Income"])
    debtsDf = pd.DataFrame(list(debts.items()), columns=["Debt Name", "Monthly Payment"])
    expensesDf = pd.DataFrame(list(expenses.items()), columns=["Expense Name", "Monthly Amount"])
    savingsDf = pd.DataFrame(list(savings.items()), columns=["Savings Source", "Monthly Amount"])
    savingsGoalDf = pd.DataFrame(list(savingsGoal.items()), columns=["Savings Goal", "Goal Amount"])
    monthsToGoalDf = pd.DataFrame(list(monthsToGoal.items()), columns=["Savings Goal", "Months to Goal"])
    
    # Create the Excel writer object
    with pd.ExcelWriter(f"{filename}.xlsx", engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Budget Summary', index=False)
        # incomeDf.to_excel(writer, sheet_name='Income', index=False)
        debtsDf.to_excel(writer, sheet_name='Debts', index=False)
        expensesDf.to_excel(writer, sheet_name='Expenses', index=False)
        savingsDf.to_excel(writer, sheet_name='Savings', index=False)
        savingsGoalDf.to_excel(writer, sheet_name='Savings Goals', index=False)
        monthsToGoalDf.to_excel(writer, sheet_name='Months to Goal', index=False)
        
        # Get the xlsxwriter objects
        workbook = writer.book
        chartSheet = workbook.add_worksheet('Budget Graph')
        
        # Create a pie chart in Excel
        chart = workbook.add_chart({'type': 'pie'})
        
        # Create the data for the pie chart
        chart.add_series({
            'categories': ['Budget Summary', 1, 0, 5, 0],
            'values':     ['Budget Summary', 1, 1, 5, 1],
            'data_labels': {'percentage': True},
        })
        
        # Insert the chart into the new worksheet
        chartSheet.insert_chart('B2', chart)
    
    print(f"Budget details saved to {filename}.xlsx")

""" Code that need to be looked at in order to fomat the excel spred sheet

def createBudgetFile(filename, income, debts, expenses, savings, savingsGoal, totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining, months_to_goal):
    data = {
        "Description": ["Total Income", "Total Debts", "Total Expenses", "Total Savings", "Remaining Budget"],
        "Amount": [totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining]
    }
    df = pd.DataFrame(data)
    
    # Convert dictionaries to DataFrames
    income_df = pd.DataFrame(list(income.items()), columns=["Income Source", "Monthly Income"])
    debts_df = pd.DataFrame(list(debts.items()), columns=["Debt Name", "Monthly Payment"])
    expenses_df = pd.DataFrame(list(expenses.items()), columns=["Expense Name", "Monthly Amount"])
    savings_df = pd.DataFrame(list(savings.items()), columns=["Savings Source", "Monthly Amount"])
    savingsGoal_df = pd.DataFrame(list(savingsGoal.items()), columns=["Savings Goal", "Goal Amount"])
    months_to_goal_df = pd.DataFrame(list(months_to_goal.items()), columns=["Savings Goal", "Months to Goal"])
    
    # Create the Excel writer object
    with pd.ExcelWriter(f"{filename}.xlsx", engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Budget Summary', index=False)
        income_df.to_excel(writer, sheet_name='Income', index=False)
        debts_df.to_excel(writer, sheet_name='Debts', index=False)
        expenses_df.to_excel(writer, sheet_name='Expenses', index=False)
        savings_df.to_excel(writer, sheet_name='Savings', index=False)
        savingsGoal_df.to_excel(writer, sheet_name='Savings Goals', index=False)
        months_to_goal_df.to_excel(writer, sheet_name='Months to Goal', index=False)
        
        # Get the xlsxwriter objects
        workbook = writer.book
        worksheet_summary = writer.sheets['Budget Summary']
        chart_sheet = workbook.add_worksheet('Budget Graph')
        
        # Apply formatting
        money_format = workbook.add_format({'num_format': '$#,##0.00', 'bold': True, 'font_color': 'green'})
        header_format = workbook.add_format({'bold': True, 'font_color': 'blue', 'bg_color': 'yellow'})
        
        for sheet in ['Budget Summary', 'Income', 'Debts', 'Expenses', 'Savings', 'Savings Goals', 'Months to Goal']:
            worksheet = writer.sheets[sheet]
            worksheet.set_column('A:A', 20, header_format)
            worksheet.set_column('B:B', 18, money_format)
        
        # Create a pie chart in Excel
        chart = workbook.add_chart({'type': 'pie'})
        
        # Create the data for the pie chart
        chart.add_series({
            'categories': ['Budget Summary', 1, 0, 5, 0],
            'values':     ['Budget Summary', 1, 1, 5, 1],
            'data_labels': {'percentage': True},
        })
        
        # Insert the chart into the new worksheet
        chart_sheet.insert_chart('B2', chart)
    
    print(f"Budget details saved to {filename}.xlsx")

"""

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