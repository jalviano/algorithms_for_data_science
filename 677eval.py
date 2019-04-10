# eval.py

import matplotlib.pyplot as plt
import csv


def plot_response_times():
    eval2_response_times = open('../../677/lab-1-jalvin/evaluation/eval2Peer2ResponseTimes.txt')
    e2r = [int(l.split('\n')[0]) for l in eval2_response_times.readlines()]
    eval3_response_times = open('../../677/lab-1-jalvin/evaluation/eval3Peer2ResponseTimes.txt')
    e3r = [int(l.split('\n')[0]) for l in eval3_response_times.readlines()]
    plt.boxplot([e2r, e3r], showfliers=False,
                labels=['4 peers, 2 sellers, 2 neighbors/peer', '4 peers, 1 seller, 3 neighbors/peer'])
    plt.title('Response time evaluation')
    plt.grid(alpha=0.25)
    plt.ylabel('Response time (ms)')
    plt.tight_layout()
    plt.savefig('../../677/lab-1-jalvin/evaluation/response-times.png')
    plt.clf()


def plot_latencies():
    eval1_latencies = open('../../677/lab-1-jalvin/evaluation/eval1Peer2Latencies.csv')
    e1l = [int(l['latency']) for l in csv.DictReader(eval1_latencies) if int(l['peerId']) == 1]
    eval2_latencies = open('../../677/lab-1-jalvin/evaluation/eval2Peer2Latencies.csv')
    e2l = [int(l['latency']) for l in csv.DictReader(eval2_latencies) if int(l['peerId']) == 1]
    plt.boxplot([e1l, e2l], labels=['Network distributed over 2 machines', 'Network distributed over 1 machine'])
    plt.title('Latency evaluation')
    plt.grid(alpha=0.25)
    plt.ylabel('Latency (ms)')
    plt.tight_layout()
    plt.savefig('../../677/lab-1-jalvin/evaluation/latencies.png')
    plt.clf()


if __name__ == '__main__':
    plot_response_times()
    plot_latencies()
