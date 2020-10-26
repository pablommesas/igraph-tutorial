import os
import numpy as np
import pandas as pd
import igraph

def string_tie_graph_to_dataframe(file, output_dir = None):

    # open the file in Read mode
    f = open(file, "r")

    #if f.mode == 'r':
    #    # use f.read() to read file data and store it in variable `contents`
    #    contents = f.read()
    #    print(contents)

    #df_header = ["node_id", "coordinates", "sum_coverage", "length", "coverage", "parent"]
    df_header = ["name", "start", "end", "sum_coverage", "length", "coverage", "parent"]

    # init node set vars
    #node_vars = np.ndarray(shape = (0, 5))
    node_vars = np.ndarray(shape = (0, 6))

    # init edge set vars
    #edge_vars = np.ndarray(shape = (0, 2))
    edge_vars = np.ndarray(shape = (0, 3))
    #edge_set = {}

    # (if your data is too big) read file line by line, readlines() code will
    # segregate your data in easy to read mode.
    f1 = f.readlines()
    for line in f1:
        #print(ll)
        parse_line = line.split(' ')

        # split `coordinate` into `start` and `end` cols and parse rest of columns
        _node_vars = np.concatenate(([parse_line[0]], parse_line[1][1:-2].split('-'), [xx.split('=')[-1] for xx in parse_line[2:5]]))

        # add node set info
        node_vars = np.append(node_vars, np.array([_node_vars]), axis=0)

        # if there `parent_set` is not empty - attention assuming 'trf=' column is empty!
        parent_set = parse_line[6:-1]
        if len(parent_set) > 0:
            # node_id
            child_id = parse_line[0]

            # add `edge` to edge_set
            for parent_id in parent_set:
                # add: ['parent_id', 'child_id', 'weight'=1] for now
                #edge_vars = np.append(edge_vars, np.array([[parent_id, child_id]]), axis=0)
                edge_vars = np.append(edge_vars, np.array([[parent_id, child_id, 1]]), axis=0)

        #import pdb; pdb.set_trace()
        
    # -----------
    # A. Node Set
    # -----------
    
    node_set_df = pd.DataFrame(node_vars, columns=df_header[0:6])
    #node_set_df
    #node_set_df.shape
    
    # rename: ['source', 'tank'] nodes
    node_set_df.at[0, 'name'] = 'source'
    node_set_df.at[len(node_set_df) - 1, 'name'] = 'tank'

    # -----------
    # B. Edge Set
    # -----------
    
    #edge_set_df = pd.DataFrame(edge_vars, columns=['parent', 'child'])
    edge_set_df = pd.DataFrame(edge_vars, columns=['from', 'to', 'weight'])
    #edge_set_df
    #edge_set_df.shape
    
    # store if necessary
    if not output_dir is None:
        node_set_df.to_csv(os.path.join(output_dir, 'splice_graph.nodes'), sep='\t', header=True, index=False)
        edge_set_df.to_csv(os.path.join(output_dir, 'splice_graph.edges'), sep='\t', header=True, index=False)

    return node_set_df, edge_set_df