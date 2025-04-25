import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    labels = list()
    row_count = 0
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            row_count += 1
    evidence = [[0 for i in range(17)] for j in range(row_count)]
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        
        month_to_number = {
            "Jan": 0,
            "Feb": 1,
            "Mar": 2,
            "Apr": 3,
            "May": 4,
            "June": 5,
            "Jul": 6,
            "Aug": 7,
            "Sep": 8,
            "Oct": 9,
            "Nov": 10,
            "Dec": 11
        }
        count = 0
        for row in reader:
            evidence_to_add = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            #append the first 10 Columns
            evidence_to_add[0] = (int(row[0]))
            evidence_to_add[1] = (float(row[1]))
            evidence_to_add[2] = (int(row[2]))
            evidence_to_add[3] = (float(row[3]))
            evidence_to_add[4] = (int(row[4]))
            evidence_to_add[5] = (float(row[5]))
            evidence_to_add[6] = (float(row[6]))
            evidence_to_add[7] = (float(row[7]))
            evidence_to_add[8] = (float(row[8]))
            evidence_to_add[9] = (float(row[9]))
            
            #append the month
            evidence_to_add[10] = (month_to_number.get(row[10]))
            
            #append the next 4 columns after month
            for i in range(11,15):
                evidence_to_add[i] = (int(row[i]))

            #check weather the person is a returning visitor or not
            if row[15] == "Returning_Visitor":
                evidence_to_add[15] = 1
            else:
                evidence_to_add[15] = 0
            
            #check for weekend
            if row[16] == "TRUE":
                evidence_to_add[16] = 1
            else:
                evidence_to_add[16] = 0
            
            if row[17] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)
            evidence[count] = evidence_to_add
            count += 1
    return (evidence, labels)        
    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive_count = 0
    true_positive_count = 0
    negative_count = 0
    true_negative_count = 0
    for i in range(len(labels)):
        if labels[i] == 1:#positive
            positive_count += 1
            if labels[i] == predictions[i]:
                true_positive_count += 1
        elif labels[i] == 0:#not positive
            negative_count += 1
            if labels[i] == predictions[i]:
                true_negative_count += 1
    
    sensitivity = true_positive_count/positive_count
    specificity = true_negative_count/negative_count
    return (sensitivity, specificity)
    raise NotImplementedError


if __name__ == "__main__":
    main()
