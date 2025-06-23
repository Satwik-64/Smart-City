# Placeholder for anomaly_file_checker.py
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AnomalyChecker:
    def __init__(self):
        self.anomaly_methods = {
            'z_score': self._z_score_anomalies,
            'iqr': self._iqr_anomalies,
            'isolation_forest': self._isolation_forest_anomalies
        }
    
    def detect_anomalies(self, df: pd.DataFrame, method: str = 'z_score') -> Dict[str, Any]:
        """Detect anomalies in the uploaded KPI data"""
        try:
            if df.empty:
                raise ValueError("Empty dataframe provided")
            
            # Get numeric columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if not numeric_columns:
                raise ValueError("No numeric columns found for anomaly detection")
            
            results = {
                "summary": {
                    "total_records": len(df),
                    "metrics_analyzed": numeric_columns,
                    "anomaly_method": method,
                    "detection_timestamp": datetime.now().isoformat()
                },
                "anomalies_by_metric": {},
                "anomaly_summary": {},
                "recommendations": []
            }
            
            total_anomalies = 0
            
            for column in numeric_columns:
                try:
                    anomaly_result = self._detect_column_anomalies(df, column, method)
                    results["anomalies_by_metric"][column] = anomaly_result
                    
                    anomaly_count = len(anomaly_result["anomaly_indices"])
                    total_anomalies += anomaly_count
                    
                    results["anomaly_summary"][column] = {
                        "anomaly_count": anomaly_count,
                        "anomaly_percentage": (anomaly_count / len(df)) * 100,
                        "severity": self._classify_anomaly_severity(anomaly_count, len(df)),
                        "most_extreme_value": anomaly_result.get("most_extreme_value")
                    }
                    
                except Exception as e:
                    logger.warning(f"Failed to detect anomalies in {column}: {e}")
                    continue
            
            results["summary"]["total_anomalies"] = total_anomalies
            results["summary"]["overall_anomaly_rate"] = (total_anomalies / len(df)) * 100
            
            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            raise
    
    def _detect_column_anomalies(self, df: pd.DataFrame, column: str, method: str) -> Dict[str, Any]:
        """Detect anomalies in a single column"""
        data = df[column].dropna()
        
        if len(data) < 5:
            return {
                "anomaly_indices": [],
                "anomaly_values": [],
                "thresholds": {},
                "statistics": {},
                "error": "Insufficient data points"
            }
        
        # Use the specified method
        if method in self.anomaly_methods:
            anomaly_indices, thresholds = self.anomaly_methods[method](data)
        else:
            anomaly_indices, thresholds = self._z_score_anomalies(data)
        
        anomaly_values = data.iloc[anomaly_indices].tolist()
        
        # Calculate basic statistics
        statistics = {
            "mean": float(data.mean()),
            "std": float(data.std()),
            "min": float(data.min()),
            "max": float(data.max()),
            "q25": float(data.quantile(0.25)),
            "q50": float(data.quantile(0.50)),
            "q75": float(data.quantile(0.75))
        }
        
        # Find most extreme anomaly
        most_extreme_value = None
        if anomaly_values:
            mean_val = statistics["mean"]
            most_extreme_value = max(anomaly_values, key=lambda x: abs(x - mean_val))
        
        return {
            "anomaly_indices": anomaly_indices,
            "anomaly_values": anomaly_values,
            "thresholds": thresholds,
            "statistics": statistics,
            "most_extreme_value": most_extreme_value
        }
    
    def _z_score_anomalies(self, data: pd.Series, threshold: float = 3.0) -> Tuple[List[int], Dict]:
        """Detect anomalies using Z-score method"""
        z_scores = np.abs(stats.zscore(data))
        anomaly_indices = np.where(z_scores > threshold)[0].tolist()
        
        thresholds = {
            "method": "z_score",
            "threshold": threshold,
            "upper_bound": float(data.mean() + threshold * data.std()),
            "lower_bound": float(data.mean() - threshold * data.std())
        }
        
        return anomaly_indices, thresholds
    
    def _iqr_anomalies(self, data: pd.Series, multiplier: float = 1.5) -> Tuple[List[int], Dict]:
        """Detect anomalies using Interquartile Range (IQR) method"""
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        anomaly_indices = data[(data < lower_bound) | (data > upper_bound)].index.tolist()
        
        thresholds = {
            "method": "iqr",
            "multiplier": multiplier,
            "upper_bound": float(upper_bound),
            "lower_bound": float(lower_bound),
            "Q1": float(Q1),
            "Q3": float(Q3),
            "IQR": float(IQR)
        }
        
        return anomaly_indices, thresholds
    
    def _isolation_forest_anomalies(self, data: pd.Series, contamination: float = 0.1) -> Tuple[List[int], Dict]:
        """Detect anomalies using Isolation Forest (simplified version)"""
        try:
            from sklearn.ensemble import IsolationForest
            
            # Reshape data for sklearn
            X = data.values.reshape(-1, 1)
            
            # Fit Isolation Forest
            clf = IsolationForest(contamination=contamination, random_state=42)
            outlier_labels = clf.fit_predict(X)
            
            # Get anomaly indices
            anomaly_indices = np.where(outlier_labels == -1)[0].tolist()
            
            thresholds = {
                "method": "isolation_forest",
                "contamination": contamination,
                "anomaly_score_threshold": "adaptive"
            }
            
            return anomaly_indices, thresholds
            
        except ImportError:
            logger.warning("scikit-learn not available, falling back to Z-score method")
            return self._z_score_anomalies(data)
    
    def _classify_anomaly_severity(self, anomaly_count: int, total_count: int) -> str:
        """Classify the severity of anomalies"""
        rate = (anomaly_count / total_count) * 100
        
        if rate > 10:
            return "high"
        elif rate > 5:
            return "medium"
        elif rate > 1:
            return "low"
        else:
            return "minimal"
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on anomaly detection results"""
        recommendations = []
        
        try:
            overall_rate = results["summary"]["overall_anomaly_rate"]
            
            if overall_rate > 15:
                recommendations.append("High anomaly rate detected - investigate data collection processes")
            elif overall_rate > 10:
                recommendations.append("Moderate anomaly rate - consider reviewing data quality controls")
            
            # Metric-specific recommendations
            for metric, summary in results["anomaly_summary"].items():
                severity = summary["severity"]
                metric_name = metric.replace('_', ' ').title()
                
                if severity == "high":
                    recommendations.append(f"{metric_name}: High anomaly rate - urgent investigation required")
                elif severity == "medium":
                    recommendations.append(f"{metric_name}: Monitor closely for unusual patterns")
                elif summary["anomaly_count"] > 0:
                    recommendations.append(f"{metric_name}: Minor anomalies detected - routine review recommended")
            
            # General recommendations
            if not recommendations:
                recommendations.append("Data quality appears good - no significant anomalies detected")
            
            recommendations.append("Consider implementing automated anomaly alerts for real-time monitoring")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append("Unable to generate specific recommendations")
        
        return recommendations
    
    def get_anomaly_report(self, results: Dict[str, Any]) -> str:
        """Generate a text report of anomaly detection results"""
        try:
            report = []
            report.append("ANOMALY DETECTION REPORT")
            report.append("=" * 40)
            report.append("")
            
            summary = results["summary"]
            report.append(f"Total Records Analyzed: {summary['total_records']}")
            report.append(f"Total Anomalies Found: {summary['total_anomalies']}")
            report.append(f"Overall Anomaly Rate: {summary['overall_anomaly_rate']:.2f}%")
            report.append(f"Detection Method: {summary['anomaly_method']}")
            report.append("")
            
            report.append("ANOMALIES BY METRIC:")
            report.append("-" * 20)
            
            for metric, summary in results["anomaly_summary"].items():
                metric_name = metric.replace('_', ' ').title()
                report.append(f"{metric_name}:")
                report.append(f"  - Count: {summary['anomaly_count']}")
                report.append(f"  - Rate: {summary['anomaly_percentage']:.2f}%")
                report.append(f"  - Severity: {summary['severity']}")
                report.append("")
            
            report.append("RECOMMENDATIONS:")
            report.append("-" * 15)
            for i, rec in enumerate(results["recommendations"], 1):
                report.append(f"{i}. {rec}")
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"Error generating anomaly report: {e}")
            return "Error generating report"