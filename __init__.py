#!/usr/bin/env jython
import sys
import time
try:
    import java
except (ImportError,):
    print 'Run this script with jython, not python.'
    sys.exit(1)
try:
    import com.ib
except (ImportError,):
    print 'Could not import com.ib.  Try adding jtsclient.jar to CLASSPATH.'
    sys.exit(2)
import com.ib.client

class ReferenceWrapper(com.ib.client.EWrapper):
    def __init__(self, callBack):
        super(ReferenceWrapper, self).__init__()
        self.remoteCallBack = callBack

    def callBack(self, msg, mapping):
        try:
            del(mapping['self'])
        except (KeyError,):
            pass
        self.remoteCallBack(msg, mapping)
    
    #Definitions from EWrapper
    def tickPrice(self, tickerId, field, price, canAutoExecute):
        self.callBack('tickPrice', vars())
    def tickSize(self, tickerId, field, size):
        self.callBack('tickSize', vars())
    def tickOptionComputation(self, tickerId, field, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        self.callBack('tickOptionComputation', vars())
    def tickGeneric(self, tickerId, tickType, value):
        self.callBack('tickGeneric', vars())
    def tick(self, tickerId, tickType,  value):
        self.callBack('tick', vars())
    def tickEFP(self, tickerId,  tickType, basisPos, formattedBasisPos, impliedFuture, holdDays, futureExpiry, dividendImpact, dividendsToExpiry):
        self.callBack('tickEFP', vars())
    def orderStatus(self, orderId,  status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld):
        self.callBack('orderStatus', vars())
    def openOrder(self, orderId, contract, order, orderState):
        self.callBack('openOrder', vars())
    def openOrderEnd(self):
        self.callBack('openOrderEnd', vars())
    def updateAccountValue(self, key,  value, currency, accountName):
        self.callBack('updateAccountValue', vars())
    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        self.callBack('updatePortfolio', vars())
    def updateAccountTime(self, timeStamp):
        self.callBack('updateAccountTime', vars())
    def accountDownloadEnd(self, accountName):
        self.callBack('accountDownloadEnd', vars())
    def nextValidId(self, orderId):
        self.callBack('nextValidId', vars())
    def contractDetails(self, reqId, contractDetails):
        self.callBack('contractDetails', vars())
    def bondContractDetails(self, reqId, contractDetails):
        self.callBack('bondContractDetails', vars())
    def contractDetailsEnd(self, reqId):
        self.callBack('contractDetailsEnd', vars())
    def execDetails(self, reqId, contract, execution):
        self.callBack('execDetails', vars())
    def execDetailsEnd(self, reqId):
        self.callBack('execDetailsEnd', vars())
    def updateMktDepth(self, tickerId, position, operation, side, price,  size):
        self.callBack('updateMktDepth', vars())
    def updateMktDepthL2(self, tickerId, position, marketMaker, operation, side, price, size):
        self.callBack('updateMktDepthL2', vars())
    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        self.callBack('updateNewsBulletin', vars())
    def managedAccounts(self, accountsList):
        self.callBack('managedAccounts', vars())
    def receiveFA(self, faDataType, xml):
        self.callBack('receiveFA', vars())
    def historicalData(self, reqId,  date,  open,  high,  low, close, volume, count,  WAP, hasGaps):
        self.callBack('historicalData', vars())
    def scannerParameters(self, xml):
        self.callBack('scannerParameters', vars())
    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        self.callBack('scannerData', vars())
    def scannerDataEnd(self, reqId):
        self.callBack('scannerDataEnd', vars())
    def realtimeBar(self, reqId,  time, open, high, low, close, volume, wap, count):
        self.callBack('realtimeBar', vars())
    def currentTime(self, time):
        self.callBack('currentTime', vars())
    def fundamentalData(self, reqId,  data):
        self.callBack('fundamentalData', vars())
    def deltaNeutralValidation(self, reqId, underComp):
        self.callBack('deltaNeutralValidation', vars())
    def tickSnapshotEnd(self, reqId):
        self.callBack('tickSnapshotEnd', vars())
    def marketDataType(self, reqId, marketDataType):
        self.callBack('marketDataType', vars())
    #Definitions from AnyWrapper
    def error(self, *ar, **args):
        self.callBack('error', vars())
    def connectionClosed(self):
        self.callBack('connectionClosed', vars())

#EOF
