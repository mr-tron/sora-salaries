from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from scalecodec.type_registry import load_type_registry_file
import csv


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
