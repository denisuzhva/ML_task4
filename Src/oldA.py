## Update A

# A(i, k) <- min{0, R(k, k) + sum_{j: j \neq i, j \neq k} max{0, R(j, k)}} 
# A(k, k) <- sum_{j: j \neq k} max{0, R(j, k)}
def update_a(r_mat, a_old, damping):
    
    # aux.
    nodes_arr = np.arange(0, NODES)
    r_diag = r_mat.diagonal()
    
    # clean R from negative elements
    r_pos = sp.lil_matrix(r_mat, dtype=DTYPE)
    r_pos[r_pos < 0] = 0
    
    # do not change R(k, k)
    r_pos[nodes_arr, nodes_arr] = r_diag
    r_pos = r_pos.tocsr()
    r_pos.eliminate_zeros()
    
    # for now, just calculate a sum over all rows...
    r_pos_sum = np.asarray(r_pos.sum(axis=0)).flatten()
    
    # rearrange sum values and place them inside a
    aa_mat = sp.lil_matrix((NODES, NODES), dtype=DTYPE)
    r_pos_sum_full = r_pos_sum[s_keys[1]]
    aa_mat[s_keys[0], s_keys[1]] = r_pos_sum_full
    aa_mat = aa_mat.tocsr()
    
    # subtract where j = i
    aa_mat = aa_mat - r_pos
    
    # for A(i, k) where i \neq k remove positive elements
    a_mat = sp.lil_matrix(aa_mat, dtype=DTYPE)
    a_mat[a_mat > 0] = 0
    a_mat[nodes_arr, nodes_arr] = aa_mat[nodes_arr, nodes_arr]
    a_mat = a_mat.tocsr()
    a_mat.eliminate_zeros()
    
    print('A max %.2f' % a_mat.max())
    print('A min %.2f' % a_mat.min())
    
    # apply damping
    a_mat = damping * a_old + (1 - damping) * a_mat
   
    return a_mat