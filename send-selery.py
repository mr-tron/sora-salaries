from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from scalecodec.type_registry import load_type_registry_file
import csv
import sys

calls = []
with open(sys.argv[1], newline='') as transfers_val_csv:
    transfers_val = csv.reader(transfers_val_csv, delimiter=',')
    next(transfers_val, None)
    for row in transfers_val:
        calls.append({
            "to": row[1],
            "amount": row[2],
            "asset_id": '0x0200040000000000000000000000000000000000000000000000000000000000'
        })

with open(sys.argv[2], newline='') as transfers_pswap_csv:
    transfers_pswap = csv.reader(transfers_pswap_csv, delimiter=',')
    next(transfers_pswap, None)
    for row in transfers_pswap:
        calls.append({
            "to": row[1],
            "amount": row[2],
            "asset_id": '0x0200050000000000000000000000000000000000000000000000000000000000'
        })

print("calls {}".format(calls));

custom_type_registry = load_type_registry_file("custom_types.json")
substrate = SubstrateInterface(
    url="wss://ws.framenode-1.s1.dev.sora2.soramitsu.co.jp/",
    ss58_format=69,
    type_registry_preset='default',
    type_registry=custom_type_registry
)

keypair = Keypair.create_from_mnemonic('rifle banner arrange armed path setup speak person urge ball nerve act')

call = substrate.compose_call(
    call_module='Balances',
    call_function='transfer',
    call_params={
        'dest': 'cnS1SDG3g7wYgpEAjkg1R96rfrNUsCnoQLKejpLy6tJpw3wWK',
        'value': 1 * 10**18
    }
)

extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)
receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True, wait_for_finalization=True)
print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))
