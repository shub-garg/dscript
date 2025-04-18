# dscript

1. Install Script:
```
python3 -m venv /tmp/myenv
source /tmp/myenv/bin/activate
pip install dscript
```

2. Open "/tmp/myenv/lib/python3.11/site-packages/dscript/commands/train.py" and change:
  
model = torch.load(args.checkpoint)  --> model = torch.load(args.checkpoint, weights_only=False)

   
3. Command to create embeddings:

```
dscript embed --seqs subset_sequences1.fasta --outfile train_embeddings.h5
```

4. Command to train dscript with pre-trained weights:
```
dscript train --train train.filtered.tsv --test val.filtered.tsv --embedding sequences.filtered.h5 --checkpoint topsy_turvy_v1.sav --save-prefix topsy_turvy_v2 --num-epochs 20 --batch-size 16 -d 0
```
0 for GPU, -1 for CPU.
