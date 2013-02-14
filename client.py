import threading, Queue
import rpyc

class callBack(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.inq = Queue.Queue()
        self.nextValidId = None
        self.active = True
        self.daemon = True
        self.contractDetails = {}
        self.contractDetailsEnd = []
        self.historicalData = {}
        self.historicalDataEnd = []
        self.start()
        
    def callBack(self, msg, mapping):
        self.inq.put((msg, mapping))

    def run(self):
        while self.active:
            try:
                msg, mapping = self.inq.get(block = True, timeout = .5)
                #print 'callback run',msg,mapping
                if msg == 'nextValidId':
                    self.nextValidId = mapping['orderId']
                elif msg == 'tickPrice':
                    logging.info('tickPrice id:%d %d %.2f %s', mapping['tickerId'],mapping['field'],mapping['price'],mapping['canAutoExecute'])
                elif msg == 'tickSize':
                    logging.info('tickSize id:%d %d %d', mapping['tickerId'],mapping['field'],mapping['size'])
                elif msg == 'tickGeneric':
                    logging.info('tickGeneric id:%d %d %f', mapping['tickerId'],mapping['tickType'],mapping['value'])
                elif msg == 'contractDetails':
                    self.contractDetails.setdefault(mapping['reqId'], []).append(mapping['contractDetails'])
                    contractDetailDecode(mapping['contractDetails'])
                elif msg == 'contractDetailsEnd':
                    self.contractDetailsEnd.append(mapping['reqId'])
                    print 'contractDetailsEnd',mapping['reqId']
                elif msg == 'historicalData':
                    print msg,mapping
                    '''
                    if mapping[] == '':
                        self.historicalDataEnd.append(mapping['reqId'])
                    else:
                        self.historicalData.setdefault(mapping['reqId'], []).append(mapping)
                    '''
                elif msg == 'error':
                    print 'CRITICAL',msg, mapping
                else:
                    print 'unknown',msg, mapping
                self.inq.task_done()
            except Queue.Empty:
                pass

    def stop(self):
        self.active = False
        self.join()        

    def nextId(self):
        id1 = self.nextValidId
        self.nextValidId += 1
        return id1

def myContractFactory(client, symbol, exchange):
    contract = client.modules.com.ib.client.Contract()
    contract.m_symbol = symbol
    contract.m_secType = 'STK'
    contract.m_exchange = 'SMART'
    contract.m_currency = 'USD'
    contract.m_primaryExch = exchange
    return contract

def myContractFactory2(client, symbol, ex, typ):
    contract = client.modules.com.ib.client.Contract()
    contract.m_symbol = symbol
    contract.m_exchange = ex
    contract.m_secType = typ
    contract.m_includeExpired = True
    return contract

def myContractFactory3(client, exp, conId):
    contract = client.modules.com.ib.client.Contract()
    contract.m_expiry = exp
    contract.m_conId = conId
    return contract

def main():
    contracts = [('YM','ECBOT', 'FUT'),]
    
    c = rpyc.classic.connect('localhost')
    bgsrv = rpyc.BgServingThread(c)
    cb = callBack()
    remoteWrapper = c.modules.rIbServer.ReferenceWrapper(cb.callBack)
    csocket = c.modules.com.ib.client.EClientSocket(remoteWrapper)
    host = 'localhost'
    port = 4001
    clientId = 2
    print 'Trying to connect...Host:%s Port:%s, ClientId:%s' % (host, port, clientId)
    csocket.eConnect(host, port, clientId)
    t1 = time.time()
    while time.time()-10 < t1 and not csocket.isConnected():
        time.sleep(0.2)
        print 'Wait for connection'
    while cb.nextValidId is None:
        time.sleep(0.2)
        print 'Wait for nextValidId'
    try:
        '''
        for stock,ex in (('GOOG', 'NASDAQ'), ('YHOO', 'NASDAQ'), ('FMCN','NASDAQ'),
                ('STX','NASDAQ'),('MPWR','NASDAQ'),('CYNO','NASDAQ'),('NXY','NYSE')):
            contract1 = myContractFactory(c, stock, ex)
            id1 = csocket.reqMktData(cb.nextId(), contract1, '', False)
            #tickers[id1] = [ stock, ex, contract1, None ]
        '''
        cs = myContractFactory2(c, 'YM', 'ECBOT', 'FUT')
        rid = cb.nextId()
        csocket.reqContractDetails(rid, cs)
        while rid not in cb.contractDetailsEnd:
            time.sleep(.2)
            print 'wait for',rid
        for cd in cb.contractDetails[rid]:
            contractDetailDecode(cd)


        cs = myContractFactory3(c, '201212', 98714808)
        csocket.reqContractDetails(cb.nextId(), cs)

        time.sleep(5)
    except:
        traceback.print_exc()

    csocket.eDisconnect()
    cb.stop()
    bgsrv.stop()
    c.close()
    
    
if __name__ == '__main__':
    main()

#EOF
