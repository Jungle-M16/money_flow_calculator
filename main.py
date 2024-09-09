import matplotlib.pyplot as plt
import pandas as pd

class MoneyFlow:
    def __init__(self, initial_salary, salary_tax_rate, vat_rate, cycles, personuafslattur):
        self.initial_salary = initial_salary
        self.salary_tax_rate = salary_tax_rate
        self.vat_rate = vat_rate
        self.cycles = cycles
        self.personuafslattur = personuafslattur
        self.history = []
        self.total_government_money = 0  # Track cumulative government collections

    def apply_salary_tax(self, amount):
        # Calculate the salary tax based on the salary tax rate
        salary_tax = amount * self.salary_tax_rate

        # Apply the persónuafsláttur (personal tax credit)
        salary_tax -= self.personuafslattur  # Reduce the tax by persónuafsláttur

        # Ensure tax doesn't go below 0
        if salary_tax < 0:
            salary_tax = 0

        # The amount after tax is deducted
        taxed_amount = amount - salary_tax

        return taxed_amount, salary_tax


    def apply_vat(self, amount):
        vat_deducted = amount * (1 - self.vat_rate)
        vat_tax = amount * self.vat_rate
        return vat_deducted, vat_tax

    def simulate(self):
        current_money = self.initial_salary

        # Add the first step: showing the initial salary before any tax
        self.history.append({
            'Cycle': 0,
            'Event': 'Initial Salary',
            'Amount': current_money,
            'Government Collected': 0,
            'Total Government Collected': 0,
            'Percent of Initial Salary Collected': 0
        })

        for i in range(self.cycles):
            # Phase 1: Earn salary and apply salary tax
            net_salary, salary_tax = self.apply_salary_tax(current_money)
            self.total_government_money += salary_tax
            self.history.append({
                'Cycle': i + 1,
                'Event': 'Salary Tax',
                'Amount': net_salary,
                'Government Collected': salary_tax,
                'Total Government Collected': self.total_government_money,
                'Percent of Initial Salary Collected': (self.total_government_money / self.initial_salary) * 100
            })
            
            # Phase 2: Spend money on something that has VAT
            after_vat, vat_tax = self.apply_vat(net_salary)
            self.total_government_money += vat_tax
            self.history.append({
                'Cycle': i + 1,
                'Event': 'VAT Tax',
                'Amount': after_vat,
                'Government Collected': vat_tax,
                'Total Government Collected': self.total_government_money,
                'Percent of Initial Salary Collected': (self.total_government_money / self.initial_salary) * 100
            })

            # Update current money to be used in the next cycle (assuming it's the new salary)
            current_money = after_vat

        return self.total_government_money, current_money

    def get_history(self):
        return self.history

    def plot_history(self):
        cycles = [entry['Cycle'] for entry in self.history if entry['Event'] == 'VAT Tax']
        amounts = [entry['Amount'] for entry in self.history if entry['Event'] == 'VAT Tax']
        
        plt.plot(cycles, amounts, marker='o')
        plt.title("Money Reduction Due to Taxes Across Cycles")
        plt.xlabel("Cycle")
        plt.ylabel("Remaining Money After Tax")
        plt.grid(True)
        plt.show()


# Simulation Parameters
initial_salary = 1100  # Starting salary
personuafslattur = 64  # Threshold before taking income tax
salary_tax_rate = 0.35  # 35% salary tax
vat_rate = 0.24  # 24% VAT
cycles = 12  # Number of cycles (iterations)

# Create and run the simulation
simulation = MoneyFlow(initial_salary, salary_tax_rate, vat_rate, cycles, personuafslattur)
total_government_money, remaining_money = simulation.simulate()

# Calculate percentage of total money collected by the government
total_collected_percentage = (total_government_money / initial_salary) * 100

# Print the total government money and the remaining money
print(f"Total money the government collected: {total_government_money}")
print(f"Remaining money after {cycles} cycles: {remaining_money}")
print(f"Total % collected by the government: {total_collected_percentage:.2f}%")

# Print the history as a DataFrame
df_history = pd.DataFrame(simulation.get_history())
print(df_history)

# Plot the results
simulation.plot_history()
