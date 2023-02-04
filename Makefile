test:
	@python3 src/rcgg.py --n_inputs=2 --n_outputs=1 --max_nodes_per_level=2 --max_fan_in=2 --max_fan_out=2 --depth=10
clean:
	@rm -rf *.v
	@rm -rf *.bench
	@rm -rf work
	@rm -rf c*
	@rm -rf *.edgelist
	@rm -rf *.npy
test_no_redundancy:
	@python3 src/rcgg.py --n_inputs=4 --max_nodes_per_level=10 --max_fan_in=2 --depth=10 --no_redundancy
generate_dataset:
	@bash utils/generate_dataset.sh $(NUM_CIRCUITS)
