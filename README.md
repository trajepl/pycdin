# BlockChain Simulation

``BlockChain`` ``Django``

we use python socket and Django to implement ``BlockChain Simulation``.

## component
### blockchain/
  This component is made up of ``block.py`` and ``chain.py`` which have a ``Block`` and ``Chain`` classes. These two classes implement the layer of blockchain in which we can read blocks from the corresponding file and some other functions. In order to search blocks quickly, we build the ``index.id`` file to record the offset of each block in the file. 

| data |bytes length|
|:---|:---|
|  magic network id | 8 |
|  timestamp |  8  |
|  previous block hash |  64  |
|  merkle root |  64  |
|  rand number |  4  |
|  data length |  4  |
|  sum |  148  |
|  data |  data length  |

*Note that: In this component, we use the ``Merkle Tree`` to hash the transactions of list. The details about the Mekle Tree you can see [wiki-merkle-tree](https://en.wikipedia.org/wiki/Merkle_tree)*

### chat/ | module-inject/ | module/
Those modules contains some little programs to implement and test the ``module-inject`` among many computers by socket of python module. We also implement the simple ``ChatRoom`` program.

### venv/
In this component, we use the [nginx + uwsgi + python3 + django + virtualenv](http://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html) to build the browser-server by which we could operate the blockchains and implement the ``DATA STORAGE``, ``DATA DISTRIBUTION``, ``CONSENSUS MECHANISM``, ``DEFENCE``, ``WRITE ACCESS`` and so on. *Now, we have not completed those function.*
**0.0**
  
Here is one example to explain the struct of blockchain:
*Note that: there are some duplicate blocks we add into blockchain on purpose.*
```
Magic id            : 0xdab5bffa
timestamp           : Tue Mar 21 12:42:33 2017
previous hash       : 0000000000000000000000000000000000000000000000000000000000000000
merkle_root         : ba74546219a1f6189a511ac313bb109b5b9fe40c9bc669e87621ee7f3c198166
data length         : 26
rand number         : 26
trade               : trajep create first block.
--------------------------------------------------------------------------------------
Magic id            : 0xdab5bffa
timestamp           : Tue Mar 21 12:42:45 2017
previous hash       : ba74546219a1f6189a511ac313bb109b5b9fe40c9bc669e87621ee7f3c198166
merkle_root         : bdf0dc64671b6084b973f4a9e1f5d88da63b28b514604a4029b878d3d8890f1a
data length         : 73
rand number         : 99991
trade               : trajep3 create first block.
                    : trajep create 2rd block.
                    : trajep create 3th bloc
--------------------------------------------------------------------------------------
Magic id            : 0xdab5bffa
timestamp           : Tue Mar 21 12:43:02 2017
previous hash       : bdf0dc64671b6084b973f4a9e1f5d88da63b28b514604a4029b878d3d8890f1a
merkle_root         : 14b7e8ac1e30486a84dc04b590c20535bafe190422d6b9376967f4bde93692ce
data length         : 73
rand number         : 0
trade               : trajep1 create first block.
                    : trajep create 2rd block.
                    : trajep create 3th bloc
--------------------------------------------------------------------------------------
Magic id            : 0xdab5bffa
timestamp           : Tue Mar 21 12:55:44 2017
previous hash       : 14b7e8ac1e30486a84dc04b590c20535bafe190422d6b9376967f4bde93692ce
merkle_root         : 14b7e8ac1e30486a84dc04b590c20535bafe190422d6b9376967f4bde93692ce
data length         : 73
rand number         : -243436
trade               : trajep1 create first block.
                    : trajep create 2rd block.
                    : trajep create 3th bloc
--------------------------------------------------------------------------------------
[(0, 0), (1, 174), (2, 397), (3, 620), (4, 843)]

```
