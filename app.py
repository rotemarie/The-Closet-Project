import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
from PIL import Image
from collections import Counter


st.set_page_config(page_title='My Closet')
st.header("My Closet")

#LOAD DATAFRAMEs
closet_df = pd.read_excel('ClosetData.xlsx', 'MyCloset')
wore_df = pd.read_excel('ClosetData.xlsx', 'WhatIWoreToday')
wore_sports_df = pd.read_excel('ClosetData.xlsx', 'WhatIWore_Sports')

# VIEW
# item view
st.subheader("Closet View")

#view item by brand
st.subheader("View by Brand")
brands = closet_df['Brand'].unique().tolist()
brand_selection = st.multiselect('Brands:', brands, default=brands)
mask_brands = closet_df['Brand'].isin(brand_selection)
filtered_df_brands = closet_df[mask_brands]
st.dataframe(filtered_df_brands)
num_results_brands = closet_df[mask_brands].shape[0]
st.markdown(f'Available Results:{num_results_brands}*')

#view item by type
st.subheader("View by Type")
types = closet_df['Type'].unique().tolist()
type_selection = st.multiselect('Item Type:', types, default=types)
mask_types = closet_df['Type'].isin(type_selection)
filtered_df_types = closet_df[mask_types]
st.dataframe(filtered_df_types)
num_results_types = closet_df[mask_types].shape[0]
st.markdown(f'Available Results:{num_results_types}*')

st.subheader("Wardrobe Stats")
#VIEW

#ANALYSIS -- ITEM
# initializing counters for each piece of clothing
top_counter = Counter()
bottom_counter = Counter()
shoes_counter = Counter()
sportsbra_counter = Counter()
leggings_counter = Counter()

# saving items in Series
top_items = pd.concat([wore_df['Top'], wore_df['Other top']])
top_items = top_items.dropna()
bottom_items = wore_df['Bottom']
shoes_items = wore_df['Shoes']
sportsbra_items = wore_sports_df['Sports bra']
leggins_items = wore_sports_df['Bottom']

# Counting the items
for item in top_items:
    top_counter[item] += 1
for item in bottom_items:
    bottom_counter[item] +=1
for item in shoes_items:
    shoes_counter[item] += 1
for item in sportsbra_items:
    sportsbra_counter[item] += 1
for item in leggins_items:
    leggings_counter[item] += 1

# Get the most common items in each category
most_common_top = top_counter.most_common(1)[0][0]
most_common_bottom = bottom_counter.most_common(1)[0][0]
most_common_shoes = shoes_counter.most_common(1)[0][0]
most_common_sportsbra = sportsbra_counter.most_common(1)[0][0]
most_common_leggings = leggings_counter.most_common(1)[0][0]

# Create a DataFrame for the most common items and their counts
most_common_data = pd.DataFrame({
    'Clothing Type': ['Top', 'Bottom', 'Shoes', 'Sports Bra', 'Leggings'],
    'Most Common Item': [most_common_top, most_common_bottom, most_common_shoes, most_common_sportsbra, most_common_leggings],
    'Count': [top_counter[most_common_top], bottom_counter[most_common_bottom], shoes_counter[most_common_shoes],
              sportsbra_counter[most_common_sportsbra], leggings_counter[most_common_leggings]]
})

# Create a bar chart
most_worn_chart = px.bar(most_common_data, x='Clothing Type', y='Count', color='Most Common Item',
                         title='Most Worn Item in Every Clothing Category')
st.plotly_chart(most_worn_chart)

# Function to create bar chart
def create_bar_chart(counter, title):
    data = {'Item': list(counter.keys()), 'Count': list(counter.values())}
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Item', y='Count', title=title)
    return fig

# Example usage
st.title("Item Counts")

# Display bar chart for Top items
fig_top = create_bar_chart(top_counter, "Top Items")
st.plotly_chart(fig_top)

# Display bar chart for Bottom items
fig_bottom = create_bar_chart(bottom_counter, "Bottom Items")
st.plotly_chart(fig_bottom)

# Display bar chart for Shoes items
fig_shoes = create_bar_chart(shoes_counter, "Shoes Items")
st.plotly_chart(fig_shoes)

# Display bar chart for Sports Bra items
fig_sportsbra = create_bar_chart(sportsbra_counter, "Sports Bra Items")
st.plotly_chart(fig_sportsbra)

# Display bar chart for Leggings items
fig_leggings = create_bar_chart(leggings_counter, "Leggings Items")
st.plotly_chart(fig_leggings)
#ANALYSIS -- ITEM


#ANALYSIS -- BRAND
brand_counter = Counter()
items_by_brands = closet_df['Brand']
for item in items_by_brands:
    brand_counter[item] += 1
brands_data = pd.DataFrame({
    'Brand': list(brand_counter.keys()),
    'Count': list(brand_counter.values())
})
brands_chart = px.pie(brands_data, names='Brand', values='Count', title='Brands Distribution')
st.plotly_chart(brands_chart)
#ANALYSIS -- BRAND


#NOT WORN ITEMS
all_worn_items = set(top_counter.keys()) | set(bottom_counter.keys()) | set(shoes_counter.keys()) | set(sportsbra_counter.keys()) | set(leggings_counter.keys())
all_items = set(closet_df['Description'])

st.subheader("Items Not Worn")

# Find items in all_items but not in all_worn_items
not_worn = all_items.difference(all_worn_items)
st.write(not_worn)
st.write("Have not worn", len(not_worn), "items out of", len(all_items), "items.")


# .streamlit/secrets.toml
#[connections.gsheets]
#spreadsheet = "https://docs.google.com/spreadsheets/d/1qTCB0JQ2EtG5f_qNbk1ePdv8HNHCyg61lrZIOMR-la4/edit?usp=sharing"
#connections = st.secrets["gsheets"]
#conn = st.connection("gsheets", type=GSheetsConnection)

#df = conn.read()

# Print results.
#for row in df.itertuples():
#    st.write(f"{row.name} has a :{row.pet}:")

#    df = conn.read(
#    worksheet="MyCloset",
#    ttl="10m",
#    usecols=[0, 1],
#    nrows=3,
#)

#st.dataframe(df)'''
