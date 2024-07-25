import pandas as pd
import numpy as np
import warnings
from pandas.tseries.offsets import CustomBusinessDay
from pathlib import Path
warnings.filterwarnings('ignore')
from Logger import setup_logging

logger = setup_logging('Forecast.log')


class Features():

    def __init__(self , Dataset_path , USD_Dataset_path, info = False , t1 = 100 , t2 = 500 , t3 = 1000 , t4 = 5000):
        try:
            self.df = pd.read_json(Dataset_path, lines=True)
            logger.info("File loaded successfully")
        except FileNotFoundError:
            logger.error("The Dataset file was not found.")
        except ValueError:
            logger.error("The Dataset file could not be parsed.")
        except Exception as e:
            logger.error(f"An Dataset error occurred: {e}")

        try:
            self.usd = pd.read_csv(USD_Dataset_path)
            self.usd['RecTime'] = pd.to_datetime(self.usd["Date"])
            logger.info("File loaded successfully")
        except FileNotFoundError:
            logger.error("The USD file was not found.")
        except ValueError:
            logger.error("The USD file could not be parsed.")
        except Exception as e:
            logger.error(f"An USD error occurred: {e}")


        if(info):
            self.dataset_info()
        
        self.process_dates()
        self.convert(t1 , t2 , t3 , t4)
        
        self.df['TotalValueUSD'] = self.df.apply(lambda row: self.convert_to_usd(row['RecTime'], row['TotalValue']), axis=1)
        self.df['Last7Days_mean'] = self.df['TotalValueUSD'].rolling(window=7, min_periods=1).mean().shift(1)
        self.df['Last30Days_mean'] = self.df['TotalValueUSD'].rolling(window=30, min_periods=1).mean().shift(1)
        
        logger.info('Amounts Converted to USD')

        self.add_holidays()
        logger.info('Holidays Added')

        self.add_events()
        logger.info('Events Added')

        self.add_paydays()
        logger.info('Paydays Added')

        self.df['HolidaySequence'] = self.get_holidays_sequence(self.df['IsHoliday'])
        logger.info('Holiday sequence Added')
        

        name = Path(r"C:\Users\Hp\Desktop\cashInfo-1006.json").stem
        self.df.to_csv(name+'processed')
        logger.info(f'Procesed Dataset saved as {name}processed.csv')


    def dataset_info(self):
        logger.info('DF Shape: %s', self.df.shape)
        logger.info('Number of Columns: %d', len(self.df.columns))
        logger.info('Number of Observations: %d', len(self.df))
        logger.info('Number of values in self.df: %d', self.df.count().sum())
        logger.info('Total Number of Missing values in self.df: %d', self.df.isna().sum().sum())
        logger.info('Percentage of Missing values: %.2f%%', (self.df.isna().sum().sum() / self.df.count().sum() * 100))
        logger.info('Total Number of Duplicated records in self.df: %d', self.df.duplicated().sum())
        logger.info('Percentage of Duplicated values: %.2f%%', (self.df.duplicated().sum() / self.df.count().sum() * 100))

    def process_dates(self):
        self.df['RecTime'] = pd.to_datetime(self.df['RecTime'])
        self.df['Year'] = self.df['RecTime'].dt.year
        self.df['Month'] = self.df['RecTime'].dt.month
        self.df['Date'] = self.df['RecTime'].dt.day
        self.df['DayOfWeek'] = self.df['RecTime'].dt.dayofweek
        self.df['IsWeekend'] = self.df['RecTime'].dt.dayofweek >= 5
        self.df['Quarter'] = self.df['RecTime'].dt.quarter
        self.df['DayOfYear'] = self.df['RecTime'].dt.dayofyear
        self.df['PartOfMonth'] = self.df['RecTime'].dt.day.apply(lambda day: '1' if day <= 10 else ('2' if day <= 20 else '3'))
        # self.df['prevWeek'] = self.df['TotalValue'].rolling(window=7, min_periods=1).mean().shift(1)


        self.df.drop(['ATMId' , 'Id' , 'HolidayType' ] , axis= 1 , inplace= True)

    def convert(self , t1 = 100 , t2 = 500 , t3 = 1000 , t4 = 5000):
        self.df['Type1Value'] = t1 * self.df['Type1Count']
        self.df['Type2Value'] = t2 * self.df['Type2Count']
        self.df['Type3Value'] = t3 * self.df['Type3Count']
        self.df['Type4Value'] = t4 * self.df['Type4Count']
        self.df['TotalValue'] = self.df['Type1Value'] + self.df['Type2Value'] + self.df['Type3Value'] + self.df['Type4Value'] 
        
    def convert_to_usd(self , date, total_value):
       
        price_row = self.usd[self.usd['RecTime'] <= date]
        
        if not price_row.empty:
            # Find the most recent available exchange rate before or on the given date
            latest_price_row = price_row.sort_values(by='RecTime', ascending=False).iloc[0]
            price = latest_price_row['Price']
            # Convert TotalValue to USD
            return total_value / price
        else:
            # If no exchange rate is available, return NaN or handle accordingly
            return None


    def add_holidays(self):
        public_holidays = {
            '2020-02-05': 'Kashmir Day',
            '2020-03-23': 'Pakistan Day',
            '2020-05-01': 'Labour Day',
            '2020-05-24': 'Eid-ul-Fitr Day 1',
            '2020-05-25': 'Eid-ul-Fitr Day 2',
            '2020-05-26': 'Eid-ul-Fitr Day 3',
            '2020-07-31': 'Eid al-Adha Day 1',
            '2020-08-01': 'Eid al-Adha Day 2',
            '2020-08-02': 'Eid al-Adha Day 3',
            '2020-08-14': 'Independence Day',
            '2020-08-28': 'Ashura',
            '2020-08-29': 'Ashura',
            '2020-10-29': 'Eid Milad un-Nabi',
            '2020-11-09': 'Iqbal Day',
            '2020-12-25': 'Christmas Day',
            '2020-12-25': 'Quaid-e-Azam Day',


            '2021-02-05': 'Kashmir Day',
            '2021-03-23': 'Pakistan Day',
            '2021-05-01': 'Labour Day',
            '2021-05-13': 'Eid-ul-Fitr Day 1',
            '2021-05-14': 'Eid-ul-Fitr Day 2',
            '2021-05-15': 'Eid-ul-Fitr Day 3',
            '2021-07-20': 'Eid al-Adha Day 1',
            '2021-07-21': 'Eid al-Adha Day 2',
            '2021-07-22': 'Eid al-Adha Day 3',
            '2021-08-14': 'Independence Day',
            '2021-08-18': 'Ashura',
            '2021-08-19': 'Ashura',
            '2021-10-19': 'Eid Milad un-Nabi',
            '2021-11-09': 'Iqbal Day',
            '2021-12-25': 'Christmas Day',
            '2021-12-25': 'Quaid-e-Azam Day',
            

            '2022-02-05': 'Kashmir Day',
            '2022-03-23': 'Pakistan Day',
            '2022-05-01': 'Labour Day',
            '2022-05-03': 'Eid-ul-Fitr Day 1',
            '2022-05-04': 'Eid-ul-Fitr Day 2',
            '2022-05-05': 'Eid-ul-Fitr Day 3',
            '2022-07-10': 'Eid-ul-Azha Day 1',
            '2022-07-11': 'Eid-ul-Azha Day 2',
            '2022-07-12': 'Eid-ul-Azha Day 3',
            '2022-08-07': 'Ashura',
            '2022-08-08': 'Ashura',
            '2022-08-14': 'Independence Day',
            '2022-10-09': 'Eid Milad-un-Nabi',
            '2022-12-25': 'Quaid-e-Azam Day',

            '2023-02-05': 'Kashmir Day',
            '2023-03-23': 'Pakistan Day',
            '2023-04-22': 'Eid ul-Fitr Day 1',
            '2023-04-23': 'Eid ul-Fitr Day 2',
            '2023-04-24': 'Eid ul-Fitr Day 3',    
            '2023-05-01': 'Labour Day',
            '2023-06-29': 'Eid ul-Azha Day 1',
            '2023-06-30': 'Eid ul-Azha Day 2',
            '2023-07-1': 'Eid ul-Azha Day 2',
            '2023-07-28': 'Ashura',
            '2023-07-29': 'Ashura',
            '2023-08-14': 'Independence Day',
            '2023-09-28': 'Eid Milad un-Nabi',
            '2023-11-09': 'Iqbal Day',
            '2023-12-25': 'Quaid-e-Azam Day',

            '2024-02-05': 'Kashmir Day',
            '2024-03-23': 'Pakistan Day',
            '2024-05-01': 'Labour Day',
            '2024-05-03': 'Eid ul-Fitr Day 1',
            '2024-05-04': 'Eid ul-Fitr Day 2',
            '2024-05-05': 'Eid ul-Fitr Day 3',
            '2024-07-16': 'Eid ul-Azha Day 1',
            '2024-07-17': 'Eid ul-Azha Day 2',
            '2024-07-18': 'Eid ul-Azha Day 3',
            '2024-08-07': 'Ashura',
            '2024-08-08': 'Ashura',
            '2024-08-14': 'Independence Day',
            '2024-09-28': 'Eid Milad un-Nabi',
            '2024-11-09': 'Iqbal Day',
            '2024-12-25': 'Quaid-e-Azam Day',
            '2024-12-26': 'Day after Christmas',

            '2024-01-01': 'New Year’s Day',
            '2024-02-05': 'Kashmir Day',
            '2024-03-23': 'Pakistan Day',
            '2024-05-01': 'Labour Day',
            '2024-05-03': 'Eid ul-Fitr Day 1',
            '2024-05-04': 'Eid ul-Fitr Day 2',
            '2024-05-05': 'Eid ul-Fitr Day 3'
        }
        self.df['HolidayType'] = None
        self.df['IsHoliday'] = False

            # Add 'HolidayType' based on 'RecTime'
        self.df['HolidayType'] = self.df['RecTime'].apply(lambda x: public_holidays.get(x.strftime('%Y-%m-%d'), None))
        self.df['IsHoliday'] = self.df['HolidayType'].notna()
        self.df.loc[self.df['IsWeekend'], 'IsHoliday'] = True



        self.df.loc[self.df['RecTime'].between(pd.to_datetime('2024-2-8') ,pd.to_datetime('2024-2-9') ), 'HolidayType'] = 'Elections'
    


    def add_events(self):
        self.df['RecTime'] = pd.to_datetime(self.df['RecTime'])
        ramzan_ranges = [
            (pd.to_datetime('2020-04-24'), pd.to_datetime('2020-05-23')),
            (pd.to_datetime('2021-04-13'), pd.to_datetime('2021-05-12')),
            (pd.to_datetime('2022-04-02'), pd.to_datetime('2022-05-01')),
            (pd.to_datetime('2023-03-22'), pd.to_datetime('2023-04-21')),
            (pd.to_datetime('2024-03-11'), pd.to_datetime('2024-04-09'))
        ]

        hajj_ranges = [
            (pd.to_datetime('2020-07-22'), pd.to_datetime('2020-07-31')),
            (pd.to_datetime('2021-07-11'), pd.to_datetime('2021-07-20')),
            (pd.to_datetime('2022-06-30'), pd.to_datetime('2022-07-09')),
            (pd.to_datetime('2023-06-19'), pd.to_datetime('2023-06-28')),
            (pd.to_datetime('2024-06-07'), pd.to_datetime('2024-06-16'))
        ]

        muharram_ranges = [
            (pd.to_datetime('2020-08-20'), pd.to_datetime('2020-09-18')),
            (pd.to_datetime('2021-08-10'), pd.to_datetime('2021-09-08')),
            (pd.to_datetime('2022-07-31'), pd.to_datetime('2022-08-28')),
            (pd.to_datetime('2023-07-21'), pd.to_datetime('2023-08-19')),
            (pd.to_datetime('2024-07-10'), pd.to_datetime('2024-08-08'))
        ]



        self.df['Event'] = "Nothing"

        for start, end in ramzan_ranges:
            self.df.loc[self.df['RecTime'].between(start, end), 'Event'] = 'Ramzan'


        for start, end in hajj_ranges:
            self.df.loc[self.df['RecTime'].between(start, end), 'Event'] = 'Hajj'
            
        for start, end in muharram_ranges:
            self.df.loc[self.df['RecTime'].between(start, end), 'Event'] = 'Muharram'

    def add_paydays(self):

        all_paydays = []

        for year in range(2020, 2025):
            paydays_year = []
            
            for month in range(1, 13):
                month_dates = pd.date_range(start=f'{year}-{month:02d}-01', end=f'{year}-{month:02d}-10')
                paydays_year.append(pd.DataFrame({'RecTime': month_dates}))

            paydays_year = pd.concat(paydays_year, ignore_index=True)
            weekmask = 'Mon Tue Wed Thu Fri'
            bday = CustomBusinessDay(weekmask=weekmask)
            paydays_year['RecTime'] = paydays_year['RecTime'] + bday
            
            all_paydays.append(paydays_year)

        all_paydays = pd.concat(all_paydays, ignore_index=True)
        all_paydays['RecTime'] = pd.to_datetime(all_paydays['RecTime'])
        self.df['Paydays'] = False


        self.df.loc[self.df['RecTime'].isin(all_paydays['RecTime']), 'Paydays'] = True
    
    def get_holidays_sequence(self,is_holiday_series):
        sequence = []
        n = len(is_holiday_series)
        for i in range(n):
            if i == 0:  # Only today
                seq = ('H' if is_holiday_series[i] else 'W')
            elif i == 1:  # Yesterday and today
                seq = ('H' if is_holiday_series[i-1] else 'W') + ('H' if is_holiday_series[i] else 'W')
            elif i == n-1:  # Yesterday and today
                seq = ('H' if is_holiday_series[i-1] else 'W') + ('H' if is_holiday_series[i] else 'W')
            elif i == n-2:  # Yesterday, today, and tomorrow
                seq = (
                    ('H' if is_holiday_series[i-1] else 'W') +
                    ('H' if is_holiday_series[i] else 'W') +
                    ('H' if is_holiday_series[i+1] else 'W')
                )
            else:  # Full sequence
                seq = (
                    ('H' if is_holiday_series[i-1] else 'W') +
                    ('H' if is_holiday_series[i] else 'W') +
                    ('H' if is_holiday_series[i+1] else 'W') +
                    ('H' if is_holiday_series[i+2] else 'W')
                )
            sequence.append(seq)
        return sequence