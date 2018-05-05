# bitcoin address labelling

Work Flow:

### insert bitcoin data into dgraph

[Dgraph](https://docs.dgraph.io/) is a distributed based graph database. At first, we load bitcoin transaction data into dgraph. Code is available at `create_dgraph_network.py`

You can use `GraphQL+-`, a graph query language based on Facebook’s GraphQL, to do visualization of addresses' relationship. Code attached below is a simple demo to search related addresses in the nearest 4 layers.  

```mysql
{
  everyone(func: eq(address, "13uHBf49DjimMpEkaSEshpcKipFDmem2Cr")) {
    uid
    address
    transfer{ 
      uid
      address 
      transfer {
        address 
        transfer (first: 50){
          address
        }
      }
    	
    }
  }
}

```

The visualization result is:

![](https://github.com/QianchaoLiu/bitcoin_address_labelling/blob/master/static/visualization.png)

### search address relationship in the graph database

Using raw data that already labelled the ownership of public bitcoin address, given any bitcoin address, we can see which addresses have relationship with target address.

Demo of research result is enclosed for bitcoin address `16bk4PdZfN2aMK4RvCTEipfUXjuevzGdVG`

```json
layer 1 :
No related infomation
layer 2 :
address type is Exchange and belongs to  Poloniex.com
address type is Exchange and belongs to  Bitstamp.net
layer 3 :
address type is Services and belongs to  HaoBTC.com
address type is Exchange and belongs to  Bittrex.com
address type is Services and belongs to  Cubits.com
address type is Pool and belongs to  SlushPool.com
address type is Exchange and belongs to  Bitcoin.de
address type is Exchange and belongs to  Bitstamp.net
address type is Exchange and belongs to  Poloniex.com
address type is Exchange and belongs to  CoinMotion.com

``` 