import unittest
from mock import MagicMock
from cashback.services.purchase import PurchaseService
from cashback.data.data_access import ResellerData, PurchaseData, CashBackData

class PurchaseServiceTest(unittest.TestCase) :
    
  def test_when_add_preapproved_purchase_then_approved(self):
    #Given
    purchase = {"cpf":"15350946056", "amount":700.01, "code":999, "date":"2021-06-08"}
    #mocking data layer
    ResellerData.find_reseller = MagicMock(return_value={"cpf":"15350946056"})
    PurchaseData.add_purchase = MagicMock(return_value=purchase)
    #when
    result = PurchaseService().add_purchase(purchase)
    #then
    self.assertIn('status', result.keys())
    self.assertEqual('Approved', result['status'])

  def test_when_add_regular_purchase_then_validating(self):
    #Given
    purchase = {"cpf":"05138891987", "amount":1000.05, "code":111, "date":"2021-06-08"}
    #mocking data layer
    ResellerData.find_reseller = MagicMock(return_value={"cpf":"05138891987"})
    PurchaseData.add_purchase = MagicMock(return_value=purchase)
    #when
    result = PurchaseService().add_purchase(purchase)
    #then
    self.assertIn('status', result.keys())
    self.assertEqual('Validating', result['status'])
    
  def test_when_add_invalid_purchase_then_error(self):
    #Given
    purchase = {"cpf":"05138891987", "amount":1000.05, "code":111, "date":"2021-06-08"}
    #mocking data layer
    ResellerData.find_reseller = MagicMock(return_value={})
    PurchaseData.add_purchase = MagicMock(return_value=purchase)
    #when
    result = PurchaseService().add_purchase(purchase)
    #then
    self.assertIn('error', result.keys())   

  def test_when_amount_purchases_lt_1000_then_apply_10_percent(self):
    #Given
    #mocking data layer
    PurchaseData.find_monthly_purchases = MagicMock(return_value=[{"amount": 500.01}])
    #when
    purchases = PurchaseService().list_current_month_purchases('05138897965')
    #then
    for p in purchases:
      self.assertIn('cash_back', p.keys())
      self.assertEqual(p['amount'] * 0.1, p['cash_back'])

  def test_when_amount_purchases_eq_1000_then_apply_10_percent(self):
    #Given
    #mocking data layer
    PurchaseData.find_monthly_purchases = MagicMock(return_value=[{"amount": 500.01}, {"amount": 499.99}])
    #when
    purchases = PurchaseService().list_current_month_purchases('05138897965')
    #then
    for p in purchases:
      self.assertIn('cash_back', p.keys())
      self.assertEqual(p['amount'] * 0.1, p['cash_back'])

  def test_when_amount_purchases_lt_1500_then_apply_15_percent(self):
    #Given
    #mocking data layer
    PurchaseData.find_monthly_purchases = MagicMock(return_value=[{"amount": 500.01}, {"amount": 499.99}, {"amount": 1.99}])
    #when
    purchases = PurchaseService().list_current_month_purchases('05138897965')
    #then
    for p in purchases:
      self.assertIn('cash_back', p.keys())
      self.assertEqual(p['amount'] * 0.15, p['cash_back'])

  def test_when_amount_purchases_eq_1500_then_apply_15_percent(self):
    #Given
    #mocking data layer
    PurchaseData.find_monthly_purchases = MagicMock(return_value=[{"amount": 500.01}, {"amount": 499.99}, {"amount": 499.99}])
    #when
    purchases = PurchaseService().list_current_month_purchases('05138897965')
    #then
    for p in purchases:
      self.assertIn('cash_back', p.keys())
      self.assertEqual(p['amount'] * 0.15, p['cash_back'])

  def test_when_amount_purchases_gt_1500_then_apply_20_percent(self):
    #Given
    #mocking data layer
    PurchaseData.find_monthly_purchases = MagicMock(return_value=[{"amount": 500.01}, {"amount": 499.99}, {"amount": 500.01}])
    #when
    purchases = PurchaseService().list_current_month_purchases('05138897965')
    #then
    for p in purchases:
      self.assertIn('cash_back', p.keys())
      self.assertEqual(p['amount'] * 0.2, p['cash_back'])

  def test_when_no_purchases_then_empty_list(self):
    #Given
    #mocking data layer
    PurchaseData.find_monthly_purchases = MagicMock(return_value=[])
    #when
    purchases = PurchaseService().list_current_month_purchases('05138897965')
    #then
    self.assertEqual([], purchases)

  def test_when_get_cash_back_amount_then_return_credit(self):
    #Given
    cpf = {"cpf":"15350946051"}
    #mocking data layer
    CashBackData.get_cashback_amount = MagicMock(return_value={"credit": 1692})
    #when
    result = PurchaseService().get_cashback_amount(cpf)
    #then
    self.assertIn('credit', result.keys())