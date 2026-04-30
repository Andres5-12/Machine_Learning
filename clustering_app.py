import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from flask import render_template, jsonify
import os

# ─── Load dataset once at startup ────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'Dataset.xlsx')

df_raw = pd.read_excel(DATASET_PATH)

# ─── Route handler – called from app.py ──────────────────────────────────────

def clustering_page():
    """Render the Clustering Application page."""
    return render_template('ClusteringApp.html')


def clustering_run():
    """
    Run K-Means clustering on the dataset and return JSON results.
    Called via POST /ClusteringApp/run from the HTML page.
    """
    K = 3

    # 1. Select features
    features = df_raw[['Edad', 'Ingresos']].copy()

    # 2. Preprocessing – StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # 3. Train K-Means
    kmeans = KMeans(
        n_clusters=K,
        init='k-means++',
        n_init=10,
        max_iter=300,
        random_state=42
    )
    kmeans.fit(X_scaled)
    labels = kmeans.labels_
    wcss = float(kmeans.inertia_)

    # 4. Map cluster labels so cluster 0 = lowest income (consistent naming)
    cluster_means = {}
    for k in range(K):
        mask = labels == k
        cluster_means[k] = float(features.loc[mask, 'Ingresos'].mean())
    sorted_keys = sorted(cluster_means, key=lambda k: cluster_means[k])
    remap = {orig: new for new, orig in enumerate(sorted_keys)}
    remapped = [remap[l] for l in labels]

    # 5. Build full table
    df_result = df_raw.copy()
    df_result['Cluster'] = remapped
    cluster_names = ['Low Income', 'Middle Income', 'High Income']
    df_result['ClusterName'] = df_result['Cluster'].map(lambda c: cluster_names[c])

    table_records = df_result[['Dato', 'Edad', 'Ingresos', 'ClusterName']].rename(
        columns={'Dato': 'id', 'Edad': 'age', 'Ingresos': 'income', 'ClusterName': 'cluster'}
    ).to_dict(orient='records')

    # 6. Cluster summary
    summary = []
    for k in range(K):
        mask = df_result['Cluster'] == k
        subset = df_result[mask]
        summary.append({
            'name': cluster_names[k],
            'count': int(mask.sum()),
            'avg_age': round(float(subset['Edad'].mean()), 1),
            'avg_income': round(float(subset['Ingresos'].mean()), 1),
            'min_income': int(subset['Ingresos'].min()),
            'max_income': int(subset['Ingresos'].max()),
        })

    # 7. Centroids in original scale
    centroids_scaled = kmeans.cluster_centers_
    centroids_original = scaler.inverse_transform(centroids_scaled)

    # Remap centroids to match remapped cluster order
    centroids_list = []
    for new_k in range(K):
        orig_k = sorted_keys[new_k]
        c = centroids_original[orig_k]
        centroids_list.append({
            'name': cluster_names[new_k],
            'age': round(float(c[0]), 2),
            'income': round(float(c[1]), 2),
        })

    # 8. Scatter data
    scatter = []
    for k in range(K):
        mask = df_result['Cluster'] == k
        subset = df_result[mask]
        scatter.append({
            'cluster': cluster_names[k],
            'points': [
                {'x': int(row['Edad']), 'y': int(row['Ingresos'])}
                for _, row in subset.iterrows()
            ]
        })

    return jsonify({
        'wcss': round(wcss, 2),
        'table': table_records,
        'summary': summary,
        'centroids': centroids_list,
        'scatter': scatter,
    })