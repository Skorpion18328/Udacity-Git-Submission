import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Generate Month and Day-of-Week dictionaries so user can type in regular human text instead of trying to figure out the right numbers
month_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, '': -1}
day_dict = {'su': 6, 'm': 0, 'tu': 1, 'w': 2, 'th': 3, 'f': 4, 'sa': 5, '': -1}
num_month_dict = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june'}
num_day_dict = {6: 'sunday', 0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) desired_city - name of the city to analyze
  ADDED (str) desired_sort - Whether the user wants to sort by month, day of week, both, or none
        (str) desired_month - name of the month to filter by, or "all" to apply no month filter
        (str) desired_day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    desired_city, desired_sort, desired_month, desired_day = ['','','','']

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while desired_city == '':
        desired_city = input('Would you like to explore data for "Chicago", "New York City", or "Washington"?:\n').lower()
        if desired_city in ['chicago', 'new york city', 'washington']:
            continue
        else:
            print('Incorrect Entry for City. Please type Chicago, New York City, or Washington.')
            desired_city = ''
    
    # I've added the sort clause here so that the user is asked straight away how they want to filter the data, instead of having to go through the menus if they want no sorting
    while desired_sort == '':
        desired_sort = input('Would you like to sort by "month", "day" of week, "both", or "none"?:\n').lower()
        if desired_sort in ['month', 'day', 'both', 'none']:
            continue
        else:
            print('Incorrect Entry for Sorting. Please type month, day, both, or none.')
            desired_sort = ''
   
    # get user input for month if they requested it (january, february, ... , june)
    if desired_sort in ['month', 'both']:
        while desired_month == '':
            desired_month = input('You\'ve indicated that you would like to filter the data by month; please type the desired month ("January" through "June" only):\n').lower()
            if desired_month in ['january', 'february', 'march', 'april', 'may', 'june']:
                continue
            else:
                print('Incorrect Entry for Month. Please type (January through June only).')
                desired_month = ''

    # get user input for day of week if they requested it (monday, tuesday, ... sunday)
    if desired_sort in ['day', 'both']:
        while desired_day == '':
            desired_day = input('You\'ve indicated that you would like to filter the data by day of the week; please type the desired day ("Su","M","Tu","W","Th","F","Sa"):\n').lower()
            if desired_day in ['su','m','tu','w','th','f','sa']:
                continue
            else:
                print('Incorrect Entry for Day of Week. Please type Su, M, Tu, W, Th, F, or Sa.')
                desired_day = ''

    print('-'*40)

    return desired_city, desired_sort, month_dict[desired_month], day_dict[desired_day]


def load_data(city):
    """
    Loads data for the specified city and generates additional columns to filter on

    Args:
        (str) city - name of the city to analyze
        (str) month - REMOVED FROM THIS METHOD; UTILIZED IN table_prep() METHOD
        (str) day - REMOVED FROM THIS METHOD; UTILIZED IN table_prep() METHOD
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv('./'+city_data[city])
    
    # Convert time columns to datetime to break into chunks    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Check that Gender and Birth Year columns are there, and if not fill them with NaN
    if 'Gender' not in df:
        df['Gender'] = np.nan
    if 'Birth Year' not in df:
        df['Birth Year'] = np.nan
        
    # Break datetimes into chunks for month, day of week, and hour
    df['Start Month'] = df['Start Time'].dt.month
    df['Start Day'] = df['Start Time'].dt.day_of_week
    df['Start Hour'] = df['Start Time'].dt.hour
    
    df['End Month'] = df['End Time'].dt.month
    df['End Day'] = df['End Time'].dt.day_of_week
    df['End Hour'] = df['End Time'].dt.hour

    # Clean NaNs
    df['Gender'].fillna('None Specified', inplace = True)
    
    if df['Birth Year'].isnull().sum() == len(df):
        average_birthyear_prescrub = 0
    else:
        average_birthyear_prescrub = df['Birth Year'].mean()
    df['Birth Year'].fillna(average_birthyear_prescrub, inplace = True)

    # I'm replacing any empty User Types with Customer instead of 'None Specified', because they've obviously purchased and utilized the service and that's one less type to code for
    df['User Type'].fillna('Customer', inplace = True)

    # Generate Trips with Starts and Stops
    df['StartStop'] = df['Start Station'] + " to " + df['End Station']

    # Generate a new index column to use for this that should be numerical, and make it the actual indexing column of the dataframe

    return df


def table_filter(input_table, sort_type, month, day):

    if sort_type == 'none':
        return input_table
    
    if sort_type in ['month', 'both']:
        input_table = input_table[input_table['Start Month'] == month]
    
    if sort_type in ['day', 'both']:
        input_table = input_table[input_table['Start Day'] == day]

    return input_table


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
   
    modes = df.mode().head(1)
    
    # #1 - Popular times of travel for selected data
    print('Most Common Month of Travel:', num_month_dict[int(modes['Start Month'])].title())
    print('Most Common Day of Travel:  ', num_day_dict[int(modes['Start Day'])].title())
    
    mode_hour = int(modes['Start Hour'])
    if mode_hour > 12:
        mode_hour -= 12
        travel_hour = str(mode_hour) + ' PM'
    elif mode_hour == 12:
        travel_hour = str(mode_hour) + ' PM'
    else:
        travel_hour = str(mode_hour) + ' AM'
    
    print('Most Common Hour of Travel: ', travel_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    modes = df.mode().head(1)
    
    print('Most Common Trip:          ', modes['StartStop'][0])
    print('Most Common Start Station: ', modes['Start Station'][0])
    print('Most Common End Station:   ', modes['End Station'][0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_seconds = df['Trip Duration'].sum()
    average_seconds = total_seconds/len(df)
    print('Average Travel Time: {} minutes and {} seconds ({} seconds)'.format(int(average_seconds/60), int(average_seconds%60), int(average_seconds)))
    print('Total Travel Time:   {} minutes and {} seconds ({} seconds)'.format(int(total_seconds/60), int(total_seconds%60), int(total_seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Count of User Types:\n', df.groupby(['User Type'])['User Type'].count(),'\n')
    print('Count of User Genders:\n', df.groupby(['Gender'])['Gender'].count(),'\n')
    
    if df['Birth Year'].max() == 0:
        print('No user birth year data available.')
    else:
        print('Birth Years of Users: Oldest: {}    Youngest: {}    Average: {}'.format(df['Birth Year'].min(),df['Birth Year'].max(), df['Birth Year'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data5(df):
    df = df.drop(['Start Month', 'Start Day', 'Start Hour', 'End Month', 'End Day', 'End Hour', 'StartStop'], axis = 1)

    i = 0
    loop_var2 = input('\nWould you like to see 5 lines of raw user data from your filtered list? (Y/N)\n').lower()

    # This loop iterates through the table 5 rows at a time until the user doesn't want to anymore
    while loop_var2 in ['y','yes']:
        if loop_var2 in ['y','yes']:
            for j in range(i,i+5):
                print(df.iloc[j,:],'\n')
            i+=5
            loop_var2 = input('\nWould you like to see an additional 5 lines of raw user data from your filtered list? (Y/N)\n').lower()
        else:
            continue

def main():
    while True:
        city, sort, month, day = get_filters()
        df = load_data(city)
        df = table_filter(df, sort, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data5(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() not in ['yes','y']:
            break


if __name__ == "__main__":
	main()
