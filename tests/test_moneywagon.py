import unittest

### tests run from python 3.4+
# do not use pip install moneywagon. this would install original code.
# instead use this repository and do:
# pip install -e .
# pip install socketIO_client

from decimal import Decimal
# use my own moneywagon! Decimal handling!
from moneywagon import AddressBalance, HistoricalTransactions, ALL_SERVICES, Service
from moneywagon.core import CurrencyNotSupported, NoService

class MoneywagonTestCase(unittest.TestCase):
    #addresses with balance (taken from https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html)
    address = '16rCmCmbuWDhPjWTrpQGaU3EPdZF7MTdUk'
    address2 = '16ftSEQ4ctQFDtVZiUBusQUjRrGhM3JYwe'
    addresses = [address, address2]

    def setUp(self):
        #address balance for later tests - uses 1 confirmation
        self.balance = AddressBalance().action('btc', self.address)

    """ TODO: do a useful test for each Service """
    def test_AddressBalance(self):
        # defaults to 1 confirmation
        # from single address
        balance = AddressBalance().action('btc', self.address)
        balance2 = AddressBalance().action('btc', self.address2)
        # from multiple addresses
        balances = AddressBalance().action('btc', addresses=self.addresses)
        self.assertEqual(balance+balance2, balances['total_balance'])

    """ tests HistoricalTransactions for similar results 
        test for similar Balance on 1+ confirmations """
    def test_HistoricalTransactions(self):
        # use a single service, get historical transactions
        # I'm getting decimals, but I get different balance sums and different transactions for each service!
        okLst = []
        asset = 'btc'
        prevTxIdSet = []
        prevTxLst = []
        prevSum = self.balance # start from balance above
        for service in ALL_SERVICES:
            with self.subTest(service=service.__name__):
                try:
                    hTxInstance = HistoricalTransactions(services=[service], verbose=True)
                    txLst = hTxInstance.action(asset, self.address)
                    self.assertFalse(len(txLst) == 0, "Got empty transaction list.")
                    for tx in txLst:
                        # check for Decimal values
                        self.assertTrue(type(tx['amount']) is Decimal)
                        # amount is the same as in previous result?
                        prevTxFiltered = [t for t in prevTxLst if t['txid'] == tx['txid']]
                        if prevTxFiltered:
                            #if we already had this tx, amount must match
                            self.assertEqual(prevTxFiltered[0]['amount'], tx['amount'], "Amounts for tx %s do not match." % (tx['txid'],))
                    prevTxLst = txLst
                    # use only tx with >= 1 confirmations
                    txLst = [tx for tx in txLst if tx['confirmations'] >= 1]
                    # no duplicate txid
                    txIdLst = [tx['txid'] for tx in txLst]
                    self.assertEqual(len(txIdLst), len(set(txIdLst)), "Txid's are not unique.")
                    txIdSet = set(txIdLst)
                    # check data against previous result:
                    # same txid's
                    if prevTxIdSet:
                        self.assertEqual(prevTxIdSet, txIdSet, "Txid's do not match previous txid list.")
                    prevTxIdSet = txIdSet
                    # same amount
                    thisSum = sum([tx['amount'] for tx in txLst])
                    if prevSum is not None:
                        self.assertEqual(prevSum, thisSum, "Transations sum does not match previous sum.")
                    prevSum = thisSum
                    print("%s OK: %s btc, txid's = %s." % (service.name, thisSum, len(txIdLst)))
                    okLst.append(service.__name__)
                except CurrencyNotSupported as ex:
                    self.skipTest("CurrencyNotSupported")
                except NoService as ex:
                    self.skipTest("NoService")
                except NotImplementedError as ex:
                    self.skipTest("NotImplementedError")
                except IOError as ex:
                    self.skipTest("IOError")
                except AssertionError as aEx:
                    print("'" + service.name + "' failed:")
                    print(repr(aEx))
                    raise
        # ok, we mis-use the test here to write a list of tested, usable services, but well ...
        servicesLst = "tested_services_tx_" + asset + " = [" + ", ".join(okLst) + "]"
        with open("../moneywagon/services/tested_services.py", "w") as f:
            f.write("\n".join([
                "from .blockchain_services import *",
                "from .exchange_services import *",
                "",
                servicesLst]))
        print(servicesLst)

if __name__ == '__main__':
    unittest.main()