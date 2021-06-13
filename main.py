# Main Program

# Import Dependencies
import pandas as pd


# Defining all the functions here

# Sort the Dataframe on the basis of Fee & Weight
# We want to maximise the fee & minimise the weight
# The function takes a dataframe and two features as parameters
def sort_df(df, maxProp, minProp):
    df = df.sort_values([maxProp, minProp], ascending=[False, True]).reset_index(drop=True)
    return df

# Checking if the current Transaction will excede the weight limit
# The function will take the help of 2 global variables - max_weight & current_weight
# The function takes a pandas series as a parameter

def check_weight(x):
    global current_weight
    global max_weight
    if current_weight + x['weight'] <= max_weight:
        return True
    else:
        return False

# Checking if the transaction already exists in the global list
# The function will take the help of 1 global variable - final_list
# the function takes a transaction as a parameter

def check_in_list(x):
    if str(x) in final_list:
        return True
    else:
        return False

# Checking the parents if the exist in the global list - final_txn and if not, adding them to the list(if eligible) before adding the child 
# The function takes a pandas series and the dataframe as parameters

def check_parent(x):
    parents = str(x[3])
    if parents != "nan":
        parent_list = parents.split(";")
        for i in parent_list:
            if(check_in_list(i)):
                continue
            else:
                txnindex = df[df['tx_id'] == i].index.item()
                k = df.loc[txnindex]
                check_add_txn(k)

# Adding the transaction to the final list - final_list while will be used to generate the .txt file
# The function takes a transaction as a parameter

def add_to_list(x):
    global current_weight
    txnID = x[0]
    weight = x[2]
    current_weight += weight
    final_list.append(txnID)

# All the checks before appending the transaction to the list
# The function takes a transaction as a parameter

def check_add_txn(x):
    if(check_weight(x)):
        if(not check_in_list(x)):
            check_parent(x)
            if(check_weight(x)):
                add_to_list(x)  

# Taking the df, sorting it and iterating over each transaction, checking it and adding it to the final list(if eligible)

def mempoolMain(df):
    sortedDF = sort_df(df, "fee", "weight")
    for i in range(len(sortedDF)):
        txnVar = sortedDF.loc[i]
        check_add_txn(txnVar)

# Creating the text file using the final list

def create_textfile(fin_list):
    file = open("block.txt","a")
    for i in fin_list:
        file.write(str(i) + '\n')
    file.close()

# Import CSV into a Dataframe
df  = pd.read_csv("mempool.csv")
#df.head()

# Declaring the global variables
max_weight = 4000000
current_weight = 0
final_list = []

# feeding the dataframe as "data" imported above to the func - mempoolMain and populating the final_list
data = df
mempoolMain(data)

# Creating the text file using final_list
create_textfile(final_list)