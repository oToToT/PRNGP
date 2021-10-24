# PRNGP

The default (or widely used) PRNG implemented by most popular languages is not cryptographically secure. Here is some collections of some predictors. Feel free to send PR if you have some predictors not in this repo.

## LCG (Java)

[@giuliocandre/java-prng-predict](https://github.com/giuliocandre/java-prng-predict)

**NOTICE**: I didn't check this repo yet

## mt19937 (C++, Python, PHP)

If we have 624 output of mt19937, we could recover the whole state of mt19937.  
Also, if we have 0, 1, 397 -th output of mt19937, we could predict the 624-th output of mt19937.  
For PHP, if we have 0, 397 -th output of mt19937, we could recover the whole state of mt19937. See [this post](https://www.ambionics.io/blog/php-mt-rand-prediction).

A predictor could be found in `mt19937_64/predictor.py`

## mt19937_64 (C++)

Just like mt19937, but we only need 312 output of mt19937_64 to recover the whole state of mt19937_64.  
Also, if we have 0, 1, 156 -th output of mt19937_64, we could predict the 312-th output of mt19937_64.

A predictor could be found in `mt19937_64/predictor.py`

## XorShift128+ (JavaScript in Chrome, Firefox, Node.js or any other V8 based platform)

Check [@TACIXAT/XorShift128Plus](https://github.com/TACIXAT/XorShift128Plus/blob/master/xs128p.py) for detail.

## Misc

LCGs are not secure at all: https://tailcall.net/blog/cracking-randomness-lcgs/
