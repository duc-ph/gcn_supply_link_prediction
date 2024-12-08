#All Completed by Tom

from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
import csv
import numpy as np

#NOTE run from scripts directory!

#read in the results file
print('reading in results file...')
with open('../data/jaccard_results.csv', newline='') as file:
    reader = csv.reader(file)
    jaccard_results = list(reader)

#split the results into probabilites and labels 
print('splitting results into probabalities and labels...')
label = [l[0] for l in jaccard_results]
score = [float(l[1]) for l in jaccard_results]

#compute the ROC AUC
print('computing AUC')
roc_auc_score =  roc_auc_score(label, score)
print(f'ROC_AUC for {len(label)} test edges: {roc_auc_score}')

#plot ROC curve
print('plotting ROC')
y_true = [1 if item == 'True' else 0 for item in label ]
fpr, tpr, thresholds = metrics.roc_curve(y_true, score)
roc_auc = metrics.auc(fpr, tpr)
display = metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc,estimator_name='jaccard coefficient')
display.plot()
plt.show()

#plot confusion matrix
print('plotting confusion matrix')
y_pred = [True if prob >= .5 else False for prob in score]
cm = confusion_matrix(y_true,y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,)
disp.plot()
plt.show()

#print/plot accuracy
print(f'Accuracy for {len(y_pred)} test edges: {accuracy_score(y_true, y_pred)}')


