import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

time_filters = ['both', 'month', 'day', 'none']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'septemper', 'october', 'november', 'december']
week_days= ['Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
flag = True		

def val_check(input_filter,valid_options):
	""" Check if the input is correct"""	
	if input_filter in valid_options:
		return False
	else:
		print("\nPlease enter a valid option.")
		return True	

def get_city(flag):
	"""Asks user to specify a city"""
	while flag:
		city = input("Would you like to see the data for chicago, new york city or washington? \n").lower()
		flag = val_check(city,CITY_DATA.keys())
	return city
	
def get_time_filters(flag):
	while flag:
		filter = input("Would you like to filter the data by month, day, both or not at all? For no time filter type none.\n").lower()
		flag = val_check(filter,time_filters)
	return filter
	
def get_month(flag):
	"""Asks user to specify a month"""
	while flag:
		month = input("Which month? \(january, february, ... , june\)\n").lower()
		flag = val_check(month,months)
		if flag == False:
			month = months.index(month) + 1
	return month

def get_day(flag):
	"""Asks user to specify a day"""
	while flag:
		day = input("Which day? \(Friday, Saturday, ... , Thursday\)\n").title()
		flag = val_check(day,week_days)
	return day	
	
def get_month_day(flag, filter):
	if (filter == 'both'):
		month = get_month(flag)
		day = get_day(flag)
	elif (filter == 'month'):
		month = get_month(flag)
		day = 'all'
	elif (filter == 'day'):
		day = get_day(flag)
		month = 'all'
	elif (filter == 'none'):
		month = 'all'
		day = 'all'
	print('-'*40)
	return month,day


def load_data(city,month,day):
	df = pd.read_csv(CITY_DATA[city])
	df['Start Time'] = pd.to_datetime(df['Start Time'],infer_datetime_format=True)
	df['month'] = df['Start Time'].dt.month
	df['day_of_week']= df['Start Time'].dt.day_name()
	df ['hour'] = df['Start Time'].dt.hour
	if month != 'all':
		df = df[df['month']== month]
	if day != 'all':
		df = df[df['day_of_week']== day]
	return df
	

	
def time_stats(df,filter):
	"""Displays statistics on the most frequent times of travel."""
	print('\nCalculating The Most Frequent Times of Travel...\n')
	start_time = time.time()
	if filter != 'both':
		# display the most common month
		if filter != 'month':
			most_common_month = months[df['month'].mode()[0]]
			print('Most common month: {}'.format(most_common_month))
		# display the most common day of week
		if filter != 'day':
			most_common_day = df['day_of_week'].value_counts().idxmax()
			print('\nMost common day of week: {}'.format(most_common_day))
    # display the most common start hour
	most_common_hour = df ['hour'].mode()[0]
	print('Most common start hour: {}'.format(most_common_hour)) 
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)
	
def station_stats(df):
	"""Displays statistics on the most popular stations and trip."""
	print('\nCalculating The Most Popular Stations and Trip...\n')
	start_time = time.time()
    # display most commonly used start station
	most_common_ss = df['Start Station'].value_counts().idxmax() # ss: start station
    # display most commonly used end station
	most_common_es = df['End Station'].value_counts().idxmax()   # es: end station
    # display most frequent combination of start station and end station trip
	most_common_s = df[['Start Station','End Station']].value_counts().idxmax()  
	print('Start Station: {}'.format(most_common_ss))
	print('\nEnd Station: {}'.format(most_common_es))
	print('\nMost frequent trip: {}'.format(most_common_s))
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)
	
	
def trip_duration_stats(df):
	"""Displays statistics on the total and average trip duration."""
	print('\nCalculating Trip Duration...\n')
	start_time = time.time()
	# display total travel time
	tot_trav_t = df['Trip Duration'].sum()
	# display mean travel time
	mean_trav_t = df['Trip Duration'].mean()
	print('Total travel time: {}'.format(tot_trav_t))
	print('\nAverage travel time: {}'.format(mean_trav_t))
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def user_stats(df,city):
	"""Displays statistics on bikeshare users."""
	print('\nCalculating User Stats...\n')
	start_time = time.time()
    # Display counts of user types
	user_types = df['User Type'].value_counts()
	print(user_types)
	if city != 'washington':
		# Display counts of gender
		gender = df['Gender'].value_counts()
		print(gender)
		# Display earliest, most recent, and most common year of birth
		most_common_year = int(df['Birth Year'].mode()[0])
		most_recent_year = int(df['Birth Year'].max())
		earliest_year = int(df['Birth Year'].min())
		print('\nThe earliest year of birth: {}'.format(earliest_year))
		print('\nMost recent year of birth: {}'.format(most_recent_year))
		print('\nMost common year of birth: {}'.format(most_common_year))
	print('\nThis took %s seconds.' % (time.time() - start_time))
	print('-'*40)

def get_view_data(flag):
	while flag:
		view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
		flag = val_check(view_data,['yes','no'])
	return view_data
def display_data(view_data,df,flag):
	counter = 0
	while True:
		if view_data == 'yes':
			print(df.iloc[counter:counter+5])
			counter+=5
			view_data = get_view_data(flag)
		else :
			break
			
		
		

def main():
	while True:
		city = get_city(flag)
		filter = get_time_filters(flag)
		month, day = get_month_day(flag,filter)
		df = load_data(city,month,day)
		
		time_stats(df,filter)
		station_stats(df)
		trip_duration_stats(df)
		user_stats(df,city)
		
		view_data = get_view_data(flag)
		display_data(view_data,df,flag)
		
		restart = input('\nWould you like to restart? Enter yes or no.\n')
		if restart.lower() != 'yes':
			break


if __name__ == "__main__":
	main()
