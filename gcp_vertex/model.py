import argparse
import torch

def main(message):
    print(f"Message: {message}")


def check_cuda():
    # setting device on GPU if available, else CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Using device:', device)
    print()

    #Additional Info when using cuda
    if device.type == 'cuda':
        print(torch.cuda.get_device_name(0))
        print('Memory Usage:')
        print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
        print('Cached:   ', round(torch.cuda.memory_reserved(0)/1024**3,1), 'GB')


parser = argparse.ArgumentParser()
parser.add_argument("--message", type=str, default="Hello World!")
args = parser.parse_args()

main(args.message)
check_cuda()
