#!/usr/bin/env python3
import sys

# Configuration
FASTA      = "subset_sequences.fasta"      # Input FASTA file
SPLITS     = ["train.tsv", "val.tsv", "test.tsv"]
THRESHOLD  = 2000                     # Length cutoff
OUT_FASTA  = FASTA.replace('.fasta', '.filtered.fasta')
OUT_SUFFIX = ".filtered.tsv"


def get_long_ids(fasta_path, threshold):
    """
    Scan the FASTA and return a set of all sequence IDs whose lengths exceed the threshold.
    """
    long_ids = set()
    with open(fasta_path) as f:
        seq_id, seq_len = None, 0
        for line in f:
            line = line.rstrip()
            if line.startswith('>'):
                if seq_id and seq_len > threshold:
                    long_ids.add(seq_id)
                seq_id  = line[1:].split()[0]
                seq_len = 0
            else:
                seq_len += len(line)
        # Check the last record
        if seq_id and seq_len > threshold:
            long_ids.add(seq_id)
    return long_ids


def filter_fasta(in_fasta, long_ids, out_fasta):
    """
    Write a new FASTA excluding any records whose ID is in long_ids.
    """
    kept, removed = 0, 0
    write = False
    with open(in_fasta) as src, open(out_fasta, 'w') as dst:
        for line in src:
            if line.startswith('>'):
                seq_id = line[1:].split()[0]
                if seq_id in long_ids:
                    write = False
                    removed += 1
                else:
                    write = True
                    dst.write(line)
                    kept += 1
            else:
                if write:
                    dst.write(line)
    print(f"{in_fasta}: kept {kept} sequences, removed {removed} sequences")


def filter_tsv(in_tsv, long_ids, out_tsv):
    """
    Write a new TSV excluding any pairs involving IDs in long_ids.
    """
    total, kept = 0, 0
    with open(in_tsv) as src, open(out_tsv, 'w') as dst:
        for L in src:
            total += 1
            a, b = L.rstrip().split("\t")[:2]
            if a in long_ids or b in long_ids:
                continue
            dst.write(L)
            kept += 1
    removed = total - kept
    print(f"{in_tsv}: total={total}, kept={kept}, removed={removed}")


if __name__ == "__main__":
    # 1. Identify long sequences
    longs = get_long_ids(FASTA, THRESHOLD)
    print(f"Found {len(longs)} sequences longer than {THRESHOLD} aa:")
    for pid in sorted(longs):
        print(f"  {pid}")
    print()

    # 2. Filter the FASTA itself
    filter_fasta(FASTA, longs, OUT_FASTA)
    print()

    # 3. Filter the train/val/test TSV splits
    for split in SPLITS:
        out = split.replace('.tsv', OUT_SUFFIX)
        filter_tsv(split, longs, out)
    print("\nDone. Use the *_filtered.fasta and *_filtered.tsv files for embedding and training.")
