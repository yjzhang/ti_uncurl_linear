
import pandas as pd
import json
import os

import uncurl

import time
checkpoints = {}

## Load data -----------------------------------------------
expression = pd.read_csv("/ti/input/counts.csv", index_col=0)
params = json.load(open("/ti/input/params.json", "r"))

if os.path.exists("/ti/input/start_id.json"):
  start_id = json.load(open("/ti/input/start_id.json"))
else:
  start_id = None
if os.path.exists('/ti/input/groups_n.json'):
    groups_n = json.load(open('/ti/input/groups_n.json'))
    groups_n = groups_n[0]
else:
    groups_n = 0

checkpoints["method_afterpreproc"] = time.time()

## Trajectory inference -----------------------------------

count_data = expression.values
count_data = count_data.T
m, w, ll = uncurl.run_state_estimation(count_data, 2)

checkpoints["method_aftermethod"] = time.time()


# extract the component and use it as pseudotimes
cell_ids = pd.DataFrame({
  "cell_ids":expression.index
})
pseudotime = pd.DataFrame({
  "pseudotime":w[0, :],
  "cell_id":expression.index
})

# use w as dim_red
dimred = pd.DataFrame({
    'cell_id':expression.index,
    'comp_1':w[0,:],
    'comp_2':w[1,:]
})

# groups uses argmax(w)
groupings = pd.DataFrame({
    'cell_id':expression.index,
    'group_id':w.argmax(0)
})

# flip pseudotimes using start_id
if start_id is not None:
  if pseudotime.pseudotime[start_id].mean():
    pseudotime.pseudotime = 1 - pseudotime.pseudotime
# 
# ## Save output ---------------------------------------------
# # output pseudotimes
# output pseudotimes
cell_ids.to_csv("/ti/output/cell_ids.csv", index = False)
pseudotime.to_csv("/ti/output/pseudotime.csv", index = False)
dimred.to_csv('/ti/output/dimred.csv', index=False)
groupings.to_csv('/ti/output/grouping.csv', index=False)

json.dump(checkpoints, open("/ti/output/timings.json", "w"))
