
# Домашнее задание по теме "Блокировки потоков для доступа к общим данным"
# Цель задания:
# Практически применить знания о механизмах блокировки потоков в Python, используя класс Lock из модуля threading.
#
# Задание:
# Реализуйте программу, которая имитирует доступ к общему ресурсу с использованием механизма блокировки потоков.
#
# Класс BankAccount должен отражать банковский счет с балансом и методами для пополнения и снятия денег.
# Необходимо использовать механизм блокировки, чтобы избежать проблемы гонок (race conditions) при модификации общего ресурса.
#
# Пример работы:
# def deposit_task(account, amount):
#     for _ in range(5):
#         account.deposit(amount)
#
# def withdraw_task(account, amount):
#     for _ in range(5):
#         account.withdraw(amount)
#         account = BankAccount()
#
# deposit_thread = threading.Thread(target=deposit_task, args=(account, 100))
# withdraw_thread = threading.Thread(target=withdraw_task, args=(account, 150))
#
# deposit_thread.start()
# withdraw_thread.start()
#
# deposit_thread.join()
# withdraw_thread.join()
#
# Вывод в консоль:
# Deposited 100, new balance is 1100
# Deposited 100, new balance is 1200
# Deposited 100, new balance is 1300
# Deposited 100, new balance is 1400
# Deposited 100, new balance is 1500
# Withdrew 150, new balance is 1350
# Withdrew 150, new balance is 1200
# Withdrew 150, new balance is 1050
# Withdrew 150, new balance is 900
# Withdrew 150, new balance is 750
#
#
# Примечание:
# Используйте класс Lock из модуля threading для блокировки доступа к общему ресурсу.
# Ожидается создание двух потоков, один для пополнения счета, другой для снятия денег.
# Используйте with (lock object): в начале каждого метода, чтобы использовать блокировку
#
#
# Файл с кодом прикрепите к домашнему заданию.
# Решение

import threading # модуль

class BankAccount: # класс BankAccount, представляет банковский счет с балансом и методами для пополнения и снятия денег:
    def __init__(self):
        self.balance = 100 #баланс
        self.lock = threading.Lock() # Для предотвращения состояния гонки использ. класс Lock из модуля threading.

    def deposit(self, amount): # сумма депозита
        with self.lock: # оператор with используется для создания контекстного менеджера с помощью объекта блокировки self.lock.
            # Контекстный менеджер гарантирует, что блокировка будет корректно захвачена и освобождена внутри блока кода.
            self.balance += amount # Эта строка увеличивает текущий баланс счета на величину amount.
            # Операция выполняется внутри блокировки, чтобы избежать гонок данных при одновременном доступе из разных потоков.
            print(f"Пополнение {amount}, новый баланс {self.balance}") # Выводится сообщение о пополнении счета на
            # указанную сумму и новом балансе после операции.

    def withdraw(self, amount): # метод withdraw(self, amount) в классе BankAccount отвечает за снятие денег со счета на указанную сумму.
        with self.lock:
            if self.balance >= amount: # достаточно ли средств на счете для выполнения операции снятия указанной суммы.
                self.balance -= amount # Если на счете достаточно средств, то указанная сумма снимается со счета.
                print(f"Снято {amount}, новый баланс {self.balance}")# Выводится сообщение о снятии указанной суммы и новом балансе после операции.
            else:
                print("Не достаточно средста") # Если на счете недостаточно средств для снятия указанной суммы, выводится сообщение о недостатке средств.

def deposit_task(account, amount): # Пополнение счета на указанную сумму.

    for _ in range(5): # Этот цикл выполняет операцию пополнения счета на указанную сумму 5 раз.
        account.deposit(amount) # Вызывается метод deposit объекта account для пополнения счета на указанную сумму.

def withdraw_task(account, amount): # Снятие денег со счета на указанную сумму.
    for _ in range(5): # Этот цикл выполняет операцию снятия денег со счета на указанную сумму 5 раз.
        account.withdraw(amount) # Вызывается метод withdraw объекта account для снятия денег со счета на указанную сумму.

account = BankAccount() # Эта строка создает новый объект (экземпляр) класса BankAccount

deposit_thread = threading.Thread(target=deposit_task, args=(account, 100)) # поток пополнения (target - цель)
withdraw_thread = threading.Thread(target=withdraw_task, args=(account, 150)) # поток снятия

deposit_thread.start() # запуск потока пополнения
withdraw_thread.start() # запуск потока снятия

deposit_thread.join() # метод завершения
withdraw_thread.join() # метод завершения