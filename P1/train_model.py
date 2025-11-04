"""
Train Scikit-Learn model for sign language recognition
"""
import argparse
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')


class SignLanguageTrainer:
    """Train sign language recognition models"""
    
    def __init__(self, data_path: str):
        """
        Initialize trainer
        
        Args:
            data_path: Path to CSV file with training data
        """
        self.data_path = Path(data_path)
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_data(self):
        """Load and preprocess training data"""
        print(f"Loading data from: {self.data_path}")
        
        df = pd.read_csv(self.data_path)
        
        # Separate features and labels
        label_col = 'label'
        feature_cols = [col for col in df.columns if col.startswith('landmark_')]
        
        X = df[feature_cols].values
        y = df[label_col].values
        
        print(f"Loaded {len(X)} samples with {len(feature_cols)} features")
        print(f"Classes: {np.unique(y)}")
        print(f"Samples per class: {pd.Series(y).value_counts().to_dict()}")
        
        return X, y
    
    def split_data(self, X, y, test_size: float = 0.2, random_state: int = 42):
        """Split data into training and testing sets"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        print(f"\nTraining set: {len(self.X_train)} samples")
        print(f"Test set: {len(self.X_test)} samples")
    
    def train_random_forest(self, n_estimators: int = 100, max_depth: int = None):
        """Train Random Forest classifier"""
        print("\nTraining Random Forest classifier...")
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(self.X_train, self.y_train)
        return self.model
    
    def train_svm(self, kernel: str = 'rbf', C: float = 1.0):
        """Train SVM classifier"""
        print("\nTraining SVM classifier...")
        self.model = SVC(kernel=kernel, C=C, random_state=42)
        self.model.fit(self.X_train, self.y_train)
        return self.model
    
    def train_knn(self, n_neighbors: int = 5):
        """Train K-Nearest Neighbors classifier"""
        print("\nTraining KNN classifier...")
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)
        self.model.fit(self.X_train, self.y_train)
        return self.model
    
    def evaluate(self):
        """Evaluate model performance"""
        if self.model is None:
            print("No model trained yet!")
            return
        
        # Predictions
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        # Calculate accuracies
        train_accuracy = accuracy_score(self.y_train, y_train_pred)
        test_accuracy = accuracy_score(self.y_test, y_test_pred)
        
        print("\n" + "="*50)
        print("MODEL EVALUATION")
        print("="*50)
        print(f"Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
        print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        
        print("\nClassification Report (Test Set):")
        print(classification_report(self.y_test, y_test_pred))
        
        print("\nConfusion Matrix (Test Set):")
        cm = confusion_matrix(self.y_test, y_test_pred)
        print(cm)
        
        return {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'confusion_matrix': cm
        }
    
    def save_model(self, output_path: str):
        """Save trained model to file"""
        if self.model is None:
            print("No model to save!")
            return
        
        output_path = Path(output_path)
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        print(f"\nModel saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Train sign language recognition model")
    parser.add_argument("--data_dir", type=str, default="data",
                       help="Directory containing training data CSV")
    parser.add_argument("--data_file", type=str, default="sign_language_data.csv",
                       help="CSV file with training data")
    parser.add_argument("--output_model", type=str, default="models/sign_language_model.pkl",
                       help="Output path for trained model")
    parser.add_argument("--algorithm", type=str, default="random_forest",
                       choices=["random_forest", "svm", "knn"],
                       help="Machine learning algorithm to use")
    parser.add_argument("--test_size", type=float, default=0.2,
                       help="Test set size ratio")
    
    args = parser.parse_args()
    
    # Construct data path
    data_path = Path(args.data_dir) / args.data_file
    
    if not data_path.exists():
        print(f"Error: Data file not found at {data_path}")
        print("Please run collect_data.py first to create training data.")
        return
    
    # Initialize trainer
    trainer = SignLanguageTrainer(str(data_path))
    
    # Load data
    X, y = trainer.load_data()
    
    # Split data
    trainer.split_data(X, y, test_size=args.test_size)
    
    # Train model
    if args.algorithm == "random_forest":
        trainer.train_random_forest()
    elif args.algorithm == "svm":
        trainer.train_svm()
    elif args.algorithm == "knn":
        trainer.train_knn()
    
    # Evaluate
    trainer.evaluate()
    
    # Save model
    trainer.save_model(args.output_model)


if __name__ == "__main__":
    main()

