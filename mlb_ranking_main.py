'''
The goal is to develop a power rankings for MLB.

Roughly based on ELO? Idk.
'''
import argparse

def read_game_data(filename):

    all_rows = []

    with open(filename, 'r') as f:
        for row in f:
            split_row = row.split(",")

            all_rows.append(split_row)

    return all_rows

def main():
    raw_data = read_game_data('data/GL2017.txt')
    for i in range(2):
        print raw_data[i], len(raw_data[i])

    #blah blah

if __name__ == '__main__':
    main()