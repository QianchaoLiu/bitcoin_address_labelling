import pydgraph
import json
import datetime

class Labeling_Address()
    def __init__(self, dgrpah_server, bitcoin_rawdata_path):
        client_stub = pydgraph.DgraphClientStub('localhost:9080')
        self.client = pydgraph.DgraphClient(client_stub)
        self.bitcoin_rawdata_path = bitcoin_rawdata_path
        self.startclock = datetime.datetime.now()
        
    def clear_all_data(self):
        op = pydgraph.Operation(drop_all=True)
        self.client.alter(op)
        
    def create_schema(self):
        schema = '''address: string @index(hash, term) .
                    '''
        op = pydgraph.Operation(schema=schema)
        self.client.alter(op)

    def insert_data_json(self, data):
        txn = self.client.txn()
        try:
            assigned = txn.mutate(set_obj=data)
            txn.commit()
        finally:
            txn.discard()

    def insert_data_origin(self, data):
        txn = self.client.txn()
        try:
            assigned = txn.mutate(set_nquads=data)
            txn.commit()
        finally:
            txn.discard()

    def query_existence(self, address):
        query = """query all($a: string) {
          all(func: eq(address, $a))
          {
            uid
          }
        }"""
        variables = {'$a': address}
        res = self.client.txn().query(query, variables=variables)
        all_addresses = json.loads(res.json.decode('utf-8'))['all']
        if len(all_addresses)>0:
            return all_addresses[0]['uid']
        else:
            return None
        
    def csv_generator(self, path):
        with open(path) as f:
            for line in f:
                yield line

    def update_graph(self, data):
        for item in data:
            inputs = item[0]
            outputs = item[1]
            for input_addr in inputs:
                if input_addr!='null':
                    transfer = []
                    for out_address in outputs:
                        output_exist = self.query_existence(out_address)
                        if output_exist:
                            transfer.append({"uid":output_exist, 'address': out_address})
                        else:
                            transfer.append({'address': out_address})
                    exist = self.query_existence(input_addr)
                    if exist:
                        dat = {"uid": exist, 'address':input_addr, 'transfer':transfer}
                    else:
                        dat = {'address':input_addr, 'transfer':transfer}
                    self.insert_data_json(dat)

    def timer(self, block_num):
        now = datetime.datetime.now()
        print(block_num, 'used time:',(now-self.startclock).seconds/60., 'min')
        
    def insert_graph(self, target_block=10):
        tx_header = self.bitcoin_rawdata_path+'tx_header.csv'
        tx_input = self.bitcoin_rawdata_path+'tx_input.csv'
        tx_output = self.bitcoin_rawdata_path+'tx_output.csv'

        header_generator = self.csv_generator(tx_header)
        input_generator = self.csv_generator(tx_input)
        output_generator = self.csv_generator(tx_output)
        input_row = next(input_generator)
        input_hash = ','.join(input_row.split(',')[:2])
        output_row = next(output_generator)
        output_hash = ','.join(output_row.split(',')[:2])

        info = list()
        block_num = int(input_row.split(',')[0])

        start_clock = datetime.datetime.now()
        while(block_num < target_block):
            tx_row = next(header_generator)
            new_block_num = int(tx_row.split(',')[0])
            if new_block_num!=block_num:
                self.timer(block_num)
                block_num+=1
                self.update_graph(info)
                info = list()
            tx_hash = ','.join(tx_row.split(',')[:2])
            
            inputs = []
            while(input_hash == tx_hash):
                inputs.append(input_row.split(',')[-1][:-1])
                input_row = next(input_generator)
                input_hash = ','.join(input_row.split(',')[:2])

            outputs = []
            while(output_hash == tx_hash):
                address = output_row.split(',')[5]
                if address != 'None':
                    outputs.append(address)
                output_row = next(output_generator)
                output_hash = ','.join(output_row.split(',')[:2])
            info.append([inputs, outputs])

    def start_parse(self):
        self.create_schema()
        self.insert_graph()