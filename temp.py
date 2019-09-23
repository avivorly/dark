for computed_output in self.computed_outputs:
    next_node.o[computed_output['name']['value']] = computed_output['value']['value']