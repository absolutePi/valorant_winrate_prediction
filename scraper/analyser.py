import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def knn_team():
    # Step 1: Load the data from CSV file
    df = pd.read_csv('combined_team_stats.csv')

    # Step 2: Encode the categorical variables
    le_org = LabelEncoder()
    df['org'] = le_org.fit_transform(df['org'])

    le_result = LabelEncoder()
    df['result'] = le_result.fit_transform(df['result'])

    # Step 3: Split the data into features and target
    X = df.drop('result', axis=1)
    y = df['result']

    # Step 4: Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Step 5: Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    # Step 6: Train the KNN model
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)

    # Step 7: Make predictions and evaluate the model
    y_pred = knn.predict(X_test)

    # Step 8: Print the accuracy and classification report
    print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
    print(classification_report(y_test, y_pred, zero_division=1))

    # Optional: Print the actual and predicted results for the test set
    print('Actual:', y_test.values)
    print('Predicted:', y_pred)

def log_reg_team():
    # Step 1: Load the data from CSV file
    df = pd.read_csv('combined_team_stats.csv')

    # Step 2: Encode the categorical variables
    le_org = LabelEncoder()
    df['org'] = le_org.fit_transform(df['org'])

    le_result = LabelEncoder()
    df['result'] = le_result.fit_transform(df['result'])

    # Step 3: Split the data into features and target
    X = df.drop('result', axis=1)
    X = X.drop('org', axis=1)
    y = df['result']

    # Step 4: Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Step 5: Split the data into training and test data sets with stratification (to ensure y value is the same in training and testing sets)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    # Step 6: Train the Logistic Regression model
    log_reg = LogisticRegression()
    log_reg.fit(X_train, y_train)

    # Step 7: Make predictions and evaluate the model
    y_pred = log_reg.predict(X_test)

    # Step 8: Print the accuracy and classification report
    print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
    print(classification_report(y_test, y_pred, zero_division=1))

    # Step 9: Extract the weights (coefficients) of each predictor variable
    coefficients = log_reg.coef_[0]
    features = X.columns
    weights_df = pd.DataFrame({'Feature': features, 'Coefficient': coefficients})

    # Print the coefficients
    print(weights_df)

    # Visualize the coefficients
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Feature', y='Coefficient', data=weights_df)
    plt.title('Logistic Regression Coefficients')
    plt.xticks(rotation=90)
    plt.show()

    # Optional: Visualize the standardized features
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

    # Plot histograms for each standardized feature
    plt.figure(figsize=(12, 8))
    for i, column in enumerate(X_scaled_df.columns, 1):
        plt.subplot(2, 3, i)
        sns.histplot(X_scaled_df[column], kde=True)
        plt.title(f'Distribution of {column}')
    plt.tight_layout()
    plt.show()

    #Plot boxplots for each standardized feature
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=X_scaled_df)
    plt.xticks(rotation=90)
    plt.title('Boxplot of Standardized Features')
    plt.show()

#knn_team()
log_reg_team()
