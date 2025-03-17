import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Restaurant Sales Analysis')

df = pd.read_csv('balajisalesdata.csv')

st.sidebar.title('Restaurant Sales Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Transaction Type','Daily Sales','Monthly Sales','By Items'])

def load_overall_analysis():
    st.title('Overall Analysis')

    # average amount
    avg_sale = df['transaction_amount'].mean()
    # max amount
    max_sale = df['transaction_amount'].max()
    # min amount
    min_sale = df['transaction_amount'].min()
    total_sale = df['transaction_amount'].sum()
    total_transaction = df['transaction_amount'].count()

    col1,col2,col3,col4,col5=st.columns(5)

    with col1:
        st.metric('Minimum', str(min_sale) + ' INR')
    with col2:
        st.metric('Maximum', str(max_sale) + ' INR')
    with col3:
        st.metric('Average',str(round(avg_sale)) + ' INR')
    with col4:
        st.metric('Total',str(total_sale)+' INR')
    with col5:
        st.metric('Total Transaction',str(total_transaction))


    st.header('MoM Graph')
    fig, ax = plt.subplots()
    sns.histplot(df['transaction_amount'], bins=30, kde=True, ax=ax)
    ax.set_title('Transaction Amount Distribution')
    ax.set_xlabel('Transaction Amount (INR)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    st.subheader('Top-Selling Items')
    top_selling_items = df.groupby('item_name')['transaction_amount'].sum().reset_index().sort_values(by='transaction_amount', ascending=False).head(5)
    fig, ax = plt.subplots()
    sns.barplot(x='transaction_amount', y='item_name', data=top_selling_items, ax=ax)
    ax.set_title('Top 5 Selling Items')
    ax.set_xlabel('Total Sales (INR)')
    ax.set_ylabel('Item Name')
    st.pyplot(fig)


def load_transanction_type_analysis():
    st.title('Transaction Type')

    st.subheader('Transaction Type Distribution')
    transaction_type_distribution = df['transaction_type'].value_counts().reset_index()
    transaction_type_distribution.columns = ['transaction_type', 'count']

    col6, col7 = st.columns(2)
    with col6:
        st.metric('Cash Transactions', transaction_type_distribution.loc[
            transaction_type_distribution['transaction_type'] == 'Cash', 'count'].values[0])
    with col7:
        st.metric('Online Transactions', transaction_type_distribution.loc[
            transaction_type_distribution['transaction_type'] == 'Online', 'count'].values[0])


    st.subheader('Transaction Type Distribution')
    transaction_type_distribution = df['transaction_type'].value_counts().reset_index()
    transaction_type_distribution.columns = ['transaction_type', 'count']
    fig, ax = plt.subplots()
    sns.barplot(x='transaction_type', y='count', data=transaction_type_distribution, ax=ax)
    ax.set_title('Transaction Type Distribution')
    ax.set_xlabel('Transaction Type')
    ax.set_ylabel('Count')
    st.pyplot(fig)

def load_daily_sale_analysis():
    st.title('Average Daily Sales Item-wise')

    # Ensure date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Calculate daily sales per item
    daily_sales_itemwise = df.groupby([df['date'].dt.date, 'item_name'])['transaction_amount'].sum().reset_index()

    # Calculate average daily sales per item
    average_daily_sales_itemwise = daily_sales_itemwise.groupby('item_name')['transaction_amount'].mean().reset_index()
    average_daily_sales_itemwise.columns = ['item_name', 'average_daily_sales']

    st.subheader('Average Daily Sales per Item')
    st.dataframe(average_daily_sales_itemwise)

    fig, ax = plt.subplots()
    sns.barplot(x='average_daily_sales', y='item_name',
                data=average_daily_sales_itemwise.sort_values(by='average_daily_sales', ascending=False), ax=ax)
    ax.set_title('Average Daily Sales per Item')
    ax.set_xlabel('Average Daily Sales (INR)')
    ax.set_ylabel('Item Name')
    st.pyplot(fig)


def load_monthly_sales_analysis():
    st.title('Monthly Sales Distribution')

    # Ensure date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Calculate monthly sales
    monthly_sales = df.resample('M')['transaction_amount'].sum().reset_index()

    st.subheader('Monthly Sales Distribution')
    fig, ax = plt.subplots()
    sns.histplot(monthly_sales['transaction_amount'], bins=12, kde=True, ax=ax)
    ax.set_title('Distribution of Monthly Sales')
    ax.set_xlabel('Total Monthly Sales (INR)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    st.subheader('Total Sales by Month')
    fig, ax = plt.subplots()
    sns.barplot(x=monthly_sales['date'].dt.strftime('%B %Y'), y=monthly_sales['transaction_amount'], ax=ax)
    ax.set_title('Total Sales by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sales (INR)')
    plt.xticks(rotation=45)
    st.pyplot(fig)


def load_item_wise_analysis():
    st.title('Item Wise Report')

    st.subheader('Sales by Item Type')
    sales_by_item_type = df.groupby('item_type')['transaction_amount'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x='item_type', y='transaction_amount', data=sales_by_item_type, ax=ax)
    ax.set_title('Total Sales by Item Type')
    ax.set_xlabel('Item Type')
    ax.set_ylabel('Total Sales (INR)')
    st.pyplot(fig)

    st.subheader('Top-Selling Items')
    top_selling_items = df.groupby('item_name')['transaction_amount'].sum().reset_index().sort_values(by='transaction_amount', ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x='transaction_amount', y='item_name', data=top_selling_items, ax=ax)
    ax.set_title('Top 10 Selling Items')
    ax.set_xlabel('Total Sales (INR)')
    ax.set_ylabel('Item Name')
    st.pyplot(fig)


if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Transaction Type':
    load_transanction_type_analysis()
elif option == 'Daily Sales':
    load_daily_sale_analysis()
elif option == 'Monthly Sales':
    load_monthly_sales_analysis()
elif option == 'By Items':
    load_item_wise_analysis()
