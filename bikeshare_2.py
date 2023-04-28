import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january','february','march','april','may','june','all']
weekdays=['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','All']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        usercity= input('Would you like to get data about chicago, new york city or washington? \n')
        city=usercity.lower()
        # if condition to handle invalid inputs from users
        if city not in CITY_DATA:
            print('sorry, ',city,' is not among the choosable cities, Please enter a valid city name')
            continue
        else:
            break



    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
        month= input('Would you like to get data from january,february,march,april,may,june or all? \n').lower()
         # if condition to handle invalid inputs from users
        if month not in months:
            print('Sorry, ',month,' is not among the choosable months.Please enter a valid month name')
            continue
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day= input('which day of the week ? you can choose all by typing "all"\n').title()
        if day not in weekdays:
            print('Please enter a valid day name')
            continue
        else:
            break

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
    #Load the csv file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    #convert the Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Extract the months from the Start Time
    df['month']=df['Start Time'].dt.month
    #Extract the days from the Start Time
    df['day_of_week']=df['Start Time'].dt.day_name()

    #filter months according to the user input
    if month.lower() != 'all':
     #Adding 1 to the index as it starts at [0]
     month=months.index(month)+1
     #Creating a new dataframe with the selected month , if applied
     df= df[df['month']==month]
    #Filter days according to the user input
    if day.lower() != 'all':
     #Creating a new dataframe with the selected day, if applied
     df=df[df['day_of_week']==day.title()]

    #print(df)-Testing
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #To display the month name, we call the months list and extract the exact month by the index number returned from the mode() method
    month_name = months[int(df['month'].mode()[0])-1]
    print('The Most Common month of travel:',month_name)

    # TO DO: display the most common day of week
    print('The Most Common day of travel:', df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
#     df['hour'] = df['Start Time'].dt.hour
    print('The Most common Hour of travel: ', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_start_station = df['Start Station'].value_counts().idxmax()
    print('The most common start station is: ',most_start_station)

    # TO DO: display most commonly used end station
    most_end_station = df['End Station'].value_counts().idxmax()
    print('The most common end station is: ', most_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most Frequent Combination:\n',combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time : ',total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time : ',mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print('User Types: \n',user_types)
    print(' '*40)
    # TO DO: Display counts of gender
    #applying try and except to avoid errors with washington as it contains no gender data
    try:
      gender = df['Gender'].value_counts().to_string()
      print('Gender: \n',gender)
    except:
      print('We are sorry, Gender data is not available for Washington')
    print(' '*40)

    # TO DO: Display earliest, most recent, and most common year of birth
    #applying try and except to avoid errors with washington as it contains no Birth year data

    try:
        earliest= int(df['Birth Year'].min())
        latest=int(df['Birth Year'].max())
        most_common=int(df['Birth Year'].mode()[0])
        print('Earliest year of birth is {} \nLatest year of birth is {} \nMost common year of birth is {}'.format(earliest,latest,most_common))
    except:
        print('We are sorry, Birthyear data is not available for Washington')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ shows raw data to the user upon request"""
    raw_data_request=input('Would you like to see the raw data ? - Type "yes" for data or "no" to exit- \n')
    # applying condition according to the user input
    # if yes, we iterate through the number of rows, 5 rows at a time, displaying the 5 next rows when the user chooses to see more
    if raw_data_request.lower() == 'yes':
      row_numbers = df.shape[0]
      print(row_numbers)
      i=5
      while True:
        #printing only the next 5 , not from the beggining
        print(df.head(i).tail())
        i+=5
        # if the number i exceeds row_numbers, there is no more data to show so we break the code
        if i >= row_numbers:
            print('Sorry, No more data available')
            break
        more=input('Would you like to see more data? - Type "yes" for more or "no" to exit- \n')
        # if the user asks for more data, we continue to the beggining of the loop,else we break
        if more.lower() == 'yes':

            continue
        else:
            break




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
