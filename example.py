from mylibs.Settings import  SwapToken, real_path

wbnbcontract = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
PancakeRouterContractV2 = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
token = "0x372e99c935c58dec5d894f9c0cb5c63f2e7ab49e"
RouterAbi = real_path()

mnemonic = "" #Mnemonic or PrivateKeys

test_net = "https://data-seed-prebsc-1-s1.binance.org:8545"
sites = "https://testnet.bscscan.com/tx/"

SwapToken = SwapToken(test_net)
SwapToken.Login(mnemonic)
print("Address Wallet: ", SwapToken.getAddressWallet())
print("wbnb Token: ", SwapToken.getBalance())
print('Private Keys: ', SwapToken.getPrivateKeys())

SwapToken.setContractForBuy(token)
SwapToken.setContractPair(wbnbcontract)
SwapToken.setGasGwei(10)
SwapToken.setInAmoun(10000)
SwapToken.setOutAmount(0.0001)

SwapToken.setRouterContract(PancakeRouterContractV2, ContractAbi=RouterAbi)
print(sites+SwapToken.ApprovSwap())