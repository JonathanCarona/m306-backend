import unittest

from flaskr.services.PaymentStrategy import PaymentContext, TwintPayment, CreditcardPayment

class PaymentStrategyTestCase(unittest.TestCase):
    """This class represents the payment strategy test case"""

    def setUp(self):
        self.context = PaymentContext()

    def test_creditcard_strategy(self):
        self.context.strategy = CreditcardPayment()
        self.assertTrue(self.context.pay_with_method(1000.0))

    def test_anotherPayment_strategy(self):
        self.context.strategy = TwintPayment()
        self.assertFalse(self.context.pay_with_method(1000.0))



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()