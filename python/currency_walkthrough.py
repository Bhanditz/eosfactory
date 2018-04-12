"""
## Example "Currency" Contract Walkthrough

EOS comes with example contracts that can be uploaded and run for testing 
purposes. We will validate our single node setup using the sample contract 
'currency'.

### Start EOS node
```
"""
import teos
teos.set_verbose(False)

daemon = teos.Daemon()
daemon.clear()
#       nodeos exe file: /mnt/e/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#    genesis state file: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/genesis.json
#        server address: 127.0.0.1:8888
#      config directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir
#      wallet directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/wallet
#     head block number: 2
#       head block time: 2018-04-10T17:20:54

# See a prove that the daemon is started:
print(daemon)
#            head block: 1047
#       head block time: 2018-04-10T16:57:27
#  last irreversible block: 1046
"""
```
### Create a wallet

Every contract requires an associated account, so first you need to create 
a wallet. To create a wallet, you need to have the wallet_api_plugin loaded 
into the nodeos process:
```
"""
wallet = teos.Wallet()
"""
```
The wallet name argument is not set: the default wallet name is 'default'.

### Load the Bios Contract

Set eosio.bios as the default system contract. This contract enables you to 
have direct control over the resource allocation of other accounts and to 
access other privileged API calls.
```
"""
contract_eosio_bios = teos.SetContract("eosio", "eosio.bios", permission="eosio")
#        transaction id: 7d5d9c7f56d46d6eab95f2dea6aaab667b5eb3d087737ada0cba5b82f26962c3
"""
```
As the set contract command call has produced the transaction id, the default 
contract is operational.

We will use an representation of the 'eosio' account:
```
"""
account_eosio = teos.EosioAccount()
"""
```
### Create an account for the "currency" contract

The account named "currency" will be used for the "currency" contract. 
Generate two public/private key pairs that will be later assigned as the 
key_owner and the key_active:
```
"""
key_owner = teos.CreateKey("key_owner")
#              key name: key_owner
#           private key: 5J4bSiNprJzPYVHqoZdSDGTTd454LiDc89AVvKT4Miv2SyzZTDF
#            public key: EOS7vDtGf9cVxEChKN7YeDgqMGrgFgvcCdN5qAUEhMMufAnPHddTb
key_active = teos.CreateKey("key_active")
#              key name: key_active
#           private key: 5KRHeQ1S7pEtCw6TMeW6WKvupuR8cVGJjpNbAN5uviXTAtvhmDW
#            public key: EOS6FfNuYYKoSa7pjhoqqeymi6iwe6j9ukVHiQxPbMeAcHmcoxRwj
"""
```
Import the two private keys into the wallet:
"""
wallet.import_key(key_owner)
wallet.import_key(key_active)
"""

You can see the contents of the wallet:
```  
"""
print(wallet)
{'keys': [['key_owner', '5J4bSiNprJzPYVHqoZdSDGTTd454LiDc89AVvKT4Miv2SyzZTDF'],
          ['key_active',
           '5KRHeQ1S7pEtCw6TMeW6WKvupuR8cVGJjpNbAN5uviXTAtvhmDW']],
 'name': 'default',
 'password': 'PW5Kih88UxyFeVeYfWiuhbBRVhxmzr4nVvyTjsuNLgP6Ropxb9SJY'}
"""
```
Create the currency account using the cleos create account command. The 
create will be authorized by the eosio account. The two public keys generated 
above will be associated with the account, one as its owner key and the other 
as its active key.
```
"""
account_currency = teos.Account(account_eosio, "currency", key_owner, key_active)
#        transaction id: 0c4e0fb1163562909a83947b77aa3ee293b880cd61d4c6610fdcd3198e2d0eb7
"""
```
As the account command call has produced the transaction id, the account is 
walid. You can see its description:
```
"""
print(account_currency)
{'account_name': 'currency',
 'permissions': [{'parent': 'owner',
                  'perm_name': 'active',
                  'required_auth': {'accounts': '',
                                    'keys': [{'key': 'EOS88rqdDApfzRMcSCTuy3HmS2gBZSW8ZokjC8cQ4aeFL7zEQqmdx',
                                              'weight': '1'}],
                                    'threshold': '1'}},
                 {'parent': '',
                  'perm_name': 'owner',
                  'required_auth': {'accounts': '',
                                    'keys': [{'key': 'EOS5WULc9uFcaME5xJbHdrrbi5xr3AhCNCogaeMGoxRkPp8PATmtc',
                                              'weight': '1'}],
                                    'threshold': '1'}}]}
"""
```
### Upload the sample "currency" contract to the blockchain

Before uploading a contract, verify that there is no current contract:
```
"""
print(account_currency.code())
#             code hash: 0000000000000000000000000000000000000000000000000000000000000000
"""
```
Upload the sample currency contract using the currency account.
```
"""
contract_currency = teos.Contract(account_currency, "currency")
print(contract_currency)
#        transaction id: 9c1b663cafcbe7ffbb18527fecfa7aa58237d00e02af125eed19b7021388238e
"""
```
Printout has a valid transaction id.

You can also verify that the code has been set:
```
"""
print(account_currency.code())
#             code hash: d6c891fbdfcff597d82e17c81354574399b01d533e53d412093f03e1950fb9d4
"""
```
Before using the currency contract, you must first create, then issue the 
currency:
```
"""
contract_currency.action(
  "create", 
  '{"issuer":"currency","maximum_supply":"1000000.0000 CUR", \
  "can_freeze":"0","can_recall":"0","can_whitelist":"0"}')
#        transaction id: afe3ed99759c637b39244556bbf14d3d49260efd37c165fb8bd1ec3c6faf6fbf

contract_currency.action(
  "issue", 
  '{"to":"currency","quantity":"1000.0000 CUR","memo":""}')
#        transaction id: 5cfc673345bedd94977eb7924e8c40a366dd4e15261b61f2742de9eec4478b42
"""
```
Verify the currency contract has the proper initial balance:
```
"""
account_currency.accounts()
"""
```
### Transfer funds using the "currency" contract

The following command shows a "transfer" action being sent to the currency 
contract, transferring "20.0000 CUR" from the currency account to the "eosio" 
account.
```
"""
contract_currency.action(
  "transfer",
  '{"from":"currency","to":"eosio","quantity":"20.0000 CUR", \
    "memo":"my first transfer"}'
)
"""
```
A successfully submitted transaction has generated a transaction ID.

### Check the "currency" contract balances

Check the state of both accounts involved in the previous transaction:
```
"""
account_currency.accounts(account_currency)
#  {
#      "rows": [
#          {
#              "balance": "980.0000 CUR",
#              "frozen": "0",
#              "whitelist": "1"
#          }
#      ],
#      "more": "false"
#  }
#

account_eosio.accounts(account_currency)
#  {
#      "rows": [
#          {
#              "balance": "20.0000 CUR",
#              "frozen": "0",
#              "whitelist": "1"
#          }
#      ],
#      "more": "false"
#  }
#
"""
```

```
"""
daemon = teos.Daemon()
daemon.clear()
print(daemon)
wallet = teos.Wallet()
contract_eosio_bios = teos.SetContract("eosio", "eosio.bios", permission="eosio")
account_eosio = teos.EosioAccount()
key_owner = teos.CreateKey("key_owner")
key_active = teos.CreateKey("key_active")
wallet.import_key(key_owner)
wallet.import_key(key_active)
account_currency = teos.Account("eosio", "currency", key_owner, key_active)
print(account_currency)
print(account_currency.code())
contract_currency = teos.Contract(account_currency, "currency")
print(contract_currency)
print(account_currency.code())
contract_currency.action(
  "create", 
  '{"issuer":"currency","maximum_supply":"1000000.0000 CUR", \
  "can_freeze":"0","can_recall":"0","can_whitelist":"0"}')
contract_currency.action(
  "issue", 
  '{"to":"currency","quantity":"1000.0000 CUR","memo":""}')
account_currency.accounts()
contract_currency.action(
  "transfer",
  '{"from":"currency","to":"eosio","quantity":"20.0000 CUR", \
    "memo":"my first transfer"}'
)
account_currency.accounts(account_currency)
account_eosio.accounts(account_currency)

"""
```
