from web3 import HTTPProvider, Web3
from time import time
from os import path

class ConnectionRPC(Web3):
    def __init__(self, rpcurl=None):
        super(ConnectionRPC, self).__init__(HTTPProvider(rpcurl))
        self.eth.account.enable_unaudited_hdwallet_features()
        self._private_keys = None
        self._address_wallet = None
        
    def Login(self, mnemonic):
        if(len(mnemonic.split(" ")) > 1):
            info = self.eth.account.from_mnemonic(mnemonic)
        else:
            info = self.eth.account.from_key(mnemonic)
        self._private_keys = info.privateKey.hex()
        self._address_wallet = info.address
        
    def getBalance(self):
        #untuk mudah dibaca manusia
        return self.fromWei(self.eth.getBalance(self.getAddressWallet()), 'ether')
        
    def getPrivateKeys(self):
        return self._private_keys
        
    def getAddressWallet(self):
        return self._address_wallet

class SwapToken(ConnectionRPC):
    def __init__(self, rpcurl):
        super(SwapToken, self).__init__(rpcurl)
        self.contractForBuy = None
        self.contractPair = None
        self.ContractRouterAddress = None
        self.ContractAbi = None
        self.gasGwei = None
        self.gas = 57819
        self.outAmoun = None
        self.inAmoun = None
        
    def setContractPair(self, ContractPair=None):
        self.contractPair = ContractPair
        
    def setContractForBuy(self, ContractForBuy=None):
        self.contractForBuy = ContractForBuy
        
    def getContractPair(self):
        return self.contractPair
        
    def setRouterContract(self, ContractRouter=None, ContractAbi=None):
        self.ContractRouterAddress = ContractRouter
        self.ContractAbi = ContractAbi
        
    def getContractAbi(self):
        return self.ContractAbi
        
    def getContractRouter(self):
        return self.ContractRouterAddress
 
    def setGasGwei(self, gwei=10):
        self.gasGwei = self.toWei(str(gwei), "gwei")
        
    def setOutAmount(self, OutAmoun=None):
        self.outAmoun = self.toWei(str(OutAmoun), 'ether')
        
    def setInAmoun(self, InAmoun):
        self.inAmoun = InAmoun
        
    def setGasLimit(self, gasLimmit=57819):
        self.gas = gasLimmit
        
    def ApprovSwap(self):
        contract_router = self.eth.contract(
                address=self.getContractRouter(),
                abi=self.getContractAbi()
        )
        Sum = lambda x: self.toChecksumAddress(x)
        tx_settings = contract_router.functions.swapExactETHForTokens(
        self.inAmoun, #InAmount
        [Sum(self.contractPair), Sum(self.contractForBuy)],
        self._address_wallet, (int(time()) + 10000)).buildTransaction(
        {
            'from': self._address_wallet,
            'value': self.outAmoun , #forBuy outAmoun
            'gas': self.gas,
            'gasPrice': self.gasGwei,
            'nonce': self.eth.getTransactionCount(self._address_wallet),
        })
        transaksi = self.eth.sendRawTransaction(
            self.eth.account.signTransaction(
            tx_settings, self._private_keys
                ).rawTransaction
            )
        return self.toHex(transaksi)


def real_path(file_name=r"/Market/Abi/pancakeswapV2.txt"):
    with open(path.dirname(path.abspath(__file__)) + file_name) as openfile:
        return openfile.readline()
    

