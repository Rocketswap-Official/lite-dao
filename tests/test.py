import unittest

from contracting.client import ContractingClient
from contracting.stdlib.bridge.time import Datetime
#from contracting.stdlib.bridge.decimal import ContractingDecimal


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.c = ContractingClient()
        self.c.flush()

        with open("./basic-token.py") as f:
            code = f.read()
            self.c.submit(code, name="currency", constructor_args={"vk": "sys"})
            self.c.submit(code, name="con_rswp_lst001", constructor_args={"vk": "sys"})
            self.c.submit(code, name="con_basic_token", constructor_args={"vk": "sys"})

        self.currency = self.c.get_contract("currency")
        self.rswp = self.c.get_contract("con_rswp_lst001")


        with open("con_staking_smart_epoch_compounding_single_asset.py") as f:
            code = f.read()
            self.c.submit(code, name="con_staking_smart_epoch_single_asset")

        self.contract_single_asset = self.c.get_contract(
            "con_staking_smart_epoch_single_asset"
        )

        with open("dex.py") as f:
            dex = f.read()
            self.c.submit(dex, name="dex")

        self.dex = self.c.get_contract("dex")

        with open(
            "con_liquidity_mining_smart_epoch.py"
        ) as f:
            code = f.read()
            self.c.submit(code, name="con_liquidity_mining_smart_epoch")

        self.yield_farm = self.c.get_contract("con_liquidity_mining_smart_epoch")


        with open(
            "../lite-dao.py"
        ) as f:
            code = f.read()
            self.c.submit(code, name="con_lite_dao")

        self.lite_dao = self.c.get_contract("con_lite_dao")

        self.setupToken()

        # create a TAU-RSWP pair pool
        self.dex.create_market(signer="sys", contract="con_rswp_lst001", currency_amount=1000, token_amount=2000)

    def setupToken(self):
        
        self.rswp.approve(
            signer="sys", amount=999999999999, to="bob"
        )
        
        self.rswp.approve(
            signer="bob", amount=999999999999, to="con_lite_dao"
        )

        # transfers
        self.rswp.transfer(signer="sys", to="bob", amount=1000000)
        self.rswp.transfer(signer="sys", to="gifty", amount=500000) 
        self.rswp.transfer(signer="sys", to="marvin", amount=200000)
        self.rswp.transfer(signer="sys", to="suz", amount=100000)
        self.rswp.transfer(signer="sys", to="mel", amount=80000)
        self.rswp.transfer(signer="sys", to="day", amount=60000)
        self.rswp.transfer(signer="sys", to="zen", amount=40000)
        self.rswp.transfer(signer="sys", to="roon", amount=20000)
        
        # approve dex to spend tokens
        self.currency.approve(signer="sys", amount=999999999, to="dex")
        self.rswp.approve(signer="sys", amount=999999999, to="dex")

    def tearDown(self):
        self.c.flush()
    
    def test_01_create_proposal_should_pass(self):
        start_env = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=start_env, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])
        
        proposal = self.lite_dao.Proposals[1]
        
        self.assertTrue(proposal is not None)


    def test_02_choices_created_should_pass(self):
        start_env = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=start_env, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        proposal = self.lite_dao.Proposals[1]
        choices = proposal['choices']

        self.assertEqual(len(choices), 3)


    def test_03_fee_deducted_should_pass(self):
        start_env = {"now": Datetime(year=2021, month=2, day=1)}

        fee_amount = self.lite_dao.metadata["fee_amount"]
        bob_old_balance = self.rswp.balances["bob"]
        self.lite_dao.create_proposal(environment=start_env, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])
        bob_new_balance = self.rswp.balances["bob"]

        difference = bob_old_balance - bob_new_balance

        self.assertEqual(fee_amount, difference)

    def test_04_cast_ballot_should_pass(self):
        env_0 = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2021, month=2, day=2)}
        # cast ballot
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        
        ballot_vk = self.lite_dao.Ballots[1, "forwards_index", 1, "user_vk"]
        choice = self.lite_dao.Ballots[1, "forwards_index", 1, "choice"]
        ballot_backwards_idx =  self.lite_dao.Ballots[1, "backwards_index", ballot_vk]
        
        self.assertEqual(ballot_vk, "bob")

    def test_05_cast_ballot_increments_ballot_count(self):
        env_0 = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2021, month=2, day=2)}
        # cast ballot
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        
        ballot_vk = self.lite_dao.Ballots[1, "forwards_index", 1, "user_vk"]
        choice = self.lite_dao.Ballots[1, "forwards_index", 1, "choice"]
        ballot_backwards_idx =  self.lite_dao.Ballots[1, "backwards_index", ballot_vk]
        
        self.assertEqual(ballot_vk, "bob")
        self.assertEqual(ballot_backwards_idx, 1)

    def test_06_cast_ballot_after_decision_date_should_fail(self):
        env_0 = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2021, month=4, day=2)}

        with self.assertRaises(AssertionError):
            self.lite_dao.cast_ballot(environment=env_1, signer="jane", proposal_idx=1, choice_idx=1)


    def test_7_cast_two_ballots_should_fail(self):
        env_0 = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2021, month=2, day=2)}
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        print(self.lite_dao.Ballots[1,"backwards_index", "bob"])
        
        env_2 = {"now": Datetime(year=2021, month=2, day=3)}
        with self.assertRaises(AssertionError):
            self.lite_dao.cast_ballot(environment=env_2, signer="bob", proposal_idx=1, choice_idx=1)

        # print(self.lite_dao.Ballots[1,"backwards_index", "bob"])
        # print(self.lite_dao.Ballots[1,"forwards_index", 0, "user_vk"])
        # print(self.lite_dao.Ballots[1,"forwards_index", 1, "user_vk"])
        # print(self.lite_dao.Ballots[1,"forwards_index", 2, "user_vk"])
        # print(self.lite_dao.BallotCount[1])
    
    def test_8_counting_ballots_should_pass(self):
        env_0 = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2021, month=2, day=2)}

        # casting ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)

        env_2 = {"now": Datetime(year=2021, month=3, day=2)}
        # count ballots
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1)

        ballot_count = 4
        counted = True

        self.assertEqual(self.lite_dao.BallotCount[1], ballot_count)
        self.assertEqual(self.lite_dao.Ballots[1, "counted"], counted)    

    def test_9_counting_ballots_in_batches_should_pass(self):
        env_0 = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2021, month=2, day=2)}

        # casting ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="mel", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="day", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="zen", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="roon", proposal_idx=1, choice_idx=1)

        first_batch_last_ballot_idx = 4
        second_batch_last_ballot_idx = 8
        
        env_2 = {"now": Datetime(year=2021, month=3, day=2)}
        # count first batch
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1, batch_size=4)
        self.assertEqual(self.lite_dao.ProcessedBallots[1], first_batch_last_ballot_idx)

        # count second batch
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1, batch_size=4)
        self.assertEqual(self.lite_dao.ProcessedBallots[1], second_batch_last_ballot_idx)
        
    def test_10_processed_ballots_should_equal_ballot_count_after_counting_pass(self):
        env_0 = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2021, month=2, day=2)}

        #cast ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)

        # count ballots 
        env_2 = {"now": Datetime(year=2021, month=3, day=2)}
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1)
        
        ballot_count = self.lite_dao.BallotCount[1]
        processed_ballots_count = self.lite_dao.ProcessedBallots[1]

        self.assertEqual(ballot_count, processed_ballots_count)

    def test_11_verifying_ballots_should_pass(self):
        env_0 = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2021, month=2, day=2)}

        # cast ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)

        # count ballots 
        env_2 = {"now": Datetime(year=2021, month=3, day=2)}
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1)
        # verify ballots
        env_3 = {"now": Datetime(year=2021, month=3, day=2, hour=2)}
        self.lite_dao.verify_ballots(environment=env_3, proposal_idx=1)

        weight_for_option_0 = 972728 # due to a deducted fee of 27272 from creating proposal
        weight_for_option_1 = 300000
        weight_for_option_2 = 500000

        self.assertEqual(self.lite_dao.VerifiedBallots[1, 0], weight_for_option_0)
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 1], weight_for_option_1)
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 2], weight_for_option_2)
    
    def test_12_moving_assets_between_addresses_between_batches_should_not_count(self):
        env_0 = {"now": Datetime(year=2021, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2021, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2021, month=2, day=2)}

        # casting ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)

        env_2 = {"now": Datetime(year=2021, month=2, day=2, hour=2, minute=10)}
        self.lite_dao.cast_ballot(environment=env_2, signer="mel", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_2, signer="day", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_2, signer="zen", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_2, signer="roon", proposal_idx=1, choice_idx=1)

        first_batch_last_ballot_idx = 4
        second_batch_last_ballot_idx = 8
        
        env_3 = {"now": Datetime(year=2021, month=3, day=2)}
        # count first batch
        self.lite_dao.count_ballots(environment=env_3, proposal_idx=1, batch_size=4)

        weight_for_option_0 = 972728 # bob's weight
        weight_for_option_1 = 360000
        weight_for_option_2 = 560000

        # bob transfers tokens to day
        env_4 = {"now": Datetime(year=2021, month=3, day=2, hour=1, minute=5)}
        self.rswp.transfer(environment=env_4, signer="bob", to="day", amount=900000)
        
        env_5 = {"now": Datetime(year=2021, month=3, day=2, hour=1, minute=10)}
        # count second batch
        self.lite_dao.count_ballots(environment=env_5, proposal_idx=1, batch_size=4)

        weight_for_option_0 = 80000 # only mel's weight. bob's weight is not counted
        weight_for_option_1 = 360000
        weight_for_option_2 = 1460000 # weight increases due to bob's transfer
        
        # verify ballots
        env_6 = {"now": Datetime(year=2021, month=3, day=2, hour=1, minute=20)}
        self.lite_dao.verify_ballots(environment=env_6, proposal_idx=1)

        
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 0], weight_for_option_0)
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 1], weight_for_option_1)
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 2], weight_for_option_2)
        

        
        
        


if __name__ == "__main__":
    unittest.main()
