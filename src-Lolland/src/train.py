from split_clean import stratified_split, clean

from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score

from sklearn.externals import joblib

def train(X_train, y_train):
    # simple voting classifier
    log_clf = LogisticRegression()
    rnd_clf = RandomForestClassifier()
    svm_clf = SVC()

    voting_clf = VotingClassifier(
        estimators = [
            ('lr', log_clf),
            ('rf', rnd_clf),
            ('svc', svm_clf)], voting='hard'                        
    )
    voting_clf.fit(X_train, y_train)

    joblib.dump(voting_clf, 'Lolland_training_model.pkl')

def main():
    data_prepared, data_labels = clean()
    train(data_prepared, data_labels)

if __name__ == "__main__":
    main()