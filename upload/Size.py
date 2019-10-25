import pandas as pd
import xgboost

def get_size(x):
    if 0 <= x <= 1:
        return '2XS'
    elif 1 < x <= 3:
        return 'XS'
    elif 3 < x <= 7:
        return 'S'
    elif 7 < x <= 11:
        return 'M'
    elif 11 < x <= 15:
        return 'L'
    elif 15 < x <= 19:
        return 'XL'
    elif 19 < x <= 22:
        return '2XL'
    elif 22 < x:
        return '3XL'
    else:
        return 'none'

def predictSize(bustsize,weight,bodytype,height,age):
    bst = xgboost.Booster({'nthread': 1})
    bst.load_model("upload/model_data/bst.pickle.dat")
    test = {'bust_size': [int(bustsize)], 'weight': [int(weight)],  'body_type': [int(bodytype)],  'height': [int(height)], 'age': [int(age)]}
    test_df = pd.DataFrame.from_dict(test)
    pred = bst.predict(xgboost.DMatrix(test_df))
    size = get_size(pred[0])
    print(size)  
    return size



    

