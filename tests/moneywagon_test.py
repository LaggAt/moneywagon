from decimal import Decimal
# use my own moneywagon! Decimal handling!
from moneywagon import AddressBalance, HistoricalTransactions, ALL_SERVICES, Service
from moneywagon.core import CurrencyNotSupported, NoService

#addresses with balance (taken from https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html)
address = '16rCmCmbuWDhPjWTrpQGaU3EPdZF7MTdUk'
address2 = '16ftSEQ4ctQFDtVZiUBusQUjRrGhM3JYwe'
addresses = [address, address2]


# get balance - not really tested now
# from single address
balance = AddressBalance().action('btc', address)
print balance
# from multiple addresses
balances = AddressBalance().action('btc', addresses=addresses)
print repr(balances)


# use a single service, get historical transactions
# I'm getting decimals, but I get different balance sums and different transactions for each service!
prevTxIdSet = []
prevSum = balance # start from balance above
for service in ALL_SERVICES:
    try:
        #txLst = HistoricalTransactions(services=[service], verbose=True).action('btc', address )
        txLst = HistoricalTransactions(services=[service]).action('btc', address)
        for tx in txLst:
            assert type(tx['amount']) is Decimal
        # no duplicate txid
        txIdLst = [tx['txid'] for tx in txLst]
        assert len(txIdLst) == len(set(txIdLst)), "Txid's on %s are not unique: %r" % (service.name, txIdLst)
        txIdSet = set(txIdLst)
        # check data against previous result:
        # same txid's
        if prevTxIdSet:
            assert prevTxIdSet == txIdSet, "Txid's on %s do not match previous txid list: %r" % (service.name,
                     prevTxIdSet.symmetric_difference(txIdSet))
        prevTxIdSet = txIdSet
        # same amount
        thisSum = sum([tx['amount'] for tx in txLst])
        if prevSum is not None:
            assert prevSum == thisSum, "Transations sum on %s does not match previous sum. %r" % (service.name, thisSum)
        prevSum = thisSum
        print "%s: %s btc, txid's = %s." % (service.name, thisSum, len(txIdLst))
    except CurrencyNotSupported as ex:
        pass
    except NoService as ex:
        pass
    except NotImplementedError as ex:
        pass
    except IOError as ex:
        pass
    except Exception as ex:
        print "INVESTIGATE: %s throws %s (%s)" % (service.name, type(ex).__name__, ex.message)
        raise ex
