import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def read_data() -> pd.DataFrame:
    """
    Reads data from an Excel file and returns a pandas DataFrame.
    """
    # Read the Excel file into a DataFrame
    df_can = pd.read_excel('https://s3.hothienlac.com/yomitoon/Canada.xlsx',
                           sheet_name='Canada by Citizenship',
                           skiprows=range(20),)
    
    return df_can

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the dataset
    """
    df = df.copy()

    # Rename columns
    df.rename(
        columns={
            'OdName': 'Country',
            'AreaName': 'Continent',
            'RegName': 'Region'
        },
        inplace=True
    )
    return df

def add_total_column(df: pd.DataFrame, years: list) -> pd.DataFrame:
    """Add Total immigration column"""
    df['Total'] = df[years].sum(axis=1)
    return df

def clean_non_country_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows that are not actual countries
    """
    EXCLUDE_ROWS = ['Total', 'Unknown']
    return df.drop(index=EXCLUDE_ROWS, errors='ignore')


# Exploration & Indexing
def explore_basic_info(df: pd.DataFrame) -> None:
    print(df.head(2))
    print("=" * 100)
    print(df.columns)
    print("=" * 100)
    print(df[['Total']].head())
    print(df.isnull().sum())
    print(df.describe())


def set_country_index(df: pd.DataFrame) -> pd.DataFrame:
    df.set_index('Country', inplace=True)
    df.index.name = None
    return df


def demonstrate_selection(df: pd.DataFrame) -> None:
    print(df.loc['Japan'])
    print(df.iloc[87])
    print(df[df.index == 'Japan'].T.squeeze())
    print(df.loc['Japan', 2013])
    print(df.iloc[87, 36])
    print(df.loc['Japan', [1980, 1981, 1982, 1983, 1984]])
    print(df.iloc[87, [3, 4, 5, 6, 7]])


def convert_years_to_string(df: pd.DataFrame) -> list:
    df.columns = list(map(str, df.columns))
    return list(map(str, range(1980, 2014)))


def filter_examples(df: pd.DataFrame) -> None:
    condition = df['Continent'] == 'Asia'
    print(condition)

    df_asia = df[condition]
    df_south_asia = df[(df['Continent'] == 'Asia') & (df['Region'] == 'Southern Asia')]

    print('data dimensions:', df.shape)
    print(df.columns)
    print(df.head(2))



# Visualization Functionns
def plot_haiti(df: pd.DataFrame, years: list) -> None:
    mpl.style.use(['ggplot'])

    haiti = df.loc['Haiti', years]
    haiti.index = haiti.index.map(int)

    haiti.plot(kind='line')
    plt.title('Immigration from Haiti')
    plt.ylabel('Number of Immigrants')
    plt.xlabel('Years')
    plt.text(2000, 6000, '2010 Earthquake')
    plt.show()


def plot_china_india(df: pd.DataFrame, years: list) -> None:
    df_ci = df.loc[['India', 'China'], years].transpose()
    df_ci.index = df_ci.index.map(int)

    df_ci.plot(kind='bar')
    plt.title('Immigrants from China and India')
    plt.ylabel('Number of Immigrants')
    plt.xlabel('Years')
    plt.show()


def plot_top5(df: pd.DataFrame, years: list) -> None:
    df.sort_values(by='Total', ascending=False, inplace=True)

    df_top5 = df.head(5)[years].transpose()
    df_top5.index = df_top5.index.map(int)

    df_top5.plot(kind='line', figsize=(14, 8))
    plt.title('Immigration Trend of Top 5 Countries')
    plt.ylabel('Number of Immigrants')
    plt.xlabel('Years')
    plt.show()

def main():
    print("Data loaded successfully!")
    print("=" * 100)

    df_can = read_data()
    df_can = preprocess_data(df_can)

    years_int = list(range(1980, 2014))
    df_can = add_total_column(df_can, years_int)

    explore_basic_info(df_can)

    print(df_can.Country)
    print(df_can[['Country', 1980, 1981, 1982, 1983, 1984, 1985]])

    df_can = set_country_index(df_can)
    demonstrate_selection(df_can)

    df_can = clean_non_country_rows(df_can)

    years = convert_years_to_string(df_can)
    filter_examples(df_can)

    plot_haiti(df_can, years)
    plot_china_india(df_can, years)
    plot_top5(df_can, years)

if __name__ == "__main__":  
    main()
