from argparse import ArgumentParser

from aerpawlib.safetyChecker import SafetyCheckerClient, SafetyCheckerServer

parser = ArgumentParser()
parser.add_argument(
    "--server",
    help="Launch a safety checker server",
    required=False,
    default=False,
)
parser.add_argument(
    "--client",
    help="Launch a safety checker client",
    required=False,
    default=False,
)
parser.add_argument(
    "--vehicle_config",
    help="Path to YAML file containing geofences and vehicle constraints",
    required=False,
)
args = parser.parse_args()

if args.server:
    server = SafetyCheckerServer("geofence_config_copter_test.yaml", server_port=14580)

elif args.client:
    client = SafetyCheckerClient("127.0.0.1", 14580)
    print(client.checkServerStatus())
