import pandas as pd

from sklearn.utils import resample
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer, make_column_selector


class ClientDataset:

    def __init__(self, path: str, transformer=None):
        self.df = pd.read_csv(path)

        if transformer:
            self.df_transformed = transformer.fit_transform(self.df)

    @property
    def X(self) -> pd.DataFrame:
        return self.df.drop('target', axis=1)

    @property
    def y(self) -> pd.DataFrame:
        return self.df.TARGET

    @property
    def dataset(self) -> pd.DataFrame:
        return self.df

    @property
    def shape(self) -> tuple:
        return self.df.shape

    @property
    def duplicate_sum(self) -> int:
        return self.df.duplicate().sum()

    @property
    def outlier_sum(self) -> pd.Series:
        result = self.df.isna().sum()[self.df.isna().sum() > 0]
        return result

    def __getitem__(self, index: int) -> pd.Series:
        try:
            return self.df_transformed.iloc[index]

        except Exception as e:
            print(e)


class DataResample(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df_min = X[X['target'] == 1]
        df_maj = X[X['target'] == 0]
        df_upsample = resample(df_min, replace=True, n_samples=len(df_maj), random_state=42)

        return pd.concat([df_maj, df_upsample], ignore_index=True).sample(frac=1.)


class DropDuplicatesAndOutliers(DataResample):
    COLUMNS_TO_DROP = [
        'socstatus_pens_fl',
        'closed_fl',
        'reg_address_province',
        'postal_address_province',
        'agreement_rk'
    ]

    COLUMNS_TO_TRANSFORM = [
        'work_time',
        'fst_payment',
        'personal_income',
        'credit',
        'term'
    ]

    def transform(self, X):
        X = X.drop_duplicates()

        X = X.drop(self.COLUMNS_TO_DROP, axis=1)

        for col in self.COLUMNS_TO_TRANSFORM:
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
    cat_features = make_column_selector(dtype_include=['object'])

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

    return column_transformer

