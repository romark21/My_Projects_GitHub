from datetime import datetime
import pandas as pd


class Wallet:
    def __init__(self, name):
        self.name = name

    def add_data(self):
        current_datetime = (a := datetime.now()).strftime("%H:%M:%S %d-%m-%Y")
        summa = float(input(f'Enter the price of {self.name}: '))
        description = input(f'Enter a description of your {self.name}: ')
        template_wallet_data = {'summa': [summa], 'description': [description], 'date': [current_datetime]}
        df = pd.DataFrame(template_wallet_data)
        if self.name == 'income':
            print(f"In your wallet added {summa:.2f}€ for {description}.")
            print('---' * 20)
        else:
            print(f"You spent {summa:.2f}€ to {description}.")
            print('---' * 20)
        return df

    def save_data_csv(self, data):
        data.to_csv(f'{self.name}.csv', mode='a', index=False, header=True)

    def read_data_csv(self):
        read_csv = pd.read_csv(f'{self.name}.csv', delimiter=',')
        return read_csv

    def balance(self, data):
        value = sum(data['summa'])
        return value


def main():
    income = Wallet('income')
    outcome = Wallet('outcome')
    while True:
        income_summa = income.balance(income.read_data_csv())
        outcome_summa = outcome.balance(outcome.read_data_csv())
        user_choose = int(input(f" 1 - Add income.\n"
                                f" 2 - Add outcome.\n"
                                f" 3 - View wallet balance.\n"
                                f" 4 - View total income.\n"
                                f" 5 - View total outcome.\n"
                                f"Select the action you need and input the command number: "))
        if user_choose == 1:
            income.save_data_csv(income.add_data())

        elif user_choose == 2:
            outcome.save_data_csv(outcome.add_data())

        elif user_choose == 3:
            print(f'In your wallet is: {income_summa - outcome_summa:.2f}€')


if __name__ == '__main__':
    main()
