#!/usr/bin/env python3

from neo.Core.Blockchain import Blockchain
from neo.Core.Block import Block
from neo.IO.MemoryStream import MemoryStream
from neo.Implementations.Blockchains.LevelDB.LevelDBBlockchain import LevelDBBlockchain
from neo.Implementations.Blockchains.LevelDB.DBPrefix import DBPrefix
from neo.Settings import settings
from neocore.IO.BinaryReader import BinaryReader
from neocore.IO.BinaryWriter import BinaryWriter
from neo.IO.MemoryStream import StreamManager,MemoryStream
import argparse
import os
import shutil
from tqdm import trange
from prompt_toolkit import prompt
import io
import binascii
badblock1550271=binascii.unhexlify(b'000000007a5549e47470d3f928e6b28417d99e86196b4af66ab98cff1b4610836ef51887401c27dabf0ec35eceb3f1212a17b43b280daa0fe8cc659a8f4e3348f165f27c680c2d5bbfa71700bb5ba79f1a6ca7edcc829bc363b3af945a5d1fb7eda5e9bd42afa0e001fd45014000d3aa781aa3ce12fe0fc9cfc78a114c6ca1653a7d47f86c8b943b03e5ffaf3af1912f3f355514e88b5ce8312095935de4f0aacb7c55aa173433d2eaf887225240c2b73819e208d6716bd24b1107d2d65d4cc48eb64f4d2da3df0d2d70e318e31b52c2ea078d82e40abbd4dca88479de00cb2f3501ad7e9a03cd25ee35fbf3241b400a17adbe0734b858e0d282eb73a22cfe1077213c8c900b14424f08477241ee6fdbd81dee91fd5ffe5112db4852e25451b1dfb3c2da4d22cf2e25ecee1574bdda408cebc8482dbbdcbe5d3f3715be76a886dcb0bfa9f75fd4a36978e45db11473f8481d48ba229e61d6a5468c6099c38311daf4c9fac808712b2092497d2542434c4060d40d0d948aeeec6ced28c11804e74ee6b1ce2156244aa82eaa774f8c53eb33d575b564b75fb52eed91a2f008b654dc0eb627af6110724b5fe73e99de70513ef155210209e7fd41dfb5c2f8dc72eb30358ac100ea8c72da18847befe06eade68cebfcb9210327da12b5c40200e9f65569476bbff2218da4f32548ff43b6387ec1416a231ee8210344925b6126c8ae58a078b5b2ce98de8fff15a22dac6f57ffd3b108c72a0670d121025bdf3f181f53e9696227843950deb72dcd374ded17c057159513c3d0abe20b6421026ce35b29147ad09e4afe4ec4a7319095f08198fa8babbe3c56e970b143528d2221039dafd8571a641058ccc832c5e2111ea39b09c0bde36050914384f7a48bce9bf92103c089d7122b840a4935234e82e26ae5efd0c2acb627239dc9f207311337b6f2c157ae030000bb5ba79f00000000d1005551515151515151515151515a515152515157535300005a02e50000005f02cb0002d400013f0155012301390121c11163726561746547656e3041756374696f6e6727465434429b64ac7d34c81edd3c2176b18b11340120e14d105e7d750e38d78cefacb2362a2ba5e679440000014140461d47d55932846f793368cc22ce33824964c84437bf016ea9c8eec6568ee5c83527f9d24b4205e815fda81e39c4f0455272f41966318564dcc683c7519e6a572321023ab1869e8df49439a92b2d8c39c7f2977d0fee0de65ad277cbbb8627b56ad578acd100575151515151515151515151575155575652575252000002c90002ca00000002d2005202cd00013001510135013a0121c11163726561746547656e3041756374696f6e6727465434429b64ac7d34c81edd3c2176b18b11340120e14d105e7d750e38d78cefacb2362a2ba5e6794400000141408cc7a47a127072880650dff2f078af7adaa01932539fefcd5521c0613b660ed41eaa5eab908428b7d67614d9664d0f02b8f2b97280c5ab1f45c2797dd3c3ca722321023ab1869e8df49439a92b2d8c39c7f2977d0fee0de65ad277cbbb8627b56ad578ac')
badblock1550275=binascii.unhexlify(b'0000000089538c5712c504cee690deeff31dbf92dc82b9c3e7863501e5297e36f25adcabc4cde1bea77b3dd88eb39e371ea8a707eb86ecbedd6f74cf0513340ae253b30d220d2d5bc3a717000df5eda48d8f80aacc829bc363b3af945a5d1fb7eda5e9bd42afa0e001fd4501406afe27e5ca7b4b7a053a466fc0293989827ab89f05f7bee570b815b2e8d97fbe5eabd7f61ea8b954a620ece2663bf5731b956ffa61c563b2b9de87667f6f8e534021606005ab6987153c7c0df12da6e8947f0bd9f4f6e0c6507f80ff028cf42f836e7dbecf11682b0e2850926ba348e76e41f4ee99531cefa984905d89176caeb440822e1c96cc8b0fb54c5f25285f8a4580daf9f9e3328c7b446fa1c32d3ebf3dcb4fcd63b316406ab062e3772b6e0cb25fdbec49166d0374e4302aab8eaba513e640301f9238c0d2ea5fcdb80f6f554e496c71c5c014b9f08805ae0198edc494239f1ceca685bf10960ab594b85e619b4977c51a58d8d00dfe074bde2f93caa2929140233d8b5085904b8b997998373a89b954b4d9cbabcfa2e53d51b65283817ca06438f4c955d7bad7d448b7fa00162ccb7bec3c2480a50dbec3409bbac3dbe93a03f155210209e7fd41dfb5c2f8dc72eb30358ac100ea8c72da18847befe06eade68cebfcb9210327da12b5c40200e9f65569476bbff2218da4f32548ff43b6387ec1416a231ee8210344925b6126c8ae58a078b5b2ce98de8fff15a22dac6f57ffd3b108c72a0670d121025bdf3f181f53e9696227843950deb72dcd374ded17c057159513c3d0abe20b6421026ce35b29147ad09e4afe4ec4a7319095f08198fa8babbe3c56e970b143528d2221039dafd8571a641058ccc832c5e2111ea39b09c0bde36050914384f7a48bce9bf92103c089d7122b840a4935234e82e26ae5efd0c2acb627239dc9f207311337b6f2c157ae0300000df5eda400000000d100595151515151515151515151585258515751555254000002db0002cd00000002d40002cd0002d10001360133012301640121c11163726561746547656e3041756374696f6e6727465434429b64ac7d34c81edd3c2176b18b11340120e14d105e7d750e38d78cefacb2362a2ba5e679440000014140d1219f1390f1785038e63151de555ed8aa3f4969594a12c569c9fc5a1f9a933b1d29f2fd8d3003e6d081479823c6909464c29f5e18ef6b372948f430e369ee9a2321023ab1869e8df49439a92b2d8c39c7f2977d0fee0de65ad277cbbb8627b56ad578acd1005951515151515151515151515a5101155251535a5152000002d10002cd000000011c02d60002cd000123014d012e01520121c11163726561746547656e3041756374696f6e6727465434429b64ac7d34c81edd3c2176b18b11340120e14d105e7d750e38d78cefacb2362a2ba5e679440000014140c44fa86cd5b643e2b2dc9e8a71e9eb58a80bb4384a66a57a6c0c654b625ec7291543d387f7ca72ca29f3c033179a3a0f90616acb9cabf72e6f7394300b9aee892321023ab1869e8df49439a92b2d8c39c7f2977d0fee0de65ad277cbbb8627b56ad578ac')
badblock1550278=binascii.unhexlify(b'0000000074960d5c3f3d245b3aeae96b083cebb323570885e72fb1ff792799792b5e49b87b39ec07685a37c54416fdff7feda498bdfd781d0390c736d768d581c7c3fb7b720d2d5bc6a71700dc667cd1ef7e120fcc829bc363b3af945a5d1fb7eda5e9bd42afa0e001fd4501406110e7c258920e5e6fe2422cfe98809a97cf304676fa3f04d12a557fe19ff2408234d8c6cbefbfb428089ad58e560daaf6ea528b492e1c14d549d4f650677dd840e55dc98ed026261cee322337b990e774496218aa627982005db2feb2a69b388948ba6e6c94994a4af213ad6b93bffaaf34a7c9748d9da1c65c82b803cffad61a40119922ead876f9f078817667289db289870109ca8cb58d0eb8d5266f8d806552723ee5e2f9ed3a67956df52d6cd62576bf35891825c1b828cdb8a02f8bd130e440ea4cc4f605063e73ff1b4628808df03f362c3378cf156a492b4e58713c5eab9d31f87baae32d442c173f84775b0860c2eb4d76dbeab46b19f2f222c913dc464f406dee22985b5c72411040e1812161b8ce40451d371ccb38a9c35dae6c81f704305a97073df9d5d2db79caf14e74b71fd453e95c93d0605644d6edf1d4a10d18aef155210209e7fd41dfb5c2f8dc72eb30358ac100ea8c72da18847befe06eade68cebfcb9210327da12b5c40200e9f65569476bbff2218da4f32548ff43b6387ec1416a231ee8210344925b6126c8ae58a078b5b2ce98de8fff15a22dac6f57ffd3b108c72a0670d121025bdf3f181f53e9696227843950deb72dcd374ded17c057159513c3d0abe20b6421026ce35b29147ad09e4afe4ec4a7319095f08198fa8babbe3c56e970b143528d2221039dafd8571a641058ccc832c5e2111ea39b09c0bde36050914384f7a48bce9bf92103c089d7122b840a4935234e82e26ae5efd0c2acb627239dc9f207311337b6f2c157ae020000dc667cd100000000d1005851515151515151515151515152011757525151525100005a02d300000002cb0002d00002d500014101420130013d0121c11163726561746547656e3041756374696f6e6727465434429b64ac7d34c81edd3c2176b18b11340120e14d105e7d750e38d78cefacb2362a2ba5e67944000001414087364cb96834b474f97aa79ee6464879bd57017751ec48548cf51eb3e4e309f135fd38aa500bc08f25d39d09b37c2ad371f2e5d7150cc0b9186b72cdc17630a62321023ab1869e8df49439a92b2d8c39c7f2977d0fee0de65ad277cbbb8627b56ad578ac')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mainnet", action="store_true", default=False,
                        help="use MainNet instead of the default TestNet")
    parser.add_argument("-c", "--config", action="store", help="Use a specific config file")

    # Where to store stuff
    parser.add_argument("--datadir", action="store",
                        help="Absolute path to use for database directories")

    parser.add_argument("-i", "--input", help="Where the input file lives")

    parser.add_argument("-t", "--totalblocks", help="Total blocks to import", type=int)

    parser.add_argument("-l", "--logevents", help="Log Smart Contract Events", default=False, action="store_true")

    parser.add_argument("-a", "--append", action="store_true", default=False,help="Append to current Block database")

    args = parser.parse_args()

    if args.mainnet and args.config:
        print("Cannot use both --config and --mainnet parameters, please use only one.")
        exit(1)

    # Setting the datadir must come before setting the network, else the wrong path is checked at net setup.
    if args.datadir:
        settings.set_data_dir(args.datadir)

    # Setup depending on command line arguments. By default, the testnet settings are already loaded.
    if args.config:
        settings.setup(args.config)
    elif args.mainnet:
        settings.setup_mainnet()

    if args.logevents:
        settings.log_smart_contract_events = True

    if not args.input:
        raise Exception("Please specify an input path")
    file_path = args.input

    append=False
    start_block = 0

    if args.append:
        append=True

    with open(file_path, 'rb') as file_input:

        total_blocks_available = int.from_bytes(file_input.read(4), 'little')
        total_blocks = total_blocks_available
        if args.totalblocks and args.totalblocks < total_blocks and args.totalblocks > 0:
            total_blocks = args.totalblocks

        target_dir = os.path.join(settings.DATA_DIR_PATH, settings.LEVELDB_PATH)
        notif_target_dir = os.path.join(settings.DATA_DIR_PATH, settings.NOTIFICATION_DB_PATH)


        if append:
            blockchain = LevelDBBlockchain(settings.chain_leveldb_path, skip_header_check=True)
            Blockchain.RegisterBlockchain(blockchain)

            start_block = Blockchain.Default().Height
            print("Starting import at %s " % start_block)
        else:
            print("Will import %s of %s blocks to %s" % (total_blocks, total_blocks_available, target_dir))
            print("This will overwrite any data currently in %s and %s.\nType 'confirm' to continue" % (target_dir, notif_target_dir))

            confirm = prompt("[confirm]> ", is_password=False)
            if not confirm == 'confirm':
                print("Cancelled operation")
                return False

            try:
                if os.path.exists(target_dir):
                    shutil.rmtree(target_dir)
                if os.path.exists(notif_target_dir):
                    shutil.rmtree(notif_target_dir)
            except Exception as e:
                print("Could not remove existing data %s " % e)
                return False

            # Instantiate the blockchain and subscribe to notifications
            blockchain = LevelDBBlockchain(settings.chain_leveldb_path)
            Blockchain.RegisterBlockchain(blockchain)

        chain = Blockchain.Default()

        stream = MemoryStream()
        reader = BinaryReader(stream)
        block = Block()
        length_ba = bytearray(4)

        for index in trange(total_blocks, desc='Importing Blocks', unit=' Block'):
            # set stream data
            file_input.readinto(length_ba)
            block_len = int.from_bytes(length_ba, 'little')

            if index == 1550271:
                reader.stream.write(badblock1550271)
                blah = file_input.read(block_len)
            elif index == 1550275:
                reader.stream.write(badblock1550275)
                blah = file_input.read(block_len)
            elif index == 1550278:
                reader.stream.write(badblock1550278)
                blah = file_input.read(block_len)

            else:
                reader.stream.write(file_input.read(block_len))
            reader.stream.seek(0)

            # get block

            block.DeserializeForImport(reader)

            # add
            if block.Index > start_block:
                chain.AddBlockDirectly(block, addHeader=False)

            # reset blockheader
            block._header = None
            block.__hash = None

            # reset stream
            reader.stream.Cleanup()

    print("Wrote blocks.  Now writing headers")

    chain = Blockchain.Default()
    # reset header hash list
    chain._db.delete(DBPrefix.IX_HeaderHashList)

    total = Blockchain.Default().Height - 1
    header_hash_list = []
    print("loading header hash list... ")
    for index in range(0, total):
        block = chain.GetBlockByHeight(index)
        header_hash_list.append(block.Hash.ToBytes())

    chain._header_index = header_hash_list
    print("storing header hash list...")
    while total - 2000 >= chain._stored_header_count:
        ms = StreamManager.GetStream()
        w = BinaryWriter(ms)
        headers_to_write = chain._header_index[chain._stored_header_count:chain._stored_header_count + 2000]
        w.Write2000256List(headers_to_write)
        out = ms.ToArray()
        StreamManager.ReleaseStream(ms)
        with chain._db.write_batch() as wb:
            wb.put(DBPrefix.IX_HeaderHashList + chain._stored_header_count.to_bytes(4, 'little'), out)

        chain._stored_header_count += 2000

    last_block = chain.GetBlockByHeight(total)
    chain.db.put(DBPrefix.SYS_CurrentHeader, header_hash_list[-1] + last_block.Index.to_bytes(4, 'little'))

    print("Imported %s blocks to %s " % (total_blocks, target_dir))


if __name__ == "__main__":
    main()
