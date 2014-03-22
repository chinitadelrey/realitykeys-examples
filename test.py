#!/usr/bin/python

import realitykeysdemo
import unittest
from unittest import TestCase
from pybitcointools import * # https://github.com/vbuterin/pybitcointools

class MakeKeysTestCast(TestCase):

    bob_seed = 'bob-082b113a7e2a5c6c1c9c682b8b25087c'
    bob_pub = '0460d353f4c834bccd1a0e690dc5b7a3c0e07f1ed916f05234ea539c08c0792f3ee90b7704a329e6e0a9e4cda2eb156ac6b1721f53a308d2bda2cce56efa925ddd'
    bob_addr_mainnet = '12fai6JhCHKGdDpJCM8ej3g7RySThdMxCD'
    bob_addr_testnet = 'mhBY19Pg1JkXQLHuuv72YxtSHy3Acje1NJ'

    alice_seed = 'alice-7d267a6b6b7bd0460fcd4a37208dea46'
    alice_pub = '04e08a571e7a61d03fb293be00a8a3e106dfc78cc47e6ef7e088850f3883b22deaa4c904b7e9e96f6ce70a2e9c7a060374f3bbf3d5b081d68d98e6e73ec0093b22'
    alice_addr_testnet = 'mraEF8MUVhpXuXVJDNhM11n9ZbfPiPa8Kh'

    fact_id = 3

    inputs = ["mhBY19Pg1JkXQLHuuv72YxtSHy3Acje1NJ:98b6cda0652dabd38a41ab454fac05714ca2ecf29af22ac351c3fb245b57a32e:0:100000",       
            "mraEF8MUVhpXuXVJDNhM11n9ZbfPiPa8Kh:99cbbbdaf1d1d8d58289f2e5a22d00bc2e6ee4132ed330e21d9b0919ff9b3940:1:100000"]

    # The transaction as completed by setup
    claimable_tx = '010000000240399bff19099b1de230d32e13e46e2ebc002da2e5f28982d5d8d1f1dabbcb99010000008a473044022033affa6041c1682eced141b93089240e8f9a17619a9d57be2dccb6e60a72ff2302200e2d12008f1b4ef935b9d1d65264ce6d9725367ae012455b78d6ba97fff8ac0e014104e08a571e7a61d03fb293be00a8a3e106dfc78cc47e6ef7e088850f3883b22deaa4c904b7e9e96f6ce70a2e9c7a060374f3bbf3d5b081d68d98e6e73ec0093b22ffffffff2ea3575b24fbc351c32af29af2eca24c7105ac4f45ab418ad3ab2d65a0cdb698000000008c493046022100be1d6ac87a95d3c0fc785b2c4ef2c7f9f65fea366a73279f631e87b356785896022100ce73f9bdb28ac5fea1b1fedd19e7974d29ef4cf3c9a43a03a4dcdbe969532b6101410460d353f4c834bccd1a0e690dc5b7a3c0e07f1ed916f05234ea539c08c0792f3ee90b7704a329e6e0a9e4cda2eb156ac6b1721f53a308d2bda2cce56efa925dddffffffff0120bf02000000000017a914f6641de65e2bf13639f38bd1524cc0e56e065f068700000000'

    claim_tx = '0100000001477a55f2f8cc1df96812a1257f5205747f3fe6b6dd5aad3f1b5da3c4baecaa0500000000d3004830450220080389b3c32f8db64bd2e90cd5b31f120ced55bc2b117fab0a679588df90e871022100d7f427d438b26018ce442cf2d8aaa3257bc4ce28c0953ccc11bbd8c5cc1297af014c87514104cd0298cfa9c3bb885ed42159f2ec3a5cc6cc294a022ce5dff8806fb5101b858e184f2d334996ff207d2f0dac386ad47bba1fa84269443be03cd376aae77002cc4104465d674476158492cf262cb9a3c7135ea9c16ea5c6e380828ddc521524360db67bb8138e358253ef20c040cdd43d80a2430b09c415dc3f6b9ddcbd07ab2cfed152aeffffffff0120bf0200000000001976a9147947f20d56ea47e518dce3ce23b604e45e3a959f88ac00000000'

    def test_make_keys(self):

        alice_priv = realitykeysdemo.user_private_key(False, self.alice_seed)
        self.assertEqual( privtopub(alice_priv), self.alice_pub)
        self.assertEqual( pubtoaddr(privtopub(alice_priv), 111), self.alice_addr_testnet)

        bob_priv = realitykeysdemo.user_private_key(False, self.bob_seed)
        self.assertEqual( privtopub(bob_priv), self.bob_pub)

        settings = {
            'seed': self.bob_seed
        }
        out = realitykeysdemo.execute_makekeys(settings)
        self.assertEqual( out[0], self.bob_pub)
        self.assertEqual( out[1], self.bob_addr_mainnet)

        settings['testnet'] = True
        out = realitykeysdemo.execute_makekeys(settings)
        self.assertEqual( out[0], '0460d353f4c834bccd1a0e690dc5b7a3c0e07f1ed916f05234ea539c08c0792f3ee90b7704a329e6e0a9e4cda2eb156ac6b1721f53a308d2bda2cce56efa925ddd')
        self.assertNotEqual( out[1], self.bob_addr_mainnet)
        self.assertEqual( out[1], self.bob_addr_testnet)

    def test_unspent_outputs(self):
        addr = "mhBY19Pg1JkXQLHuuv72YxtSHy3Acje1NJ"
        ret = realitykeysdemo.unspent_outputs(addr, self.inputs)
        self.assertEqual(len(ret), 1)
        o = ret[0]
        self.assertEqual(o['address'], addr)
        self.assertEqual(o['value'], 100000)
        self.assertEqual(o['output'], "98b6cda0652dabd38a41ab454fac05714ca2ecf29af22ac351c3fb245b57a32e:0")

        addr = "mraEF8MUVhpXuXVJDNhM11n9ZbfPiPa8Kh"
        ret = realitykeysdemo.unspent_outputs(addr, self.inputs)
        self.assertEqual(len(ret), 1)
        o = ret[0]
        self.assertEqual(o['address'], addr)
        self.assertEqual(o['value'], 100000)
        self.assertEqual(o['output'], "99cbbbdaf1d1d8d58289f2e5a22d00bc2e6ee4132ed330e21d9b0919ff9b3940:1")

    def test_setup(self):
        settings = {
            'seed': self.alice_seed,
            'testnet': True,
            'no_pushtx': True,
        }

        # This should fail because we can't get the inputs for testnet even if they're there...
        self.assertRaises(Exception, realitykeysdemo.execute_setup, settings, self.fact_id, self.alice_pub, 90000, self.bob_pub, 90000, None)

        settings['inputs'] = self.inputs
        out = realitykeysdemo.execute_setup(settings, self.fact_id, self.alice_pub, 90000, self.bob_pub, 90000, None)
        alice_tx = out[0]
        alice_tx_obj = deserialize(alice_tx)
        #print tx_obj
        self.assertEqual(180000, alice_tx_obj['outs'][0]['value'])

        settings['seed'] = self.bob_seed
        #settings['verbose'] = True
        out = realitykeysdemo.execute_setup(settings, self.fact_id, self.alice_pub, 90000, self.bob_pub, 90000, alice_tx)
        bob_tx = out[0]
        bob_tx_obj = deserialize(bob_tx)
        self.assertEqual(180000, bob_tx_obj['outs'][0]['value'])
        self.assertNotEqual(alice_tx, bob_tx)

        self.assertEqual(self.claimable_tx, bob_tx)

    def test_claim(self):
        settings = {
            'seed': self.alice_seed,
            'testnet': True,
            'no_pushtx': True,
        }
        previous_tx_obj = deserialize(self.claimable_tx)
        previous_tx_hash = txhash(self.claimable_tx)
        self.assertEqual('05aaecbac4a35d1b3fad5addb6e63f7f7405527f25a11268f91dccf8f2557a47', previous_tx_hash)
        spendable_outputs = ['' + ':' + previous_tx_hash + ':' + '0' + ':' + '180000']
        settings['inputs'] = spendable_outputs

        out = realitykeysdemo.execute_claim(settings, 3, self.alice_pub, self.bob_pub)
        tx = out[0]
        self.assertEqual(tx, self.claim_tx)

        settings = {
            'seed': self.bob_seed,
            'testnet': True,
            'no_pushtx': True,
        }
        previous_tx_obj = deserialize(self.claimable_tx)
        previous_tx_hash = txhash(self.claimable_tx)
        self.assertEqual('05aaecbac4a35d1b3fad5addb6e63f7f7405527f25a11268f91dccf8f2557a47', previous_tx_hash)
        spendable_outputs = ['' + ':' + previous_tx_hash + ':' + '0' + ':' + '180000']
        settings['inputs'] = spendable_outputs

        # Loser shouldn't win
        self.assertRaises(Exception, realitykeysdemo.execute_claim, settings, self.fact_id, self.alice_pub, self.bob_pub)

def main():
    unittest.main() 

if __name__ == '__main__':
    main()