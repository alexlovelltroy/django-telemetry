import datetime
# This assumes that you've only got utc times in your database.  Please don't put anything but utc in your database.  I'll cry.

def list_frequency(mylist):
    """ Turn a sequence with duplicates into a list of tuples matching item to frequency  """
    out = []
    if len(mylist) < 1:
        return out
    counter = {}
    for i in set(mylist):
        counter[i] = mylist.count(i)
    for x in counter:
        out.append((x, counter[x]))
    return sorted(out, key=lambda y: y[1], reverse=True)

def build_datestack(obj, date_field, qs=None):
    """ Build a sorted list of tuples matching a date to the number of dated events on that date including dates with zero """
    if not qs and not obj:
        return []
    if qs:
        obj_list = qs.order_by(date_field)
    else:
        obj_list = obj.objects.all().order_by(date_field)
    first_date = getattr(obj_list[0], date_field)
    last_date = getattr(obj_list[len(obj_list) -1], date_field)
    try:
        first_date = first_date.date()
        first_date = last_date.date()
        date_list = sorted(list_frequency([getattr(x,date_field).date() for x in obj_list]), key=lambda y: y[0], reverse=True)
    except AttributeError:
        date_list = sorted(list_frequency([getattr(x,date_field) for x in obj_list]), key=lambda y: y[0], reverse=True)
        pass
    out = []
    builder_date = first_date
    data_date = date_list.pop()
    while builder_date <= last_date:
        if data_date[0] == builder_date:
            out.append((builder_date, data_date[1]))
            try:
                data_date = date_list.pop()
            except IndexError:
                pass
        else:
            out.append((builder_date, 0))
        builder_date = builder_date + datetime.timedelta(days=1)
    return out

def rolling_average(datestack, days=7):
    """ Build a new datestack based on the one made by build_datestack that computes a rolling average"""
    # Assuming we've already summed everything, sorted everything, and zero days are included
    out = []
    for x in range(0, len(datestack)):
        if x > days:
            # calculate the sum
            sample_set = datestack[x - days:x]
            counter = 0
            for date, count in sample_set:
                counter = counter + count
            out.append((date, counter/float(days)))
    return out

def build_report(report_list, average=None):
    """ Using a list of dictionaries to build datestacks to work with, and optionally a rolling average
    [ dict(
        obj        = User, # A Django model
        date_field = 'date_joined', # the date or datetime field to count
        label      = "Users", # A convenient label to identify what's being counted
    ), ]

    In a view, you might add this to a context like this:
        for key, value in report.iteritems():
            context.update({key:value})

    Or as a serialized json object like this:
        dthandler = lambda obj: time.mktime(obj.timetuple()) if isinstance(obj, datetime.date) else None
        context['report_as_json'] = json.dumps(report, default=dthandler)
    """

    now = datetime.date.today()
    report = {}
    for each in report_list:
        obj = each.get('obj', None)
        date_field = each.get('date_field', None)
        label = each.get('label', None)
        qs = each.get('qs', None)
        if qs is None:
            qs = obj.objects.all()
        result = build_datestack(obj, date_field, qs=qs)
        report[label]  = result
        if average:
            # Check for "True",
            if isinstance(average, bool):
                report['rolling_%s' % label] = rolling_average(result)
            else:
                try:
                    report['rolling_%s'] = rolling_average(result, days=int(average))
                except TypeError:
                    # That's strange.  I expected average to be boolean or an int.  It wasn't  I don't understand what to do
                    pass

        report["%s_all_time" % label] = len(qs)
        try:
            report["%s_last_30" % label] = len([x for x in qs if getattr(x, date_field) > now - datetime.timedelta(days=30)])
            report["%s_last_60" % label] = len([x for x in qs if getattr(x, date_field) > now - datetime.timedelta(days=60)])
            report["%s_last_90" % label] = len([x for x in qs if getattr(x, date_field) > now - datetime.timedelta(days=90)])
        except TypeError: # These are datetimes
            report["%s_last_30" % label] = len([x for x in qs if getattr(x, date_field).date() > now - datetime.timedelta(days=30)])
            report["%s_last_60" % label] = len([x for x in qs if getattr(x, date_field).date() > now - datetime.timedelta(days=60)])
            report["%s_last_90" % label] = len([x for x in qs if getattr(x, date_field).date() > now - datetime.timedelta(days=90)])
    return report

