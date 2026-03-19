import pandas as pd


# Loading data from a CSV file
def load_data(file_path):
    """Load data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")

        # Renaming columns for easier access (Code was buggy at first without this)
        rename_columns = {
            "Protein(g)": "Protein",
            "Carbs(g)": "Carbs",
            "Fat(g)": "Fat",
            "Cuisine_type": "Cuisine",
        }
        data = data.rename(columns=rename_columns)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Cleaning the data by removing rows with missing values in key columns
def clean_data(data):
    """Remove rows with missing macro values."""
    data = data.dropna(subset=["Protein", "Carbs", "Fat", "Diet_type"])
    return data

# Calculating average macros by diet type
def avg_macros_by_diet(data):
    """Calculate average macros by diet type."""
    avg_macros = data.groupby("Diet_type")[["Protein", "Carbs", "Fat"]].mean().reset_index()
    return avg_macros

# Getting top 5 foods by protein content for each diet type
def top_5_protein_by_diet(data):
    """Get top 5 foods by protein content for each diet type."""
    top_protein = data.sort_values(by="Protein", ascending=False).groupby("Diet_type").head(5).reset_index(drop=True)
    return top_protein

# Identifying the diet type with the highest average protein content
def diet_with_most_protein(data):
    """Identify the diet type with the highest average protein content."""
    avg_protein = data.groupby("Diet_type")["Protein"].mean()
    top_diet = avg_protein.idxmax()
    return top_diet, avg_protein[top_diet]


def most_common_cuisine_by_diet(data):
    """Identify the most common cuisine type for each diet type."""
    common_cuisine = data.groupby("Diet_type")["Cuisine"].agg(lambda x: x.mode()[0] if not x.mode().empty else "Unknown").reset_index()
    return common_cuisine