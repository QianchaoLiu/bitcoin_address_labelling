# bitcoin address labelling

Work Flow:

- insert bitcoin data into dgraph

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
