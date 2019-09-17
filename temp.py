path = self.last_node.o['path'].replace('proc', 'mask')
mask_matrix = self.open_file(path)

is_h_energy = lambda d: np.binary_repr(d, width = 8)[5] == '1'

h_energy = np.vectorize(is_h_energy)(mask_matrix)
m = data

for i, j in np.argwhere(h_energy):
    m[max(0, i - up):i, max(0, j - up_thic): j + up_thic] = np.nan
    m[i:i + down, max(0, j - down_thic): j + down_thic] = np.nan
    m[max(0, i - left_thic): i + left_thic, max(0, j - left): j] = np.nan
    m[max(0, i - right_thic): i + right_thic, j: j + right] = np.nan
