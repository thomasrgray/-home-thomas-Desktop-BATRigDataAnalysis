import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ranksums

# Define the data for each animal
data = {
    'Pre_Carvone': [16.6, 13.6, 7, 11.3],
    'Post_Carvone': [31.9, 20.7, 16.9, 27],
    'Pre_Cis': [19.1, 20.7, 17.9, 25.4],
    'Post_Cis': [23.8, 17.4, 13.8, 22],
    'Pre_Ethyl': [24.4, 8.2, 30.6],
    'Post_Ethyl': [21.8, 12.6, 35.8],
    'Pre_Citral': [19.7, 15.2, 5.8],
    'Post_Citral': [17.7, 14.2, 12.16]
}

# Create two DataFrames, one for Ethyl and Citral, and another for Carvone and Cis
df_panel_a = pd.DataFrame({
    'Pre_Ethyl': data['Pre_Ethyl'],
    'Post_Ethyl': data['Post_Ethyl'],
    'Pre_Citral': data['Pre_Citral'],
    'Post_Citral': data['Post_Citral']
})

df_panel_b = pd.DataFrame({
    'Pre_Carvone': data['Pre_Carvone'],
    'Post_Carvone': data['Post_Carvone'],
    'Pre_Cis': data['Pre_Cis'],
    'Post_Cis': data['Post_Cis']
})

# Melt the DataFrames to long format
melted_df_panel_a = pd.melt(df_panel_a, var_name='Odor', value_name='Average Licks')
melted_df_panel_b = pd.melt(df_panel_b, var_name='Odor', value_name='Average Licks')

# Separate the 'Pre' and 'Post' test conditions
melted_df_panel_a['Test'] = melted_df_panel_a['Odor'].str.split('_').str[0]
melted_df_panel_a['Odor'] = melted_df_panel_a['Odor'].str.split('_').str[1]

melted_df_panel_b['Test'] = melted_df_panel_b['Odor'].str.split('_').str[0]
melted_df_panel_b['Odor'] = melted_df_panel_b['Odor'].str.split('_').str[1]

# Create two subplots (panels) with custom width ratios
fig, axes = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [1, 1]})

# Create the bar plots with strip plots for panel a
sns.barplot(
    x='Odor',
    y='Average Licks',
    hue='Test',
    data=melted_df_panel_a,
    ci='sd',
    edgecolor='black',
    errcolor='black',
    errwidth=1.5,
    capsize=0.1,
    ax=axes[0],
    alpha=0.5
)

sns.stripplot(
    x='Odor',
    y='Average Licks',
    hue='Test',
    data=melted_df_panel_a,
    order=['Ethyl', 'Citral'],
    palette=sns.color_palette()[:2],
    dodge=True,
    alpha=1.0,
    ax=axes[0],
    jitter=True,
    legend=False  # Remove the legend for stripplot
)

# Create the bar plots with strip plots for panel b
sns.barplot(
    x='Odor',
    y='Average Licks',
    hue='Test',
    data=melted_df_panel_b,
    ci='sd',
    edgecolor='black',
    errcolor='black',
    errwidth=1.5,
    capsize=0.1,
    ax=axes[1],
    alpha=0.5,
    palette=['lightcoral', 'skyblue']  # Custom colors for panel b bars
)

sns.stripplot(
    x='Odor',
    y='Average Licks',
    hue='Test',
    data=melted_df_panel_b,
    order=['Carvone', 'Cis'],
    palette=['darkred', 'deepskyblue'],  # Custom colors for panel b dots
    dodge=True,
    alpha=1.0,
    ax=axes[1],
    jitter=True,
    legend=False  # Remove the legend for stripplot
)

# Adjust legends and plot titles for both panels
axes[0].set_title('Average Licks for Ethyl and Citral')
axes[1].set_title('Average Licks for Carvone and Cis')

# Manually create custom legends on the right side
axes[0].legend(title='Test', loc='upper right')
axes[1].legend(title='Test', loc='upper right')

# Set the spacing between the plots
plt.subplots_adjust(wspace=0.4)

# Fine-tune the layout to avoid overlapping text
fig.tight_layout(rect=[0, 0, 0.7, 0.7])  # The right margin of the figure is set to 0.95

# Perform Wilcoxon rank-sum test
ethyl_pre = melted_df_panel_a[melted_df_panel_a['Odor'] == 'Ethyl'][melted_df_panel_a['Test'] == 'Pre']['Average Licks']
ethyl_post = melted_df_panel_a[melted_df_panel_a['Odor'] == 'Ethyl'][melted_df_panel_a['Test'] == 'Post']['Average Licks']

citral_pre = melted_df_panel_a[melted_df_panel_a['Odor'] == 'Citral'][melted_df_panel_a['Test'] == 'Pre']['Average Licks']
citral_post = melted_df_panel_a[melted_df_panel_a['Odor'] == 'Citral'][melted_df_panel_a['Test'] == 'Post']['Average Licks']

carvone_pre = melted_df_panel_b[melted_df_panel_b['Odor'] == 'Carvone'][melted_df_panel_b['Test'] == 'Pre']['Average Licks']
carvone_post = melted_df_panel_b[melted_df_panel_b['Odor'] == 'Carvone'][melted_df_panel_b['Test'] == 'Post']['Average Licks']

cis_pre = melted_df_panel_b[melted_df_panel_b['Odor'] == 'Cis'][melted_df_panel_b['Test'] == 'Pre']['Average Licks']
cis_post = melted_df_panel_b[melted_df_panel_b['Odor'] == 'Cis'][melted_df_panel_b['Test'] == 'Post']['Average Licks']

# Perform Wilcoxon rank-sum test
ethyl_wilcoxon = ranksums(ethyl_pre, ethyl_post)
citral_wilcoxon = ranksums(citral_pre, citral_post)
carvone_wilcoxon = ranksums(carvone_pre, carvone_post)
cis_wilcoxon = ranksums(cis_pre, cis_post)

# Convert the test results to text annotations
def add_test_results(ax, wilcoxon_result, x_coord, y_coord):
    test_statistic = wilcoxon_result.statistic
    p_value = wilcoxon_result.pvalue
    significance = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else ''
    
    annotation_text = f"{significance}"
    ax.annotate(annotation_text, xy=(x_coord, y_coord), xycoords='axes fraction',
                xytext=(5, 5), textcoords='offset points',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

# Add test results as annotations below each data point
add_test_results(axes[0], ethyl_wilcoxon, 0.2, 1.1)
add_test_results(axes[0], citral_wilcoxon, .7, 1.1)
add_test_results(axes[1], carvone_wilcoxon, 0.2, .9)
add_test_results(axes[1], cis_wilcoxon, .7, 1.1)

# Show the plots
plt.show()