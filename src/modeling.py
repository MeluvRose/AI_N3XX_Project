import pandas as pd
from sklearn.model_selection import train_test_split
from category_encoders import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.ensemble import RandomForestRegressor

DATA_PATH = "../data/my_data.csv"

# 1. read data completed preprocessing and set target
df = pd.read_csv(DATA_PATH)
target = "proof"

# 2. data divide to 'test/train/split'
train, test = train_test_split(df, test_size=0.2, random_state=2)
train, val = train_test_split(train, test_size=len(test), random_state=2)

features = df.columns.drop(target).tolist()
x_train = train[features]
y_train = train[target]
x_val = val[features]
y_val = val[target]
x_test = test[features]

pipe = make_pipeline(
    OrdinalEncoder(),
    SimpleImputer(),
    RandomForestRegressor(random_state=2)
)

pipe.fit(x_train, y_train)
print(pipe.score(x_val, y_val))
