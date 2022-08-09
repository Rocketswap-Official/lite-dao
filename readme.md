# Lite DAO

### A non-custodial voting system

## How it works

#### fn: create_proposal
* Anyone can create a proposal by calling the `create_proposal` method given they have enough token to pay the fee. Each proposal has a unique ID, which is retrieved from ProposalCount. ProposalCount increments after a new proposal is created.

#### fn: cast_ballot
* Users vote using the `cast_ballot` method. 
* Anyone who holds tokens, staked tokens, lp or staked lp can cast a ballot using before `date_decision`. Ballots cast are final and cannot be changed.
* Each ballot cast increments `BallotCount[proposal_id]`
* When a ballot is cast, it is recorded in `Ballots[proposal_id]` along with a forwards_index and a backwards_index for looking up the ballot by user_vk and also by ballot_id. This is to prevent one vk casting multiple ballots.

#### fn: count_ballots
After `date_decision` no more ballots can be cast and `count_ballots` can be called. `count_ballots` iterates through all cast ballots, calculates the weight for each ballot and records the value in `CountedBallots`. `count_ballots` can be called until all ballots have been processed.

Since the application counts the ballots in batches, there is a edge case where a savvy adversary could cause mischief and potentially vote with their coins more than once, by moving coins front one address to another in between batches. For this reason we have included in a verification step which assures that tokens which are used to vote cannot be used to vote a second time.

Once `count_ballots` has been called for a proposal and has counted all the ballots `verify_ballots` can be called.

#### fn: verify_ballots

* Can be called one `count_ballots` has concluded
* ensures that the token balances in accounts have not changed dramatically since being counted.
* to be called in batches, once all ballots have been verified the Proposal is marked as `concluded` and the results are considered final.
