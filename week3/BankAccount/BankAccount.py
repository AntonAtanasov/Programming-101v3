class BankAccount:
    def __init__(self, name, balance, currency):
        if balance < 0:
            raise ValueError("Start balance cannot be smaller than 0")
        self.name = str(name)
        self.my_balance = balance
        self.currency = str(currency)
        self.list_history = []
        start_message = ("Created account for {} with balance of {}{}")
        self.list_history.append(start_message.format(self.name, self.my_balance, self.currency))

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Cannot deposit negative amount.")
        self.my_balance += amount
        message = "Deposited {}{}".format(amount, self.currency)
        self.list_history.append(message)

    def currency(self):
        return self.__currency

    def balance(self):
        message = "Balance check -> {}".format(self.my_balance)
        self.list_history.append(message)
        return self.my_balance

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Cannot withdraw negative amount.")
        if self.my_balance >= amount:
            self.my_balance -= amount
            return True
        else:
            return False

    def __str__(self):
        message = "Bank account for {} with balance of {}{}"
        return message.format(self.name, self.amount, self.currency)

    def __int__(self):
        return self.balance

    def transfer_to(self, account, amount):
        if amount < 0 or self.my_balance <= amount or self.currency != account.currency:
            raise ValueError
        if self.my_balance >= amount and self.currency == account.currency:
            self.my_balance -= amount
            account.my_balance += amount
            return True
        else:
            return False

    def history(self):
        return self.list_history
