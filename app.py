import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('Amazon Sale Report.csv', encoding='unicode_escape')
df.drop(['New', 'PendingS'], axis=1, inplace=True)
df.dropna(inplace=True)
df['ship-postal-code'] = df['ship-postal-code'].astype('int')
df['Date'] = pd.to_datetime(df['Date'])
df.rename(columns={'Qty': 'Quantity'}, inplace=True)
df['Category'] = df['Category'].astype(str)

# Streamlit app starts here
st.title('Amazon Sales Data Analysis')

# Sidebar for state selection
st.sidebar.header('Filter Options')
top_10_states = df['ship-state'].value_counts().head(10).index
selected_state = st.sidebar.selectbox('Select a State to View Sales Data', ['All'] + list(top_10_states))

# Show dataframe
st.subheader('📊 Data Overview')
st.dataframe(df)  # Display the entire dataframe

# Plot data based on state selection
if selected_state == 'All':
    st.subheader('🏆 Distribution of Top 10 States')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df[df['ship-state'].isin(top_10_states)], x='ship-state', ax=ax, palette='Set1')
    ax.set_xlabel('State', fontsize=14)
    ax.set_ylabel('Count', fontsize=14)
    ax.set_title('Top 10 States by Number of Orders', fontsize=18, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.subheader(f'📊 Sales Distribution for {selected_state}')
    fig, ax = plt.subplots(figsize=(10, 6))
    state_data = df[df['ship-state'] == selected_state]
    sns.countplot(data=state_data, x='Category', ax=ax, palette='Set2')
    ax.set_xlabel('Category', fontsize=14)
    ax.set_ylabel('Count', fontsize=14)
    ax.set_title(f'Sales Distribution in {selected_state}', fontsize=18, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Centered "Other Parameters" heading
st.markdown("<h2 style='text-align: center;'>🔍 Other Parameters</h2>", unsafe_allow_html=True)

# Show distribution of Size
st.subheader('📏 Size Distribution')
fig, ax = plt.subplots()
sns.countplot(x='Size', data=df, ax=ax)
for bars in ax.containers:
    ax.bar_label(bars)
st.pyplot(fig)

# Group By Size
st.subheader('📊 Quantity by Size')
fig, ax = plt.subplots()
S_Qty = df.groupby(['Size'], as_index=False)['Quantity'].sum().sort_values(by='Quantity', ascending=False)
sns.barplot(x='Size', y='Quantity', data=S_Qty, ax=ax)
st.pyplot(fig)

# Courier Status
st.subheader('🚚 Courier Status Distribution')
fig, ax = plt.subplots()
sns.countplot(x='Courier Status', data=df, hue='Status', ax=ax)
st.pyplot(fig)

# Histogram of Size
st.subheader('📊 Size Histogram')
fig, ax = plt.subplots()
df['Size'].hist(ax=ax, edgecolor='black')
st.pyplot(fig)

# Category Distribution
st.subheader('📈 Category Distribution')
fig, ax = plt.subplots()
column_data = df['Category']
ax.hist(column_data, bins=20, edgecolor='black')
plt.xticks(rotation=90)
st.pyplot(fig)

# B2B Distribution
st.subheader('🏢 B2B Distribution')
fig, ax = plt.subplots(figsize=(8, 8))
B2B_check = df['B2B'].value_counts()
ax.pie(B2B_check, labels=B2B_check.index, autopct='%1.1f%%', colors=sns.color_palette('Set3'))
st.pyplot(fig)

# Scatter Plot
st.subheader('🔍 Scatter Plot of Category vs Size')
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df['Category'], df['Size'])
ax.set_xlabel("Category")
ax.set_ylabel("Size")
ax.set_title("Scatter Plot")
st.pyplot(fig)

# Conclusion
st.subheader('📚 Conclusion')
st.markdown("""
- The business has a significant customer base in the Maharashtra state.
- The business mainly serves retailers.
- Orders are primarily fulfilled through Amazon.
- There is a high demand for T-Shirts.
- M-size is the preferred choice among buyers.
""")
