from collections import UserList


class AmountPaymentList(UserList):
    def amount_payment(self):
        
        sum = 0
        for value in self:
            if value > 0:
                sum = sum + value
        return sum   
                

payment_list = [1, -3, 4]    
payment = AmountPaymentList(payment_list)
payment.amount_payment()
print(payment.amount_payment())