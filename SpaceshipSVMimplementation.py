import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.stats import spearmanr
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split


data = pd.read_csv("/home/b3njah/Downloads/machine learning data sets/train.csv")
test1 = pd.read_csv("/home/b3njah/Downloads/machine learning data sets/test.csv")


# convert data into dataframe
test_before = pd.DataFrame(test1)
test = pd.DataFrame(test1)
df = pd.DataFrame(data)

# check data features

print(df.columns)

# check for correlation

print(spearmanr(df["FoodCourt"], df["Transported"]))

# check for null values and drop rows with at least one null values

df['Age'] = df['Age'].fillna(df['Age'].median())
df['HomePlanet'] = df['HomePlanet'].fillna(df['HomePlanet'].mode()[0])
df['CryoSleep'] = df['CryoSleep'].fillna(df['CryoSleep'].mode()[0])
df['Destination'] = df['Destination'].fillna(df['Destination'].mode()[0])
df['VIP'] = df['VIP'].fillna(df['VIP'].mode()[0])
df['RoomService'] = df['RoomService'].fillna(df['RoomService'].mean())
df['FoodCourt'] = df['FoodCourt'].fillna(df['FoodCourt'].mean())
df['ShoppingMall'] = df['ShoppingMall'].fillna(df['ShoppingMall'].mean())
df['VRDeck'] = df['VRDeck'].fillna(df['VRDeck'].mean())

# print("test.isnull().sum()", test.isnull().sum())
# check for null and engineer the features

test['Age'] = test['Age'].fillna(test['Age'].median())
test['HomePlanet'] = test['HomePlanet'].fillna(test['HomePlanet'].mode()[0])
test['CryoSleep'] = test['CryoSleep'].fillna(test['CryoSleep'].mode()[0])
test['Destination'] = test['Destination'].fillna(test['Destination'].mode()[0])
test['VIP'] = test['VIP'].fillna(test['VIP'].mode()[0])
test['RoomService'] = test['RoomService'].fillna(test['RoomService'].mean())
test['FoodCourt'] = test['FoodCourt'].fillna(test['FoodCourt'].mean())
test['ShoppingMall'] = test['ShoppingMall'].fillna(test['ShoppingMall'].mean())
test['VRDeck'] = test['VRDeck'].fillna(test['VRDeck'].mean())

# drop cabin and spa

test = test.drop(['Spa', 'Name', 'Cabin'], axis=1)
df = df.drop(['Spa', 'Name', 'Cabin'], axis=1)

# one hot encode home-planet, cryo-sleep, VIP, Transported

home_planet_test_dummies = pd.get_dummies(test['HomePlanet'])
cryo_sleep_test_dummies = pd.get_dummies(test['CryoSleep'], drop_first=True)
test['CryoSleep'] = cryo_sleep_test_dummies
vip_test_dummies = pd.get_dummies(test['VIP'], drop_first=True)
test['VIP'] = vip_test_dummies
destination_planet_test_dummies = pd.get_dummies(test['Destination'])


home_planet_dummies = pd.get_dummies(df['HomePlanet'])
cryo_sleep_dummies = pd.get_dummies(df['CryoSleep'], drop_first=True)
df['CryoSleep'] = cryo_sleep_dummies
vip_dummies = pd.get_dummies(df['VIP'], drop_first=True)
df['VIP'] = vip_dummies
destination_planet_dummies = pd.get_dummies(df['Destination'])
transported_dummies = pd.get_dummies(df['Transported'], drop_first=True)
df['Transported'] = transported_dummies

# drop Home-planet, destination, passengerId

test = test.drop(['HomePlanet', 'Destination', 'PassengerId'], axis=1)
df = df.drop(['HomePlanet', 'Destination', 'PassengerId'], axis=1)

# join data

test_data = pd.concat([home_planet_test_dummies, destination_planet_test_dummies, test], axis=1)
train_data = pd.concat([home_planet_dummies, destination_planet_dummies, df], axis=1)

print(train_data.columns.size)
print(test_data.columns.size)
# print(test_data['CryoSleep'])

# scale FoodCourt, PassengerId, Age, ShoppingMall, VRDeck, RoomService

Scaler = StandardScaler()
feature_scale = ['FoodCourt', 'Age', 'ShoppingMall', 'VRDeck', 'RoomService']
train_data[feature_scale] = Scaler.fit_transform(train_data[feature_scale])

test_data[feature_scale] = Scaler.fit_transform(test_data[feature_scale])

print(f"test_data.shape {test_data.shape}")
print(f"train_data.shape {train_data.shape}")
# X data and y data
# print(train_data)
X = train_data.drop(['Transported'], axis=1)
y = train_data[['Transported']]

# convert to numpy and split dataset

X = X.to_numpy()
y = y.to_numpy()
test_data = test_data.to_numpy()

# n_samples = len(train_data['Transported'])
# y = y.reshape(n_samples, -1)

y = y.ravel()
print("y shape is :", y.shape)

# split data

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# model creation
model = SVC(C=1000, kernel='rbf', gamma=0.20)

# fit model
model.fit(X, y)

# predict

prediction = model.predict(test_data)

print(model.score(X_test, y_test))

submission = pd.DataFrame({
    'PassengerId': test_before['PassengerId'],
    'Transported': prediction.astype(bool)
})

submission.to_csv("spaceship_submission_v19.csv", index=False)
