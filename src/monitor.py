from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
import pandas as pd
import yaml
import mlflow

def detect_drift(config_path="configs/config.yaml"):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Load reference (training) and current (production) data
    ref_data = pd.read_parquet(config['data']['processed_path'])
    curr_data = pd.read_csv("data/live/current_data.csv")  # Simulated live data

    # Create drift report
    report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset()
    ])

    report.run(reference_data=ref_data, current_data=curr_data)
    report.save_html(f"{config['monitoring']['report_dir']}/drift_{datetime.now().strftime('%Y%m%d')}.html")

    # Extract drift score
    drift_score = report.as_dict()['metrics'][0]['result']['dataset_drift']
    mlflow.log_metric("data_drift_detected", int(drift_score))

    if drift_score > config['monitoring']['drift_threshold']:
        print("🚨 Drift detected! Triggering retraining...")
        return True
    else:
        print("✅ No significant drift.")
        return False
