import time
import datetime
import pytz

from OtipyTicket.settings import TIME_ZONE


class TimeConversionException(Exception):

    def __init__(self, e):
        message = {"error": {
            "message": "Time Conversion Exception ",
            "code": 4033,
            "developer_message": str(e),
            "status_code": 503},
            "success": False}
        self.message = message

    def __str__(self):
        return repr(self.message)


class TimeManager():
    """Conversion for time to time

    """

    def __init__(self):
        self.time = None

    def get_current_epoch(self):
        return int(time.time())

    def get_epoch_from_db_field(self, value):
        try:
            return int(time.mktime(value.timetuple()))
        except Exception as e:
            raise TimeConversionException(e)

    def get_ddmmm_from_yymmdd(self, yymmdd, days=0, formt="%b %d"):
        t = time.strptime(str(yymmdd), '%y%m%d')
        newdate = datetime.date(t.tm_year, t.tm_mon,
                                t.tm_mday) + datetime.timedelta(days)
        return newdate.strftime(formt)

    def convert_into_db_format(self, epoch, t_format='%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.datetime.fromtimestamp(
                (int(epoch))).strftime(t_format)
        except Exception as e:
            raise TimeConversionException(e)

    def convert_from_db_format(self, value, t_format='%Y-%m-%d %H:%M:%S'):
        try:
            epoch = int(time.mktime(value.timetuple()))
            return self.convert_utc_to_ist(pytz.utc.localize(datetime.datetime.fromtimestamp(
                (int(epoch))))).strftime(t_format)
        except Exception as e:
            raise TimeConversionException(e)

    def convert_utc_to_ist(self, utc_date):
        local_tz = pytz.timezone(TIME_ZONE)
        return utc_date.astimezone(local_tz)

    def get_days_diff(self, start_date, end_date):
        return (end_date - start_date).days

    def get_hhmmss_from_seconds(self, seconds):
        return {
            'hh': seconds // 3600,
            'mm': seconds // 60 % 60,
            'ss': seconds // 60 // 60 % 60
        }

    def get_now_in_ist(self):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        return now_utc.astimezone(local_tz)

    def get_now_formatted(self):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        local_time =  now_utc.astimezone(local_tz)
        return local_time.strftime("%I:%M %p %d %b %y")

    def get_days_old_2(self, db_value):
        try:
            current_epoch = self.get_current_epoch()
            given_epoch = self.get_epoch_from_db_field(db_value)
            epoch_diff = current_epoch - given_epoch
            return int(epoch_diff / (24 * 60 * 60))
        except Exception as e:
            
            return -1

    def get_days_old(self, given_epoch):
        current_epoch = self.get_current_epoch()
        epoch_diff = current_epoch - given_epoch
        return int(epoch_diff / (24 * 60 * 60))

    def get_today_date(self, days=0):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        local_time = now_utc.astimezone(local_tz)
        if days:
            local_time = local_time + datetime.timedelta(days=days)
        today = local_time.strftime("%d %b").lower()
        return today

    def get_today_date_with_day(self, days=0):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        local_time = now_utc.astimezone(local_tz)
        if days:
            local_time = local_time + datetime.timedelta(days=days)
        today = local_time.strftime("%a, %d %b").lower()
        return today

    def get_ddmmm_from_ddmmyy(self, ddmmyy):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        newdate = datetime.date(t.tm_year, t.tm_mon, t.tm_mday)
        return newdate.strftime("%d %b")
    # def get_ddmmm_from_yymmdd(self, ddmmyy):
    #     t = time.strptime(str(ddmmyy), '%d%m%y')
    #     newdate = datetime.date(t.tm_year, t.tm_mon, t.tm_mday)
    #     return newdate.strftime("%d %b")


    def get_epoch_from_ddmmyy(self, ddmmyy):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        newdate = datetime.date(t.tm_year, t.tm_mon, t.tm_mday)
        return int(time.mktime(newdate.timetuple()))

    def get_monday_from_ddmmyy(self, ddmmyy):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        newdate = datetime.date(t.tm_year, t.tm_mon, t.tm_mday)
        start = newdate - datetime.timedelta(days=newdate.weekday())
        return start.strftime("%d%m%y").lower()

    def get_day_diff_from_slots(self, ddmmyy1, ddmmyy2):
        epoch1 = self.get_epoch_from_ddmmyy(ddmmyy1)
        epoch2 = self.get_epoch_from_ddmmyy(ddmmyy2)
        epoch_diff = epoch2 - epoch1
        return int(epoch_diff / (24 * 60 * 60))

    def convert_into_db_format_from_ddmmyy(self, ddmmyy, t_format='%Y-%m-%d'):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        newdate = datetime.date(t.tm_year, t.tm_mon, t.tm_mday)
        return newdate.strftime(t_format).lower()

    def convert_into_db_format_from_ddmmYY(
            self, ddmmYY, t_format='%Y-%m-%d %H:%M:%S'):
        t = time.strptime(str(ddmmYY), '%d%m%Y %H:%M:%S')
        return datetime.datetime(
            t.tm_year,
            t.tm_mon,
            t.tm_mday,
            t.tm_hour,
            t.tm_min,
            t.tm_sec)

    def convert_into_db_datetime_from_ddmmyy(
            self, ddmmyy, t_format='%Y-%m-%d %H:%M:%S'):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        return datetime.datetime(
            t.tm_year,
            t.tm_mon,
            t.tm_mday,
            t.tm_hour,
            t.tm_min,
            t.tm_sec)

    def get_previous_Ymd_from_ddmmyy(self, ddmmyy):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        newdate = datetime.date(t.tm_year, t.tm_mon,
                                t.tm_mday) + datetime.timedelta(-1)
        return newdate.strftime("%Y-%m-%d").lower()

    def get_Ymd_from_ddmmyy(self, ddmmyy, days=0):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        newdate = datetime.date(t.tm_year, t.tm_mon,
                                t.tm_mday) + datetime.timedelta(days)
        return newdate.strftime("%Y-%m-%d").lower()

    def get_mb_from_ddmmyy(self, ddmmyy, days=0, date_format='%b %d, %a'):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        newdate = datetime.date(t.tm_year, t.tm_mon,
                                t.tm_mday) + datetime.timedelta(days)
        return newdate.strftime(date_format)

    def get_next_yymmdd(self, yymmdd, days=0):
        t = time.strptime(str(yymmdd), '%y%m%d')
        newdate = datetime.date(t.tm_year, t.tm_mon,
                                t.tm_mday) + datetime.timedelta(days)
        return newdate.strftime('%y%m%d')

    def get_mb_from_yymmdd(self, yymmdd, formt="%b %d, %a", days=0):
        t = time.strptime(str(yymmdd), '%y%m%d')
        newdate = datetime.date(t.tm_year, t.tm_mon,
                                t.tm_mday) + datetime.timedelta(days)
        return newdate.strftime(formt)

    def get_ddmmyy(self, days=0, holiday_list=[], slot_id_list=[]):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        local_time = now_utc.astimezone(local_tz)
        tom_date = local_time + datetime.timedelta(days=days)
        while tom_date.strftime('%a').lower() in holiday_list or str(tom_date.strftime("%d%m%y")) in slot_id_list:
            tom_date = tom_date + datetime.timedelta(days=1)
            

        ddmm = tom_date.strftime("%d%m%y").lower()
        return ddmm

    def get_yymmdd(self, days=0, holiday_list=[], slot_id_list=[]):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        local_time = now_utc.astimezone(local_tz)
        tom_date = local_time + datetime.timedelta(days=days)
        while tom_date.strftime('%a').lower() in holiday_list:
            tom_date = tom_date + datetime.timedelta(days=1)

        ddmm = tom_date.strftime("%y%m%d").lower()
        return int(ddmm)


    def get_date(self, days=0, holiday_list=[], slot_id_list=[]):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        local_time = now_utc.astimezone(local_tz)
        tom_date = local_time + datetime.timedelta(days=days)
        while tom_date.strftime('%a').lower() in holiday_list or str(tom_date.strftime("%d%m%y")) in slot_id_list:
            tom_date = tom_date + datetime.timedelta(days=1)

        tomorrow = tom_date.strftime("%d %b, %a").upper()
        return tomorrow

    def get_military_time(self):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        local_time = now_utc.astimezone(local_tz)
        # format as 0900, 1909
        mil_time = int(('%0*d' % (2, local_time.hour)) +
                       ('%0*d' % (2, local_time.minute)))
        return mil_time

    def get_next_working_date(self, ddmmyy, holiday_list, days=1):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        newdate = datetime.date(
            t.tm_year,
            t.tm_mon,
            t.tm_mday) + datetime.timedelta(days)
        while(newdate.strftime("%a").lower() in holiday_list):
            newdate = newdate + datetime.timedelta(1)
        return newdate.strftime("%d%m%y").lower()

    def get_previous_working_date(self, ddmmyy, holiday_list, days=1):
        t = time.strptime(str(ddmmyy), '%d%m%y')
        newdate = datetime.date(t.tm_year, t.tm_mon,
                                t.tm_mday) + datetime.timedelta(-days)
        while(newdate.strftime("%a").lower() in holiday_list):
            newdate = newdate + datetime.timedelta(1)
        return newdate.strftime("%d%m%y").lower()

    def is_editable_epoch(self, slot_id, cutoff_time, extended_time, is_deal):
        """
        If slot is 031116 and cutofftime is
        2330 and extended time is 120
        """
        ddmmyy = str(slot_id)[:-1]
        cutoff_time = str(cutoff_time)
        seconds = "00"
        ddmmyyhhmmss = ddmmyy + cutoff_time + seconds
        t = time.strptime(str(ddmmyyhhmmss), '%d%m%y%H%M%S')

        epoch_time = datetime.datetime(
            t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min).strftime('%s')

        # Because slot id is for next days
        if is_deal:
            epoch_time = int(epoch_time) - 48 * 60 * 60
        else:
            epoch_time = int(epoch_time) - 24 * 60 * 60

        delivery_date = datetime.datetime(
            t.tm_year,
            t.tm_mon,
            t.tm_mday,
            t.tm_hour,
            t.tm_min).strftime("%d %b, %a").upper()
        extended_time_epoch = int(extended_time) * 60
        cutoff_date = datetime.datetime.fromtimestamp(
            int(epoch_time) + int(extended_time_epoch))
        cutoff_mil_time = self.add_minutes_to_mil(
            int(cutoff_time), int(extended_time))

        if cutoff_mil_time < 1300:
            cutoff_date = cutoff_date - datetime.timedelta(days=1)

        cutoff_date = cutoff_date.strftime("%d %b %a").upper()
        current_epoch = int(time.time())
        if current_epoch < int(epoch_time) + extended_time_epoch:
            return True, delivery_date, cutoff_date
        else:
            return False, delivery_date, cutoff_date

    def con_milto_ampm(self, mil_time):
        """
        mil_time is int
        """
        
        mil_time = int(mil_time)
        hour = mil_time / 100
        minutes = mil_time % 100
        bk = "AM"
        if hour > 12:
            bk = "PM"
            hour = hour - 12
        return str('%0*d' %
                   (2, hour)) + ":" + str('%0*d' %
                                          (2, minutes)) + str(" ") + bk

    def add_minutes_to_mil(self, mil_time, minutes):
        hour = minutes / 60
        minu = minutes % 60
        mil_time_add = hour * 100 + minu
        return (mil_time + mil_time_add) % 2400

    def get_day_from_slot_id(self, slot_id):
        ddmmyy = str(slot_id)
        t = time.strptime(str(ddmmyy), '%d%m%y')
        delivery_day = datetime.datetime(
            t.tm_year, t.tm_mon, t.tm_mday).strftime("%A").upper()
        return delivery_day

    def get_small_day_from_slot_id(self, slot_id):
        ddmmyy = str(slot_id)
        t = time.strptime(str(ddmmyy), '%d%m%y')
        delivery_day = datetime.datetime(
            t.tm_year, t.tm_mon, t.tm_mday).strftime("%a").upper()
        return delivery_day

    def get_day_from_n_slot_id(self, n_slot_id,formt="%a"):
        yymmdd = str(n_slot_id)
        t = time.strptime(str(yymmdd), '%y%m%d')
        delivery_day = datetime.datetime(
            t.tm_year, t.tm_mon, t.tm_mday).strftime(formt).upper()
        return delivery_day

    def is_purchase_active_epoch(self, slot_id, cutoff_time):
        ddmmyyhhmm = str(slot_id) + str(cutoff_time)
        t = time.strptime(str(ddmmyyhhmm), '%d%m%y%H%M')
        epoch_time = (datetime.datetime(
            t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min) -
            datetime.timedelta(days=1))
        epoch_time = epoch_time.strftime('%s')
        current_epoch = int(time.time())
        if current_epoch < int(epoch_time):
            return True
        else:
            return False

    def is_price_active_epoch(self, start, end):
        """

        """
        start = int(start)
        end = int(end)
        msg_string = str(self.con_milto_ampm(start)) + \
            "-" + str(self.con_milto_ampm(end))
        current_mil_time = int(self.get_military_time())
        if start < current_mil_time and current_mil_time < end:
            return True, ""
        elif current_mil_time < start:
            return False, " Today timimg for placing order \n" + msg_string
        elif current_mil_time > end:
            return False, "Crofarm store will open tomorrow at \n" + msg_string

    def get_slot_id_list(self, slot_id, num_of_days):
        slot_id_list = [slot_id + "1"]
        by = datetime.date(
            int('20' + slot_id[4:6]), int(slot_id[2:4]), int(slot_id[:2]))
        for day in range(0, num_of_days):
            time = by + datetime.timedelta(-day)
            slot_id_list.append(str(time.strftime('%d%m%y') + "1"))
            slot_id_list.append(str(time.strftime('%d%m%y') + "2"))
        return slot_id_list

    def get_between_slot(self, start_slot, end_slot):
        slot_id_list = []
        by = datetime.date(
            int('20' + start_slot[4:6]), int(start_slot[2:4]),
            int(start_slot[:2]))
        end = datetime.date(
            int('20' + end_slot[4:6]), int(end_slot[2:4]), int(end_slot[:2]))
        slot_id_list.append(start_slot)
        for day in range(0, (end - by).days):
            time = by + datetime.timedelta(day + 1)
            slot_id_list.append(str(time.strftime('%d%m%y')))
        return slot_id_list

    def get_between_nslot(self,start_slot,num_of_days):
        slot_id_list = []
        by = datetime.date(
            int('20' + str(start_slot)[:2]), int(str(start_slot)[2:4]), int(str(start_slot)[4:6]))
        
        for day in range(0, num_of_days):
            time = by + datetime.timedelta(-day)
            slot_id_list.append(str(time.strftime('%y%m%d')))
        return slot_id_list

    def transpose_slot(self, slot_id):
        slot_id = str(slot_id)
        return slot_id[4:6] + slot_id[2:4] + slot_id[0:2]

    def get25PaiseRoundOff(self, value):
        value = float(value)
        valFraction = value - int(value)
        if(valFraction % 0.25 <= 0.1):
            return round((value) - (valFraction % 0.25), 2)
        else:
            return round(value + (0.25 - (valFraction % 0.25)), 2)


    def get_week_day(self, days=0, holiday_list=[], slot_id_list=[]):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        local_time = now_utc.astimezone(local_tz)
        tom_date = local_time + datetime.timedelta(days=days)
        while tom_date.strftime('%a').lower() in holiday_list or str(tom_date.strftime("%d%m%y")) in slot_id_list:
            tom_date = tom_date + datetime.timedelta(days=1)

        tomorrow = tom_date.strftime("%a").upper()
        return tomorrow

    def get_from_slot_list(self, ddmmyy, num_of_days):
        slot_id_list = []
        by = datetime.date(
            int('20' + ddmmyy[4:6]), int(ddmmyy[2:4]), int(ddmmyy[:2]))
        for day in range(0, num_of_days):
            time = by + datetime.timedelta(-day)
            slot_id_list.append(int(time.strftime('%y%m%d')))
        return slot_id_list

    def get_day_diff_from_yymmdd(self, yymmdd1, yymmdd2):
        yymmdd1 = str(yymmdd1)
        yymmdd2 =  str(yymmdd2)
        start_date = datetime.date(
            int('20' + yymmdd1[0:2]), int(yymmdd1[2:4]), int(yymmdd1[4:6]))
        end_date = datetime.date(
            int('20' + yymmdd2[0:2]), int(yymmdd2[2:4]), int(yymmdd2[4:6]))
        return (end_date - start_date).days

    def get_sec_ist_time(self,  ist_time):
        try:
            hour = ist_time.split(":")[0]
            minutes = ist_time.split(":")[1]
            am = ist_time.split(":")[2].upper()
            sec = 0
            if str(am)=="PM" and int(hour) <12:
                hour = int(hour)+12
            sec = int(hour)*60*60 + int(minutes)* 60
            return sec 

        except Exception as e:
            
            return 9*60

    def get_minutes_between_mil(self, start, end):
        start = datetime.datetime.strptime(str(start), '%H%M')
        end = datetime.datetime.strptime(str(end), '%H%M')
        return (end - start).total_seconds()/60

    def get_current_week(self):
        now_utc = datetime.datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        local_tz = pytz.timezone(TIME_ZONE)
        local_time = now_utc.astimezone(local_tz)
        week_day = local_time.isoweekday()
        start_slot = self.get_yymmdd(-week_day+1)
        if week_day < 7:
            end_slot = self.get_yymmdd(7-week_day)
        if week_day == 7:
            end_slot = self.get_yymmdd()
        return start_slot, end_slot 

    def get_days_elapsed(self, db_value):
        try:
            current_epoch = self.get_current_epoch()
            given_epoch = self.get_epoch_from_db_field(db_value)
            epoch_diff = current_epoch - given_epoch
            return int(epoch_diff / (24 * 60 * 60))
        except Exception as e:
            raise e
    
    def get_midnight_time(self):      
        from datetime import datetime, time
        midnight = datetime.combine(datetime.today(), time.min)
        return midnight

    def convert_from_epoch_to_military_time(self,epoch_time):
        tm=self.convert_into_db_format(epoch_time)
        new_tm=datetime.strptime(tm, '%Y-%m-%d %H:%M:%S')
        mil_time = int(('%0*d' % (2, new_tm.hour)) +
                       ('%0*d' % (2, new_tm.minute)))
        return mil_time

    def generate_epoch_of_specific_time(self,hour,minute):
        import datetime
        time=datetime.datetime.today()
        time=time.replace(hour=hour,minute=minute)
        epoch_time=int(time.strftime('%s'))
        return epoch_time

    def convert_datetime_local_to_epoch(self,date_in):
        date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
        date_processing.pop()
        date_processing = [int(v) for v in date_processing]
        date_out = datetime.datetime(*date_processing)
        epoch_time=int(date_out.strftime('%s'))+19800
        return epoch_time

    def is_diwali(self):
        epoch = self.get_current_epoch()
        date = self.convert_into_db_format(epoch,t_format='%Y-%m-%d')
        flag = False
        if date in ['2021-11-04', '2021-11-05']:
            hour = self.convert_into_db_format(epoch,t_format='%H')
            if not (date == '2021-11-04' and int(hour) < 17):
                flag = True
        return flag

    def get_expiry_from_slot_and_days(self, yymmdd1, best_before):
        """
        ddmmyy1- ddmmyy2
        """
        t = time.strptime(str(yymmdd1), '%y%m%d')
        d1 = datetime.date(t.tm_year, t.tm_mon, t.tm_mday)
        expiry=d1+datetime.timedelta(days=int(best_before))
        expiry=expiry.strftime('%y%m%d')
        return expiry
