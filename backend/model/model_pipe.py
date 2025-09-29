import datetime
import dill

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from backend.preprocess.preprocessors import ClientDataset, DataResample, DropDuplicatesAndOutliers, column_preprocessor


PATH = '../data/client_dataset.csv'


def main():

    """CLIENT DATASET"""
    dataset = ClientDataset(PATH, DropDuplicatesAndOutliers())

    df = dataset.df_transformed

    X = df.drop('target', axis=1)
    y = df['target']

    train, test = train_test_split(df,
                                   test_size=0.3,
                                   random_state=42,
                                   stratify=df['target'])

    train_resampled = DataResample().fit_transform(train)

    x_train = train_resampled.drop('target', axis=1)
    x_test = test.drop('target', axis=1)

    y_train = train_resampled['target']
    y_test = test['target']

    models = [
        LogisticRegression(C=1.1780126533834017, solver='lbfgs', max_iter=1000),
        SVC(C=10)
    ]

    best_score = 0
    best_model = None
    for model in models:
        pipe = Pipeline(steps=[
            ('preprocessor', column_preprocessor()),
            ('classifier', model)
        ])

        pipe.fit(x_train, y_train)
        prediction = pipe.predict(x_test)
        score = roc_auc_score(y_test, prediction)

        if score > best_score:
            best_score = score
            best_model = pipe

    print(f"roc_auc_score: {best_score}")
    print(f"best_model: {best_model.__class__.__name__}")

    best_model.fit(X, y)
    with open('client_pipe.pkl', 'wb') as file:
        dill.dump({
            'model': best_model,
            'metadata': {
                 'name': 'client pipeline',
                 'date': datetime.datetime.now(),
                 'type': type(best_model.named_steps['classifier']).__name__,
                 'roc_auc': best_score
            }
        }, file)


def get_model():
    with open('backend/model/client_pipe.pkl', 'rb') as file:
        model = dill.load(file)

        return model


if __name__ == "__main__":
    main()


