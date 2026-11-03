import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

def load_and_clean_data(filepath):
    """Loads dataset and ensures correct data types."""
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def generate_seaborn_dashboard(df, output_dir="visualizations"):
    """Creates a 2x2 Seaborn grid with cohesive styling."""
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Sales Performance Dashboard', fontsize=20, fontweight='bold', y=1.02)

    # 1. Box Plot
    sns.boxplot(
        x='Product',
        y='Total_Sales',
        data=df,
        hue='Product',
        ax=axes[0, 0],
        palette='Set2',
        legend=False
    )
    axes[0, 0].set_title('Total Sales Distribution by Product')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # 2. Violin Plot
    sns.violinplot(
        x='Region',
        y='Quantity',
        data=df,
        hue='Region',
        ax=axes[0, 1],
        palette='Pastel1',
        inner='quartile',
        legend=False
    )
    axes[0, 1].set_title('Quantity Distribution by Region')

    # 3. Bar Plot
    sales_by_region = df.groupby('Region')['Total_Sales'].sum().reset_index()
    sns.barplot(
        x='Region',
        y='Total_Sales',
        data=sales_by_region,
        hue='Region',
        ax=axes[1, 0],
        palette='crest',
        legend=False
    )
    axes[1, 0].set_title('Total Sales Revenue by Region')

    # 4. Correlation Heatmap
    numeric_cols = df[['Quantity', 'Price', 'Total_Sales']]
    sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', ax=axes[1, 1], vmin=-1, vmax=1, center=0)
    axes[1, 1].set_title('Correlation Matrix')

    plt.tight_layout()
    plt.savefig(f"{output_dir}/seaborn_grid.png", dpi=300, bbox_inches='tight')
    print("Static dashboard saved to visualizations/seaborn_grid.png")

def generate_plotly_interactive(df, output_dir="visualizations"):
    """Creates a 5th interactive chart with hover data and animations."""
    df_sorted = df.sort_values('Date')
    
    fig = px.scatter(
        df_sorted, 
        x="Price", 
        y="Total_Sales", 
        size="Quantity", 
        color="Product",
        hover_name="Customer_ID",
        hover_data=["Region", "Date"],
        title="Interactive Sales Analysis: Price vs. Total Sales (Bubble Size = Quantity)",
        template="plotly_white"
    )
    
    # Save as interactive HTML
    fig.write_html(f"{output_dir}/interactive_plotly.html")
    print("Interactive dashboard saved to visualizations/interactive_plotly.html")

if __name__ == "__main__":
    # Ensure you are referencing the file verbatim as requested
    DATA_FILE = "sales_data (3).csv"
    
    try:
        sales_df = load_and_clean_data(DATA_FILE)
        generate_seaborn_dashboard(sales_df)
        generate_plotly_interactive(sales_df)
        print("Dashboard generation complete!")
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found. Please ensure it is in the root directory.")