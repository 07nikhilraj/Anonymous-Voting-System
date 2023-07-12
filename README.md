# Anonymous Voting System using Blockchain in Python
This is an anonymous voting system built with Python and blockchain technology. The system consists of three main classes: Vote, Voter, and Candidate. It uses the Proof of Stake Algorithm to mine blocks and ZKP to validate votes.

# Classes
## Vote Class
- The Vote class represents a single vote/transaction. It contains the following attributes:
- voter: The voter who casts a vote.
- candidate: The candidate who received the vote.

## Voter Class
The Voter class represents a voter. It contains the following attributes:
- id: A unique identifier for the voter.
- publicKnowledge: The public key of the voter's Ethereum account.
- credit: The number of credits the voter has(kind of reputation).
- proof: A zero-knowledge proof that the vote was cast by an eligible voter.
- secret: Secret key for ZKP

## Candidate Class
The Candidate class represents a candidate. It contains the following attributes:
- id: A unique identifier for the candidate.
- name: The name of the candidate.
- vote_count: The number of votes the candidate has received.
- manifesto: Manifesto for the candidate
- voter: Voter object of the candidate

## Validator Class
The Winner class represents a winner of the particular round. It is an extension of the voter class. It has the following methods:
- Validation of transactions
- Validation of Chain
- Validation of Block

# Proof of Stake Algorithm
The Proof of Stake Algorithm used in this system requires voters to have a certain number of credits to be eligible to cast a vote. This is to prevent Sybil attacks, where a single user creates multiple identities to gain an unfair advantage.

# Zero-Knowledge Proofs
Zero-Knowledge Proofs (ZKPs) are used to validate that a vote was cast by an eligible voter without revealing the voter's identity. This ensures that the system is truly anonymous and prevents voter coercion.

# Working
We specify the number of voters, and then you specify the number of candidates, then mention the description of candidates. Every candidate is a voter. Then the voting procedure begins, then every voter is allowed to cast his/her vote. Every vote is verified using the ZKP algorithm, designed specifically for this algorithm/ voting system. If the votes are valid, they are stored in a verified pool; else, they are stored in a malicious pool. After this, when a specific block limit is reached, the validation process begins. First of all, the validator for the chain is decided using an algorithm similar to the proof of stake, in which the voter themselves, who are not candidates, contest a mini-election to decide the winner/validator. Each voter also has credit, and if they validate the chain properly, their credits increase which helps them display more trustworthiness for the next round. The validator then verifies the transaction (transaction picked from the verified pool) and the block and then creates the block. The hash of this block is calculated using a Merkle tree, and it is hashed using the SHA256 algorithm, and this block is then added to the blockchain. This finishes the voting round. We also can, at any time, see the structure of the blockchain and also see the transactions of one particular user. Also, during the voting procedure, we can see a live chart of the candidate's share of votes. 

# Conclusion
This anonymous voting system uses blockchain technology to ensure the integrity of the voting process while maintaining the anonymity of the voters. It also implements Proof of Stake and Zero-Knowledge Proof for added security.

# Project
1.  Clone the repo
2. Run the main.py python file

