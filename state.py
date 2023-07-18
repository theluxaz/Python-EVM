from external_contract import ExternalContract

import pickledb


class State:

    def __init__(self,testing:bool) -> None:
        if(testing):
            db = pickledb.load('EVM_STATE_TESTING.db', False)         
        else:
            db = pickledb.load('EVM_STATE.db', False)         
        self.EVM_STATE = db
        # self.self_state = db.get(address)
        
    def get(self,key):
        return self.EVM_STATE.get(key)
    def set(self,key,value):
        return self.EVM_STATE.set(key,value)
    def save(self):
        self.EVM_STATE.dump()
    

        
        