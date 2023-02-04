# RCGG - Random Circuit Graph Generator (Structural Version)
Create random combinational circuit using ISCAS bench format.

## Usage
```bash
python3 rcgg.py <options>
```
## Example
```bash
python3 rcgg.py -o prova.bench --n_inputs=2 --n_outputs=2 --max_nodes_per_level=4 --max_fan_in=2 --max_fan_out=3 --depth=5
```

## Generate a dataset
```bash
make generate_dataset NUM_CIRCUITS=XX
```