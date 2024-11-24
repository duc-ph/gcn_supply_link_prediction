from sklearn.metrics import roc_auc_score
import csv

print('reading in results file...')
with open('jaccard_results.csv', newline='') as file:
    reader = csv.reader(file)
    jaccard_results = list(reader)
    
print('splitting results into probabalities and labels...')
label = [l[0] for l in jaccard_results]
score = [float(l[1]) for l in jaccard_results]


print('computing AUC')
roc_auc_score =  roc_auc_score(label, score)
print(f'ROC_AUC for {len(label)} test edges: {roc_auc_score}')


