import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv',
}

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
        'saturday', 'sunday']
SEPARATOR = '-' * 40


def get_valid_input(prompt, valid_options):
    """Prompt the user until they enter one of the allowed options."""
    valid_options_text = ', '.join(valid_options)

    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input

        print(f"Please enter one of the following: {valid_options_text}.")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_valid_input(
        'Which city would you like to analyze? '
        '(chicago, new york city, washington)\n',
        CITY_DATA.keys(),
    )

    # get user input for month (all, january, february, ... , june)
    month = get_valid_input(
        'Which month would you like to filter by? '
        '(all, january, february, march, april, may, june)\n',
        MONTHS,
    )

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_valid_input(
        'Which day would you like to filter by? '
        '(all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n',
        DAYS,
    )

    print(SEPARATOR)
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_number = MONTHS.index(month)
        df = df[df['month'] == month_number]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    df = df.copy()
    return df


def display_most_common(df, column, label):
    """Display the most common value in a column when data is available."""
    if df.empty:
        print(f"No data available for {label}.")
        return

    most_common = df[column].mode().iloc[0]
    print(f"Most common {label}: {most_common}")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    display_most_common(df, 'month', 'month')

    # display the most common day of week
    display_most_common(df, 'day_of_week', 'day of week')

    # display the most common start hour
    display_most_common(df, 'hour', 'start hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    display_most_common(df, 'Start Station', 'start station')

    # display most commonly used end station
    display_most_common(df, 'End Station', 'end station')

    # display most frequent combination of start station and end station trip
    if df.empty:
        print("No data available for station trip combinations.")
    else:
        trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
        print(f"Most frequent trip: {trip[0]} to {trip[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    if df.empty:
        print("No trip duration data available.")
    else:
        print(f"Total travel time: {df['Trip Duration'].sum()}")

        # display mean travel time
        print(f"Mean travel time: {df['Trip Duration'].mean()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUser type counts:")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df:
        print("\nGender counts:")
        print(df['Gender'].value_counts())
    else:
        print("\nGender data is not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_year = df['Birth Year'].dropna()
        if birth_year.empty:
            print("\nBirth year data is not available for this selection.")
        else:
            print(f"\nEarliest birth year: {int(birth_year.min())}")
            print(f"Most recent birth year: {int(birth_year.max())}")
            print(f"Most common birth year: {int(birth_year.mode().iloc[0])}")
    else:
        print("\nBirth year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
