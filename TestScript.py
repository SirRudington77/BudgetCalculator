import unittest
from unittest.mock import patch, mock_open
from BudgetCalculatorTest import getIncome, getDebts, getExpenses, getSavings, getSavingsGoal, getBudget, timeToGoal, createBudgetFile
import os

class TestBudgetCalculator(unittest.TestCase):

    @patch('builtins.input', side_effect=["Salary", "2000", "n"])
    def test_getIncome(self, mock_input):
        result = getIncome()
        self.assertEqual(result, {'Salary': 2000.0})

    @patch('builtins.input', side_effect=["Credit Card", "500", "y", "Car Note", "250", "n"])
    def test_getDebts(self, mock_input):
        result = getDebts()
        self.assertEqual(result, {'Credit Card': 500.0, 'Car Note': 250.0})

    @patch('builtins.input', side_effect=["Rent", "1200", "y", "Groceries", "300", "n"])
    def test_getExpenses(self, mock_input):
        result = getExpenses()
        self.assertEqual(result, {'Rent': 1200.0, 'Groceries': 300.0})

    @patch('builtins.input', side_effect=["Savings", "200", "n"])
    def test_getSavings(self, mock_input):
        result = getSavings()
        self.assertEqual(result, {'Savings': 200.0})

    @patch('builtins.input', side_effect=["Vacation", "1500", "y", "Home Renovation", "5000", "n"])
    def test_getSavingsGoal(self, mock_input):
        result = getSavingsGoal()
        self.assertEqual(result, {'Vacation': 1500.0, "Home Renovation": 5000.0})

    def test_getBudget(self):
        income = {'Salary': 4000.0}
        debts = {'Credit Card': 500.0, 'Car Note': 250.0}
        expenses = {'Rent': 1200.0, 'Groceries': 300.0}
        savings = {'Savings': 200.0}
        totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining = getBudget(income, debts, expenses, savings)
        self.assertEqual(totalIncome, 4000.0)
        self.assertEqual(totalDebts, 750.0)
        self.assertEqual(totalExpenses, 1500.0)
        self.assertEqual(totalSavings, 200.0)
        self.assertEqual(totalRemaining, 1550.0)

    def test_timeToGoal(self):
        totalSavings = 200.0
        savingsGoal = {'Vacation': 1500.0, "Home Renovation": 5000.0}
        totalIncome = 4000.0
        months_to_goal = timeToGoal(totalSavings, savingsGoal, totalIncome)
        self.assertEqual(months_to_goal, {'Vacation': 7.5, "Home Renovation": 25.0})

    @patch('builtins.input', side_effect=["BudgetFile"])
    def test_createBudgetFile(self, mock_input):
        income = {'Salary': 4000.0}
        debts = {'Credit Card': 500.0, 'Car Note': 250.0}
        expenses = {'Rent': 1200.0, 'Groceries': 300.0}
        savings = {'Savings': 200.0}
        savingsGoal = {'Vacation': 1500.0, "Home Renovation": 5000.0}
        totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining = getBudget(income, debts, expenses, savings)
        months_to_goal = timeToGoal(totalSavings, savingsGoal, totalIncome)

        filename = input("Enter the name for your Excel file (without extension): ")
        createBudgetFile(filename, income, debts, expenses, savings, savingsGoal, totalIncome, totalDebts, totalExpenses, totalSavings, totalRemaining, months_to_goal)
        
    
        self.assertTrue(os.path.isfile(f"{filename}.xlsx"))
        
        
        # os.remove(f"{filename}.xlsx")

if __name__ == '__main__':
    unittest.main()
