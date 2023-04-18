from hashlib import sha256
from random import randint
G = 6888568692585230484085178164612752085904825452153643755802747
P = 1301684163193187640725836061992756910805734280651377378363069
import collections
import time
import json
mpp = {}
mpp1 = {}
mph = {}
verified_pool=[]
malicious_pool=[]
BLOCKSIZE = 3
class Vote:
    def __init__(self, voter,candidate):
        self.voter=voter
        self.candidate = candidate 
        self.timestamp = time.time() 
    def ZKP_TransactionVerification(self):
            
        ROUNDS = 500
        #Multiple rounds to ensure that the 
        for Round in range(ROUNDS):

            y = self.voter.publicKnowledge

            # Node: Chooses 0 <= r < p - 1, sends h = pow(g,r,p)
            h = self.voter.Prove(0, None)

            # Second Step of ZKP:
            # Miner: Gives b = randint(0,1)
            # Node: Sends s = r+b*x % p-1
            b = randint(0,1)
            s = self.voter.Prove(1, b)

            # Step 4: verify
            # Miner: Checks if pow(g,s,p) == h*pow(y,b,p) % p
            valid = pow(G,s,P) == (h*pow(y,b,P)) % P
            
            if not valid:
               return False
        return True
        
    def getVotingData(self): 
        return str(self.voter.id) +" "+ self.candidate.name + " "+ str(self.timestamp)
class Block:
    def __init__ (self,prev_hash,merkleRootHash,timestamp,hash):
        self.prev_hash=prev_hash
        self.merkleRootHash=merkleRootHash
        self.timestamp=timestamp
        self.hash=hash
        
    def computeHash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:    
    def __init__(self):
        self.chain_array=[]
    def create_genesis(self):
        to_hash1=str("0")+str("-1")+str(time.time())
        hashblock= sha256(to_hash1.encode()).hexdigest()
        genesis_block=Block("-1","0",time.time(),hashblock)
        genesis_block.hash=Block.computeHash(genesis_block)
        self.chain_array.append(genesis_block)   
    def last_block(self):
        return self.chain_array[-1]
    def add_block(self,Block):
        self.chain_array.append(Block)
        return True     
def CalculateMerkleRoot(hashes_List_Of_Transactions):
    tempList=hashes_List_Of_Transactions
    while len(tempList)>1:
        tmp=[]
        if(len(tempList)%2!=0):            #if odd size then duplicate last elem
            tempList.append(tempList[-1])
        for i in range(0, len(tempList), 2):
            hashPair=tempList[i]+tempList[i+1]       #A+B
            tmp.append(sha256(hashPair.encode()).hexdigest())
        tempList=tmp
    return tempList[0]
        
def winner(arr_of_voter,arr_of_cand):
    print("********************")
    print("The consensus to decide who will be the validator of this round begins\n")
    st={}
    pot=[]
    n=len(arr_of_voter)
    for i in range(n):
        if arr_of_voter[i].id in mpp1:
            print("You are a candidate, you cannot become a validator \n")
            continue 
        f = int(input("Do you wish to become a validator? (0/1) "))
        if f == 1:
            pot.append(arr_of_voter[i])
    for i in range(len(pot)):
        print("The ID of the voter is: "+str(pot[i].id))
        print("The credit of the voter is: "+str(pot[i].credit))
        st[pot[i]]=0
    
    for i in range(n):
        pot_id = int(input("Enter the id of the validator you want to vote for "))
        st[mph[pot_id]]+=1
    st_f = sorted(st.items(), key=lambda x:x[1])
    return st_f[len(pot)-1][0]

class voter:
    
    def __init__(self,id,weight:int,credit:int,prev_trans):
        self.id=id
        self.secret = randint(1,10000000) #private key of the node
        self.publicKnowledge = pow(G,self.secret,P) #power(G,secret) (mod P); public key
        # G -> Generator, P -> Prime number, 
        # brute method of solving for x -> Disc log
        self.r = None
        # r -> random number belonging to [0,p-1]
        self.votingWeight = weight
        self.credit=credit#
        self.prev_trans=prev_trans
    
    def add_prev(self,Transac):
        self.prev_trans.append(Transac)    
    
    def Prove(self,questionNumber,verifierData):
        if questionNumber==0:
            #first step of ZKP, h = power(G,r) (mod p)
            self.r = randint(0, P-1)
            h = pow(G,self.r,P)
            return h

        else:
            #third step of ZKP:
            b = verifierData
            x = self.secret
            s = (self.r + b*x) % (P-1)
            return s

class candidate:
    
    def __init__(self,id,name,manifesto,voter):
        self.id=id
        self.name=name
        self.manifesto=manifesto
        self.votes=0 
        self.voter=voter
    def addVotes(self):
        self.votes=self.votes+1
        
    
class validator:
    def __init__(self,voter_obj):
        self.voter=voter_obj
    def validate_chain(self,chain_array):
        _prevBlock = "-1"
        for block in chain_array:
            if block.prev_hash==_prevBlock:
                _prevBlock = block.hash
            else:
                return False
            return True  


def voter_adding(arr_of_voter,no_of_voters):
    for i in range(no_of_voters):
        list_of_prev=[]
        id = i+1
        per =voter(id,100,100,list_of_prev)
        mph[id]=per
        arr_of_voter.append(per)
        

def candidate_adding(arr_of_cand,no_of_cand):
    
    for i in range(no_of_cand):
        list_of_prev=[]
        id=int(input("Enter ID of candidate: "))
        v_id=int(input("Enter  Voter ID of candidate: "))
        name=input("Enter candidate name: ")
        manifesto=input("Write the manifesto for the candidate: ")
        cand=candidate(id,name,manifesto,mph[v_id])
        mpp[id]=cand
        mpp1[v_id]=cand
        arr_of_cand.append(cand)

def voting_procedure(arr_of_cand,arr_of_voter,no_of_cand,no_of_voters,BC):
    print("******** ********")
    # DISPLAYING THE MANIFESTO OF CANDIDATES
    for i in range(len(arr_of_cand)):
        print("The ID of the candidate is: "+str(arr_of_cand[i].id))
        print("The name of the candidate is: "+arr_of_cand[i].name)
        print("The manifesto of the candidate is: "+arr_of_cand[i].manifesto)
        print("**** ****")

    for i in range(len(arr_of_voter)):
        if arr_of_voter[i].credit < 50:
            print("Your credits are too low for you to vote \n")
            continue 
        cand_id = int(input("Enter the id of the candidate you want to vote for "))
        vote_trans=Vote(arr_of_voter[i],mpp[cand_id])
        if vote_trans.ZKP_TransactionVerification() == True:
            verified_pool.append(vote_trans)
        else:
            malicious_pool.append(vote_trans)
        
        if len(verified_pool) == BLOCKSIZE:
            winner_of_round=winner(arr_of_voter,arr_of_cand)
            leader_of_chain=validator(winner_of_round)
            winner_of_round.credit+=50
            print(winner_of_round.id)
            chain_true=leader_of_chain.validate_chain(BC.chain_array)
            last_blc=BC.last_block()
            if chain_true:
                hash_of_trans=[]
                for transac in verified_pool:
                    to_hash=transac.getVotingData()
                    hash_of_trans.append(sha256(to_hash.encode()).hexdigest())
                    transac.candidate.addVotes()
                    transac.voter.add_prev(transac)
                    # print(transac.candiid)
                    
                merkle_root=CalculateMerkleRoot(hash_of_trans) 
                to_hash1=str(merkle_root)+str(last_blc.hash)+str(time.time())
                hashblock= sha256(to_hash1.encode()).hexdigest()
                newBlock=Block(last_blc.hash,merkle_root,time.time(),hashblock)
                BC.chain_array.append(newBlock)
                verified_pool.clear()
    
    if len(verified_pool)!=0:
        winner_of_round=winner(arr_of_voter,arr_of_cand)
        leader_of_chain=validator(winner_of_round)
        winner_of_round.credit+=50
        print(winner_of_round.id)
        chain_true=leader_of_chain.validate_chain(BC.chain_array)
        last_blc=BC.last_block()
        if chain_true:
            hash_of_trans=[]
            for transac in verified_pool:
                to_hash=transac.getVotingData()
                hash_of_trans.append(sha256(to_hash.encode()).hexdigest())
                transac.candidate.addVotes()
                transac.voter.add_prev(transac)
                # print(transac.candiid)
                
            merkle_root=CalculateMerkleRoot(hash_of_trans) 
            to_hash1=str(merkle_root)+str(last_blc.hash)+str(time.time())
            hashblock= sha256(to_hash1.encode()).hexdigest()
            newBlock=Block(last_blc.hash,merkle_root,time.time(),hashblock)
            BC.chain_array.append(newBlock)
            verified_pool.clear()
    
    res=[]
    for i in range(len(arr_of_cand)):
        res.append([arr_of_cand[i],arr_of_cand[i].votes])
    res.sort(key = lambda x: x[1])
    res.reverse()
    print("********** Here are the results of the election: **********\n")
    for i in range(len(res)):
        print("The id of the candidate is " + str(res[i][0].id) + ", the name is " + res[i][0].name + ", with " + str(res[i][1]) + " votes.\n")

def main():
    
    BC=Blockchain()
    BC.create_genesis()

    # print(arr_of_cand)
    run=True
    while run:
        print("******** ********")
        print("Enter 1 for : Begin the voting procedure\nEnter -1 to exit \nEnter 2 to check Transactions against the user\nEnter 3 to check block structure")
        val=int(input())
        if val == -1:
            run=False
        elif val == 1:
            arr_of_voter=[]
            arr_of_cand=[]
            no_of_voters=int(input("Enter the number of voters: "))
            voter_adding(arr_of_voter,no_of_voters)
            no_of_cand=int(input("Enter number of candidate: "))
            candidate_adding(arr_of_cand,no_of_cand) 
            voting_procedure(arr_of_cand,arr_of_voter,no_of_voters,no_of_cand,BC)  
        elif val == 2:
            voter_id=int(input("Please Enter the voter ID whose previous transactions you want to view: "))
            if mph.get(voter_id) is None:
                print("\nVoter does NOT exist.\n")
            elif len(mph[voter_id].prev_trans)==0:
                print("No transactions have occured for this voter")
            else:
                for transac in mph[voter_id].prev_trans:
                    print(str(transac.voter.id)+" voted for "+transac.candidate.name+" at "+ str(transac.timestamp))
        elif val == 3:
            for block in BC.chain_array:
                print("previous hash is ",block.prev_hash," current block hash is ",block.hash," merke root is ",block.merkleRootHash,"\n")
    
    
    
    
if __name__=="__main__":
    main()



