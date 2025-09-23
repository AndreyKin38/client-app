import datetime
import pandas as pd
import dill

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils import resample
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer, make_column_selector


def main():
    class DataResample(BaseEstimator, TransformerMixin):

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            X = X.copy()

            df_min = X[X['TARGET'] == 1]
            df_maj = X[X['TARGET'] == 0]

            df_upsample = resample(df_min, replace=True, n_samples=len(df_maj), random_state=42)

            X = pd.concat([df_maj, df_upsample], ignore_index=True).sample(frac=1.)

            return X

    class RemoveFeatures(BaseEstimator, TransformerMixin):
        COLUMNS_TO_DROP = [
            'SOCSTATUS_PENS_FL',
            'CLOSED_FL',
            'REG_ADDRESS_PROVINCE',
            'POSTAL_ADDRESS_PROVINCE',
            'AGREEMENT_RK'
        ]

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            return X.drop(self.COLUMNS_TO_DROP, axis=1)

    class RemoveOutliers(BaseEstimator, TransformerMixin):

        COLUMNS_FIT = [
            'WORK_TIME',
            'FST_PAYMENT',
            'PERSONAL_INCOME',
            'CREDIT',
            'TERM'
        ]

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            for col in self.COLUMNS_FIT:
                _, high = self.quantile(X[col])
                X.loc[X[col] > high, col] = float(high)
            return X

        @staticmethod
        def quantile(data):
            q25 = data.quantile(0.25)
            q75 = data.quantile(0.75)
            iqr = q75 - q25

            return q25 - iqr * 1.5, q75 + iqr * 1.5

    def column_preprocessor():
        num_features = make_column_selector(dtype_include=['int', 'float'])
        cat_features = make_column_selector(dtype_include=object)

        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
        ])

        column_transformer = ColumnTransformer(transformers=[
            ('numerical', numerical_transformer, num_features),
            ('categorical', categorical_transformer, cat_features)
        ])

        transformer = Pipeline(steps=[
            ('remove_features', RemoveFeatures()),
            ('remove_outliers', RemoveOutliers()),
            ('column_transformer', column_transformer)
        ])

        return transformer

    """CLIENT DF"""
    df = pd.read_csv('client_data/client_dataset.csv')

    train, test = train_test_split(
        df,
        test_size=0.25,
        random_state=42,
        stratify=df['TARGET']
    )

    """RESAMPLE TRAIN DATA"""
    train = DataResample().fit_transform(train)

    x_train = train.drop(['TARGET', 'ID_CLIENT'], axis=1)
    y_train = train['TARGET']

    x_test = test.drop(['TARGET', 'ID_CLIENT'], axis=1)
    y_test = test['TARGET']

    """PREPROCESSOR"""
    preprocessor = column_preprocessor()

    models = [
        LogisticRegression(C=1.1780126533834017, solver='lbfgs', max_iter=1000),
        SVC(C=10, kernel='poly')
    ]

    best_score = 0
    best_pipe = None
    cm = None
    for model in models:
        pipe = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])

        pipe.fit(x_train, y_train)
        prediction = pipe.predict(x_test)
        score = roc_auc_score(y_test, prediction)
        con_matrix = confusion_matrix(y_test, prediction)

        if score > best_score:
            best_score = score
            best_pipe = pipe
            cm = con_matrix

    print(f"roc_auc_score: {best_score}")
    print(f"best_model: {type(best_pipe.named_steps['classifier']).__name__}")
    print(f"confusion_matrix: \n {cm}")

    with open('client_pipe.pkl', 'wb') as file:
        dill.dump({
            'model': best_pipe,
            'metadata': {
                 'name': 'client pipeline',
                 'date': datetime.datetime.now(),
                 'type': type(best_pipe.named_steps['classifier']).__name__,
                 'roc_auc': best_score
            }
        }, file)


def get_model():
    with open('model/client_pipe.pkl', 'rb') as file:
        model = dill.load(file)

    return model


if __name__ == "__main__":
    main()


