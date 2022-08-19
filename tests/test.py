import unittest

from contracting.client import ContractingClient
from contracting.stdlib.bridge.time import Datetime


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
            self.c.submit(dex, name="con_rocketswap_official_v1_1")

        self.dex = self.c.get_contract("con_rocketswap_official_v1_1")

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

        
    def setupToken(self):
        start_env = {"now": Datetime(year=2022, month=2, day=1)}

        # approvals
        ## currency approval for rocketswap dex to spend
        self.currency.approve(signer="sys", amount=999999999, to="con_rocketswap_official_v1_1")
        self.currency.approve(signer="bob", amount=999999999, to="con_rocketswap_official_v1_1")
        self.currency.approve(signer="gifty", amount=999999999, to="con_rocketswap_official_v1_1")
        self.currency.approve(signer="marvin", amount=999999999, to="con_rocketswap_official_v1_1")
        self.currency.approve(signer="suz", amount=999999999, to="con_rocketswap_official_v1_1")
        self.currency.approve(signer="mel", amount=999999999, to="con_rocketswap_official_v1_1")
        self.currency.approve(signer="day", amount=999999999, to="con_rocketswap_official_v1_1")
        self.currency.approve(signer="zen", amount=999999999, to="con_rocketswap_official_v1_1")
        self.currency.approve(signer="roon", amount=999999999, to="con_rocketswap_official_v1_1")
        ## currency approval for lite-dao contract to spend
        self.rswp.approve(signer="bob", amount=999999999999, to="con_lite_dao")
        ## RSWP approval for rocketswap dex to spend
        self.rswp.approve(signer="sys", amount=999999999, to="con_rocketswap_official_v1_1")
        self.rswp.approve(signer="bob", amount=999999999, to="con_rocketswap_official_v1_1")
        self.rswp.approve(signer="gifty", amount=999999999, to="con_rocketswap_official_v1_1")
        self.rswp.approve(signer="marvin", amount=999999999, to="con_rocketswap_official_v1_1")
        self.rswp.approve(signer="suz", amount=999999999, to="con_rocketswap_official_v1_1")
        self.rswp.approve(signer="mel", amount=999999999, to="con_rocketswap_official_v1_1")
        self.rswp.approve(signer="day", amount=999999999, to="con_rocketswap_official_v1_1")
        self.rswp.approve(signer="zen", amount=999999999, to="con_rocketswap_official_v1_1")
        self.rswp.approve(signer="roon", amount=999999999, to="con_rocketswap_official_v1_1")
        ## RSWP approval for single-asset-compound contract to spend
        self.rswp.approve(signer="bob", amount=999999999, to="con_staking_smart_epoch_single_asset")
        self.rswp.approve(signer="gifty", amount=999999999, to="con_staking_smart_epoch_single_asset")
        self.rswp.approve(signer="marvin", amount=999999999, to="con_staking_smart_epoch_single_asset")
        self.rswp.approve(signer="suz", amount=999999999, to="con_staking_smart_epoch_single_asset")
        self.rswp.approve(signer="mel", amount=999999999, to="con_staking_smart_epoch_single_asset")
        self.rswp.approve(signer="day", amount=999999999, to="con_staking_smart_epoch_single_asset")
        self.rswp.approve(signer="zen", amount=999999999, to="con_staking_smart_epoch_single_asset")
        self.rswp.approve(signer="roon", amount=999999999, to="con_staking_smart_epoch_single_asset")
        # RSWP LP approval for liquidity farm contract to spend
        self.dex.approve_liquidity(signer="bob", contract="con_rswp_lst001", to="con_liquidity_mining_smart_epoch", amount=999999999)
        self.dex.approve_liquidity(signer="gifty", contract="con_rswp_lst001", to="con_liquidity_mining_smart_epoch", amount=999999999)
        self.dex.approve_liquidity(signer="marvin", contract="con_rswp_lst001", to="con_liquidity_mining_smart_epoch", amount=999999999)
        self.dex.approve_liquidity(signer="suz", contract="con_rswp_lst001", to="con_liquidity_mining_smart_epoch", amount=999999999)
        self.dex.approve_liquidity(signer="mel", contract="con_rswp_lst001", to="con_liquidity_mining_smart_epoch", amount=999999999)
        self.dex.approve_liquidity(signer="day", contract="con_rswp_lst001", to="con_liquidity_mining_smart_epoch", amount=999999999)
        self.dex.approve_liquidity(signer="zen", contract="con_rswp_lst001", to="con_liquidity_mining_smart_epoch", amount=999999999)
        self.dex.approve_liquidity(signer="roon", contract="con_rswp_lst001", to="con_liquidity_mining_smart_epoch", amount=999999999)
        
        # create a TAU-RSWP pair pool
        self.dex.create_market(signer="sys", contract="con_rswp_lst001", currency_amount=1000, token_amount=2000)

        # TAU transfers to users
        self.currency.transfer(signer="sys", to="bob", amount=1000000)
        self.currency.transfer(signer="sys", to="gifty", amount=500000) 
        self.currency.transfer(signer="sys", to="marvin", amount=200000)
        self.currency.transfer(signer="sys", to="suz", amount=100000)
        self.currency.transfer(signer="sys", to="mel", amount=80000)
        self.currency.transfer(signer="sys", to="day", amount=60000)
        self.currency.transfer(signer="sys", to="zen", amount=40000)
        self.currency.transfer(signer="sys", to="roon", amount=20000)

        # RSWP transfers to users
        self.rswp.transfer(signer="sys", to="bob", amount=1000000)
        self.rswp.transfer(signer="sys", to="gifty", amount=500000) 
        self.rswp.transfer(signer="sys", to="marvin", amount=200000)
        self.rswp.transfer(signer="sys", to="suz", amount=100000)
        self.rswp.transfer(signer="sys", to="mel", amount=80000)
        self.rswp.transfer(signer="sys", to="day", amount=60000)
        self.rswp.transfer(signer="sys", to="zen", amount=40000)
        self.rswp.transfer(signer="sys", to="roon", amount=20000)
        
        # add liquidity to TAU-RSWP pool
        self.dex.add_liquidity(signer="bob", contract="con_rswp_lst001", currency_amount=2000)
        self.dex.add_liquidity(signer="gifty", contract="con_rswp_lst001", currency_amount=2000)
        self.dex.add_liquidity(signer="marvin", contract="con_rswp_lst001", currency_amount=2000)
        self.dex.add_liquidity(signer="suz", contract="con_rswp_lst001", currency_amount=2000)
        self.dex.add_liquidity(signer="mel", contract="con_rswp_lst001", currency_amount=2000)
        self.dex.add_liquidity(signer="day", contract="con_rswp_lst001", currency_amount=2000)
        self.dex.add_liquidity(signer="zen", contract="con_rswp_lst001", currency_amount=2000)
        self.dex.add_liquidity(signer="roon", contract="con_rswp_lst001", currency_amount=2000)

        # stake RSWP in rocketfuel
        self.dex.stake(signer="bob", amount=1000)
        self.dex.stake(signer="gifty", amount=1000)
        self.dex.stake(signer="marvin", amount=1000)
        self.dex.stake(signer="suz", amount=1000)
        self.dex.stake(signer="mel", amount=1000)
        self.dex.stake(signer="day", amount=1000)
        self.dex.stake(signer="zen", amount=1000)
        self.dex.stake(signer="roon", amount=1000)

        # stake RSWP in single-asset-compound contract
        self.contract_single_asset.addStakingTokens(signer="bob", amount=1000)
        self.contract_single_asset.addStakingTokens(signer="gifty", amount=1000)
        self.contract_single_asset.addStakingTokens(signer="marvin", amount=1000)
        self.contract_single_asset.addStakingTokens(signer="suz", amount=1000)
        self.contract_single_asset.addStakingTokens(signer="mel", amount=1000)
        self.contract_single_asset.addStakingTokens(signer="day", amount=1000)
        self.contract_single_asset.addStakingTokens(signer="zen", amount=1000)
        self.contract_single_asset.addStakingTokens(signer="roon", amount=1000)

        # stake RSWP LP in liquidity farming contract
        self.yield_farm.addStakingTokens(signer="bob", amount=100)
        self.yield_farm.addStakingTokens(signer="gifty", amount=100)
        self.yield_farm.addStakingTokens(signer="marvin", amount=100)
        self.yield_farm.addStakingTokens(signer="suz", amount=100)
        self.yield_farm.addStakingTokens(signer="mel", amount=100)
        self.yield_farm.addStakingTokens(signer="day", amount=100)
        self.yield_farm.addStakingTokens(signer="zen", amount=100)
        self.yield_farm.addStakingTokens(signer="roon", amount=100)

    def tearDown(self):
        self.c.flush()
    
    def test_01_create_proposal_should_pass(self):
        start_env = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=start_env, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])
        
        proposal = self.lite_dao.Proposals[1]
        
        self.assertTrue(proposal is not None)


    def test_02_choices_created_should_pass(self):
        start_env = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=start_env, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        proposal = self.lite_dao.Proposals[1]
        choices = proposal['choices']

        self.assertEqual(len(choices), 3)


    def test_03_fee_deducted_should_pass(self):
        start_env = {"now": Datetime(year=2022, month=2, day=1)}

        fee_amount = self.lite_dao.metadata["fee_amount"]
        bob_old_balance = self.rswp.balances["bob"]
        self.lite_dao.create_proposal(environment=start_env, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])
        bob_new_balance = self.rswp.balances["bob"]

        difference = bob_old_balance - bob_new_balance

        self.assertEqual(fee_amount, difference)

    def test_04_cast_ballot_should_pass(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=2, day=2)}
        # cast ballot
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        
        ballot_vk = self.lite_dao.Ballots[1, "forwards_index", 1, "user_vk"]
        choice = self.lite_dao.Ballots[1, "forwards_index", 1, "choice"]
        ballot_backwards_idx =  self.lite_dao.Ballots[1, "backwards_index", ballot_vk]
        
        self.assertEqual(ballot_vk, "bob")

    def test_05_cast_ballot_increments_ballot_count(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=2, day=2)}
        # cast ballot
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        
        ballot_vk = self.lite_dao.Ballots[1, "forwards_index", 1, "user_vk"]
        choice = self.lite_dao.Ballots[1, "forwards_index", 1, "choice"]
        ballot_backwards_idx =  self.lite_dao.Ballots[1, "backwards_index", ballot_vk]
        
        self.assertEqual(ballot_vk, "bob")
        self.assertEqual(ballot_backwards_idx, 1)

    def test_06_cast_ballot_after_decision_date_should_fail(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=4, day=2)}

        with self.assertRaises(AssertionError):
            self.lite_dao.cast_ballot(environment=env_1, signer="jane", proposal_idx=1, choice_idx=1)


    def test_07_cast_two_ballots_should_fail(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=2, day=2)}
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        print(self.lite_dao.Ballots[1,"backwards_index", "bob"])
        
        env_2 = {"now": Datetime(year=2022, month=2, day=3)}
        with self.assertRaises(AssertionError):
            self.lite_dao.cast_ballot(environment=env_2, signer="bob", proposal_idx=1, choice_idx=1)

        # print(self.lite_dao.Ballots[1,"backwards_index", "bob"])
        # print(self.lite_dao.Ballots[1,"forwards_index", 0, "user_vk"])
        # print(self.lite_dao.Ballots[1,"forwards_index", 1, "user_vk"])
        # print(self.lite_dao.Ballots[1,"forwards_index", 2, "user_vk"])
        # print(self.lite_dao.BallotCount[1])
    
    def test_08_counting_ballots_should_pass(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=2, day=2)}

        # casting ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)

        env_2 = {"now": Datetime(year=2022, month=3, day=2)}
        # count ballots
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1)

        ballot_count = 4
        counted = True

        self.assertEqual(self.lite_dao.BallotCount[1], ballot_count)
        self.assertEqual(self.lite_dao.Ballots[1, "counted"], counted)    

    def test_09_counting_ballots_in_batches_should_pass(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=2, day=2)}

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
        
        env_2 = {"now": Datetime(year=2022, month=3, day=2)}
        # count first batch
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1, batch_size=4)
        self.assertEqual(self.lite_dao.ProcessedBallots[1], first_batch_last_ballot_idx)

        # count second batch
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1, batch_size=4)
        self.assertEqual(self.lite_dao.ProcessedBallots[1], second_batch_last_ballot_idx)
        
    def test_10_processed_ballots_should_equal_ballot_count_after_counting_pass(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=2, day=2)}

        #cast ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)

        # count ballots 
        env_2 = {"now": Datetime(year=2022, month=3, day=2)}
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1)
        
        ballot_count = self.lite_dao.BallotCount[1]
        processed_ballots_count = self.lite_dao.ProcessedBallots[1]

        self.assertEqual(ballot_count, processed_ballots_count)
    
    def test_11_verifying_ballots_should_pass(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=2, day=2)}

        # cast ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)

        # # count ballots 
        env_2 = {"now": Datetime(year=2022, month=3, day=2)}
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1)
        # # verify ballots
        env_3 = {"now": Datetime(year=2022, month=3, day=2, hour=2)}
        self.lite_dao.verify_ballots(environment=env_3, proposal_idx=1)

        weight_for_option_0 = 971728 
        weight_for_option_1 = 298000
        weight_for_option_2 = 499000

        self.assertEqual(self.lite_dao.VerifiedBallots[1, 0], weight_for_option_0)
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 1], weight_for_option_1)
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 2], weight_for_option_2)

    def test_12_verified_ballots_should_equal_ballot_count_after_verifying_pass(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=2, day=2)}

        # cast ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)

        # # count ballots 
        env_2 = {"now": Datetime(year=2022, month=3, day=2)}
        self.lite_dao.count_ballots(environment=env_2, proposal_idx=1)
        # # verify ballots
        env_3 = {"now": Datetime(year=2022, month=3, day=2, hour=2)}
        self.lite_dao.verify_ballots(environment=env_3, proposal_idx=1)

        ballot_count = self.lite_dao.BallotCount[1]
        processed_ballots_count = self.lite_dao.VerifiedBallots[1]

        self.assertEqual(ballot_count, processed_ballots_count)
    
    def test_13_more_than_5_perc_change_in_voting_weight_should_not_count(self):
        env_0 = {"now": Datetime(year=2022, month=2, day=1)}
        # create proposal
        self.lite_dao.create_proposal(environment=env_0, signer="bob", title="hello world!", description="describe the world, before it's too late :(", date_decision=Datetime(year=2022, month=3, day=1, hour=1, minute=1), choices=['choice one is the choicest', 'choice two is the choosiest', 'choice three is for the thriceiest'])

        env_1 = {"now": Datetime(year=2022, month=2, day=2)}

        # casting ballots 
        self.lite_dao.cast_ballot(environment=env_1, signer="bob", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_1, signer="gifty", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_1, signer="marvin", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_1, signer="suz", proposal_idx=1, choice_idx=1)

        env_2 = {"now": Datetime(year=2022, month=2, day=2, hour=2, minute=10)}
        self.lite_dao.cast_ballot(environment=env_2, signer="mel", proposal_idx=1, choice_idx=0)
        self.lite_dao.cast_ballot(environment=env_2, signer="day", proposal_idx=1, choice_idx=2)
        self.lite_dao.cast_ballot(environment=env_2, signer="zen", proposal_idx=1, choice_idx=1)
        self.lite_dao.cast_ballot(environment=env_2, signer="roon", proposal_idx=1, choice_idx=1)
        
        env_3 = {"now": Datetime(year=2022, month=3, day=2)}
        # count first batch
        self.lite_dao.count_ballots(environment=env_3, proposal_idx=1, batch_size=4)
        
        # bob transfers tokens to day
        env_4 = {"now": Datetime(year=2022, month=3, day=2, hour=1, minute=5)}
        self.rswp.transfer(environment=env_4, signer="bob", to="day", amount=48637)
        
        env_5 = {"now": Datetime(year=2022, month=3, day=2, hour=1, minute=10)}
        # count second batch
        self.lite_dao.count_ballots(environment=env_5, proposal_idx=1, batch_size=4)

        weight_for_option_0 = 1050728 # bob's weight + mel's weight   
        weight_for_option_1 = 356000
        weight_for_option_2 = 560000
        
        # verify ballots
        env_6 = {"now": Datetime(year=2022, month=3, day=2, hour=1, minute=20)}
        self.lite_dao.verify_ballots(environment=env_6, proposal_idx=1)

        weight_for_option_0 = 79000 # only mel's weight. bob's weight is not counted
        weight_for_option_1 = 356000
        weight_for_option_2 = 606637 # weight increases due to bob's transfer to day
        
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 0], weight_for_option_0)
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 1], weight_for_option_1)
        self.assertEqual(self.lite_dao.VerifiedBallots[1, 2], weight_for_option_2)

if __name__ == "__main__":
    unittest.main()
