# pycdin (python code injection)
tags: BlockChain Django

we use python injection to implement ``BlockChain``.

## component
### blockchain/
  This component is made up of ``block.py`` and ``chain.py`` which have a ``Block`` and ``Chain`` classes. These two classes implement the layer of blockchain in which we can read blocks from the corresponding file and some other functions. In order to search blocks quickly, we build the ``index.id`` file to record the offset of each block in the file. 

    data struct
| data |bytes length|
|:---|:---|
|  magic network id | 8 |
|  timestamp |  8  |
|  previous block hash |  64  |
|  block hash |  64  |
|  data length |  4  |
|  timestamp |  data length  |
|  sum |  148  |

### chat/ | module-inject/ | module/
Those modules contains some little programs to implement and test the ``module-inject`` among many computers by socket of python module. We also implement the simple ``ChatRoom`` program.

### venv/
In this component, we use the [nginx + uwsgi + python3 + django + virtualenv](http://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html) to build the browser-server by which we could operate the blockchains and implement the ``DATA STORAGE``, ``DATA DISTRIBUTION``, ``CONSENSUS MECHANISM``, ``DEFENCE``, ``WRITE ACCESS`` and so on. *Now, we have not complete those function.*
**0.0**
  
      Here is one example to explain the struct of blockchain:
*Note that: there are some duplicate blocks we add into blockchain on purpose.*
```
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:23 2017
    previous hash       : 0000000000000000000000000000000000000000000000000000000000000000
    hash_value          : ba74546219a1f6189a511ac313bb109b5b9fe40c9bc669e87621ee7f3c198166
    data length         : 26
    data                : trajep create first block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:29 2017
    previous hash       : ba74546219a1f6189a511ac313bb109b5b9fe40c9bc669e87621ee7f3c198166
    hash_value          : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    data length         : 22
    data                : trajep create 7 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:30 2017
    previous hash       : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    hash_value          : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    data length         : 22
    data                : trajep create 7 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:31 2017
    previous hash       : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    hash_value          : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    data length         : 22
    data                : trajep create 7 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:32 2017
    previous hash       : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    hash_value          : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    data length         : 22
    data                : trajep create 7 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:33 2017
    previous hash       : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    hash_value          : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    data length         : 22
    data                : trajep create 7 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:34 2017
    previous hash       : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    hash_value          : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    data length         : 22
    data                : trajep create 7 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:35 2017
    previous hash       : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    hash_value          : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    data length         : 22
    data                : trajep create 7 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:36 2017
    previous hash       : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    hash_value          : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    data length         : 22
    data                : trajep create 7 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:36 2017
    previous hash       : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    hash_value          : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    data length         : 22
    data                : trajep create 7 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:12:53 2017
    previous hash       : 5e5fb8b696f870502d498ef1f21ddb5d97a2377898e71fb594b01200d457417d
    hash_value          : 5ebfa46d73112ce1539f359a4cb66435ec3d6878ce75181c5db7c887da12df21
    data length         : 22
    data                : trajep create 8 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:13:11 2017
    previous hash       : 5ebfa46d73112ce1539f359a4cb66435ec3d6878ce75181c5db7c887da12df21
    hash_value          : cd12d78723093e6cdf574ce04c8a354a33988d4c39d7b961e945aecfa3a96c45
    data length         : 22
    data                : trajep create 9 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:13:18 2017
    previous hash       : cd12d78723093e6cdf574ce04c8a354a33988d4c39d7b961e945aecfa3a96c45
    hash_value          : ffe38405924d1eedea63dad9ebade73e7cdbd522c4415d077b134ca8c989a1c0
    data length         : 23
    data                : trajep create 10 block.
    --------------------------------------------------------------------------------------
    Magic id            : 0xdab5bffa
    timestamp           : Wed Mar  1 10:24:05 2017
    previous hash       : ffe38405924d1eedea63dad9ebade73e7cdbd522c4415d077b134ca8c989a1c0
    hash_value          : ffe38405924d1eedea63dad9ebade73e7cdbd522c4415d077b134ca8c989a1c0
    data length         : 23
    data                : trajep create 10 block.
    --------------------------------------------------------------------------------------
    [(0, 0), (1, 174), (2, 344), (3, 514), (4, 684), (5, 854), (6, 1024), (7, 1194), (8, 1364), (9, 1534), (10, 1704), (11, 1874), (12, 2044), (13, 2215), (14, 2386)]
```
