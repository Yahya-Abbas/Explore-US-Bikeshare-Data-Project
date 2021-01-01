import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month, day = 'all', 'all'
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input(
        "Would you like to see the data for Chicago, New York, or Washington?\n").lower()
    while city.title() not in ["Chicago", "New York", "Washington"]:
        city = input(
            "Invalid input, please choose a city from Chicago, New York, or Washington, and review your spelling.\n").lower()

    # get user input for month (all, january, february, ... , june)
    time_filter = input(
        "Would you like to filter the data by month, day, both, or not at all? Type 'none' for no filters on time.\n")
    while time_filter.lower() not in ["month", "day", "both", "none"]:
        time_filter = input(
            "Invalid input. Please choose to filter by month, day, both, or none, and review your spelling.\n")
    if time_filter.lower() != 'none':
        if time_filter.lower() in ["both", "month"]:
            month = input(
                "Which month?  January, February, March, April, May, or June?\n").lower()
            while month.title() not in ["January", "February", "March", "April", "May", "June"]:
                month = input(
                    "Invalid input. Please choose a month from January, February, March, April, May, or June. And check your spelling.\n").lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
        if time_filter.lower() in ["both", "day"]:
            day = input(
                "Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").lower()
            while day.title() not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                day = input(
                    "Invalid input. Please choose a day from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday. And check your spelling.\n").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city], index_col=[0])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        print("The Most Common Month of travel is:\n{}".format(
            df['month'].mode()[0]))
    # display the most common day of week
    if day == 'all':
        print("The Most Common Day of Week for travel is:\n{}".format(
              df['day_of_week'].mode()[0]))
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The Most Popular Start Hour:\n{}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The Most Popular Start Station is:\n",
          df['Start Station'].mode()[0], sep='')
    # display most commonly used end station
    print("The Most Popular End Station is:\n",
          df['End Station'].mode()[0], sep='')
    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print("The Most Popular Combination of Start - End Stations is:\n{}".format(
        popular_combination).replace(',', ' -'))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, month, day):
    """Displays statistics on the total and average trip duration based on the filters the user applied."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time (for all the 6 month if the user didn't filter data)
    total_travel_time = pd.to_timedelta(df['Trip Duration'].sum(), unit='s')
    if month == 'all' and day == 'all':
        print("Total Time spent on trips during The First 6 Months of 2017 is:\n",
              total_travel_time, sep='')

    # display travel duration statistics for the month the user chose
    elif month != 'all' and day == 'all':
        print("Total Time spent on trips during {}, 2017 is:\n".format(
            month.title()), total_travel_time, sep='')

    # display travel duration statistics for the day the user chose
    elif month == 'all' and day != 'all':
        print("Total Time spent on trips during {}s, through 2017 is:\n".format(
            day.title()), total_travel_time, sep='')

    # display travel duration statistics for the month the user chose
    else:
        print("Total Time spent on trips during {}s in {}, 2017 is:\n".format(day.title(),
                                                                              month.title()), total_travel_time, sep='')
    # display mean travel time
    print("And The Average Time spent on each trip is:\n",
          pd.to_timedelta(df['Trip Duration'].mean(), unit='s'), sep='')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Breakdown of Users:\n")
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())
    # Display counts of gender
    print("\nBreakdown of Gender:")
    if city.title() == "Washington":
        print("There is no Gender Data to share about Washington.")
        print("\nThe Earliest, Most Recent, and Most Common Year of birth, Respectively:")
        print("There is no Birth Year data about Washington to share.")
    else:
        gender_breackdown = df['Gender'].value_counts()
        print(gender_breackdown.to_string())
    # Display earliest, most recent, and most common year of birth
        print("\nThe Earliest, Most Recent, and Most Common Year of birth, Respectively:\n{}, {}, {}".format(
            int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df, month, day)
        user_stats(df, city)
        see_individual_trips = input(
            '\nWould you like to view individual trip data? Type yes or no.\n')
        row_index = 0
        while see_individual_trips.lower() not in ['yes', 'no']:
            see_individual_trips = input(
                "\nInvalid Input. Please Type 'yes' to see Individual trips or 'no' to skip.\n")
        while see_individual_trips.lower() == 'yes':
            print("\n", df[row_index*5: row_index*5 + 5])
            see_individual_trips = input(
                '\nWould you like to view another 5 lines of raw data? Type yes or no.\n')
            while see_individual_trips.lower() not in ['yes', 'no']:
                see_individual_trips = input(
                    "\nInvalid Input. Please Type 'yes' to see more Individual trips or 'no' to skip.\n")

            row_index += 1
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() not in ['yes', 'no']:
            restart = input(
                "\nInvalid Input. Please type 'yes' to restart or 'no' to exit.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
