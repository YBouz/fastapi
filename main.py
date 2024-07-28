from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import MT5Manager

app = FastAPI()
manager = MT5Manager.ManagerAPI()

class Symbol:
    def __init__(self, symbol, description, contract_size, swap_long, swap_short):
        self.symbol = symbol
        self.description = description
        self.contract_size = contract_size
        self.swap_long = swap_long
        self.swap_short = swap_short

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}


@app.get("/api/managers")
async def get_managers():
    return_dict = {}
    if manager.Connect("23.106.62.88:443", 1401, "WebMaster@24", 
                    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_USERS, 120000):
        print("Connected to server")
        # get the list of managers on the server
        managers = manager.UserGetByGroup("managers\\*")
        # check the obtained list
        if managers is not False:
            print(f"There are {len(managers)} managers on server")
        else:
            # failed to get the list
            print(f"Failed to get manager list: {MT5Manager.LastError()}")
        # disconnect from the server
        manager.Disconnect()
        
        return {"# of managers": len(managers)}
    else:
        # failed to connect to the server
        print(f"Failed to connect to server: {MT5Manager.LastError()}")

@app.get("/api/symbols")
async def get_symbols():
    return_dict = {}
    if manager.Connect("23.106.62.88:443", 1401, "WebMaster@24", 
                    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_SYMBOLS, 120000):
        print("Connected to server")
        symbols = manager.SymbolRequestArray("Crypto*", None)

        # check the obtained list
        if symbols is not False:
            print(f"There are {len(symbols)} symbols on server")
        else:
            # failed to get the list
            print(f"Failed to get symbol list: {MT5Manager.LastError()}")
        # disconnect from the server

        # for obj in symbols:
        #     key_value_pairs = [f"{attr}: {getattr(obj, attr)}" for attr in dir(obj) if attr in ["Symbol", "Description", "ContractSize", "SwapLong", "SwapShort"]]
        #     return_dict[obj.Symbol] = key_value_pairs
            
        manager.Disconnect()
        return {"symbols": symbols}
    else:
        print(f"Failed to connect to server: {MT5Manager.LastError()}")