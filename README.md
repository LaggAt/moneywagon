# moneywagon


Moneywagon is a an implementation of a Blockchain Kernel. It is a tool that can be used
to built lightweight cryptocurrency wallets. Blockchain Kernels provide an
alternative to the outdated "SPV" method of building lightweight cryptocurrency
services.


## Main developer

The scripts are developed [over here, see priestc's repository.](https://github.com/priestc/moneywagon)
His donation btc address is:

1HWpyFJ7N6rvFkq3ZCMiFnqM6hviNFmG5X

## This fork

I decided to do my changes in an own fork, and maybe do a pull request later. These are the goals I want to reach here:

* Use Decimal instead of float. 
This is a breaking change, as applications using float's usually couldn't work with Decimals without code change. BUT: Decimals are always exact, floats aren't. Therefore for currencies Decimal should be used. https://en.wikipedia.org/wiki/Floating-point_arithmetic#Accuracy_problems

* Test and document functions. For now: AddressBalance and HistoricalTransactions.
Currently I get different results from different services. I'm currently fixing this. See /tests directory.

## Donate

Help me reaching my goals:

![Imgur](https://i.imgur.com/4RgMA5nm.png)

17Xz11thcE16siwqSGSS9ANhVrqvfT2fWH
