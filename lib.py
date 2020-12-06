import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
import scipy.integrate as integrate

def getMinMaxDates(df):
    # find the dates that exist for all measurements
    maxdate = df.index.get_level_values('Unix').max()
    mindate = df.index.get_level_values('Unix').min()
    # for all buildings get the common denominator for min and max dates
    for i in np.unique(df.index.get_level_values('building')):
        mask = df.index.get_level_values('building') == i
        if (df.loc[mask].index.get_level_values('Unix').max()) < maxdate:
            maxdate = df.loc[mask].index.get_level_values('Unix').max()
        if (df.loc[mask].index.get_level_values('Unix').min()) > mindate:
            mindate = df.loc[mask].index.get_level_values('Unix').min()
    return (mindate, maxdate)

def on_times(appliance):
    """
        Parameters
        ----------
        appliance = a dataframe of an appliance witn an 'active' column

        Returns
        A dataframe with a datetime index and a column duration.
        Index is when the appliance started and duration the amount of slots the appliance was on (power>20watt).

    """
    records = len(appliance)
    on_dur = pd.DataFrame(columns=['duration'])
    i = 0
    # TODO(kyrcha): possible optimization with matrix
    while (i < records):
        j = 0
        if appliance['active'].values[i] > 50:
            # to parakatw to evala giati evgaze proeidopoihsh gia nan pou nomizw den isxye kiolas
            # todo: check if nan exist.
            np.warnings.filterwarnings('ignore')
            #αν δεν είναι το τελευταιο στοιχείο του πίνακα γιατί πετούσε έρρορ
            while appliance['active'].values[i + j] > 50:
                if j == 0:
                    on_time = appliance.index.get_level_values('Unix')[i]
                j = j + 1
                if ((i + j) == records):
                    break
            on_dur.loc[on_time] = j
            i = i + j -1
        i = i + 1
    return on_dur

def weekday (appliance):
    '''

    Parameters

    appliance

    Returns
    probs = a list of probabilities for each day

    '''
    new_app = appliance
    on_app = on_times(new_app)

    if on_app.empty:
        print('The appliance was never on')
        probs = []
    else:
        on_app['weekday'] = on_app.index.weekday
        new_app['weekday'] = new_app.index.get_level_values('Unix').weekday
        # για όλες τις μέρε του εξεταζόμενου διαστήματος φτιάχνουμε ένα dataframe [φτιάχνω καινούρια dataframe γιατί δν κτλβαίνω τι γίνεται στα παλιά αν τα κάνεις πχ resample]
        final_app = new_app.groupby([pd.Grouper(level='Unix', freq='D')]).mean()
        # για όλες τις μέρες που άνοιξε στο εξεταζόμενο διάστημα φτιάχνουμε ένα dataframe
        final_on_app = on_app.groupby(on_app.index.date).mean()
        #   μετράμε πόσες μέρες από κάθε είδος μέρας υπάρχει σε κάθε ένα από τα δύο dataframe
        days_on = final_on_app['weekday'].value_counts().to_frame().sort_index()
        days_total = final_app['weekday'].value_counts().to_frame().sort_index()
        # Η πιθανότητα μιας να είναι ανοιχτή μια καθημερινή ημέρα σε σχέση με το να μην είναι
        each_day_on = []
        each_day_total = []
        probs = []
        name_days = np.array(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        for i in range(0, 7):
            if i in days_on.index:
                each_day_on.append(days_on.loc[i]['weekday'])
                each_day_total.append(days_total.loc[i]['weekday'])
                #print("Number of ", name_days[i], "s the appliance was on: ", each_day_on[i], sep='')
                #print('Total number of ', name_days[i], 's ', each_day_total[i], sep='')
                probs.append(each_day_on[i] / each_day_total[i])
                #print('Probability P(', name_days[i], "_on) = ", probs[i], sep='')
            else:
                #print("The appliance didn't turn on on ", name_days[i], 's', sep='')
                each_day_on.append(0)
                each_day_total.append(days_total.loc[i]['weekday'])
                probs.append(0)
            i = i + 1
    return probs

def prob_time_new(appliance):
    '''

    Parameters
    ----------
    appliance = a dataframe of an appliance witn an 'active' column

    Returns
    a series of diffent start times & how many times they occured
    an array of the same thing

    '''
    #fig = plt.figure()
    #ax = fig.add_subplot(1,1,1)
    #fig.suptitle(name + ' time on', fontsize=16)
    new_app = appliance
    # check  mer
    if new_app.empty:
        print('The appliance was never on')
        ptonosx = []
    else:
        on_app = on_times(new_app)
        if len(on_app) > 1:
            #κάνω μια στηλη μόνο με τις ώρες από το Datatime index
            on_app['time'] = on_app.index.time
            #μου εβγαζε error αν εβαζα κατευθείαν το index στο GMM και γ αυτό έκανα όλο αυτό με τους πίνακες ώστε να φτάσω στο W
            Y = on_app['time'].index.to_list()
            X = []
            for i in range(0, len(Y)):
               X.append(Y[i].hour * 3600 + Y[i].minute * 60 + Y[i].second)
            fullX = X.copy()

            # need to plot these here...
            # do everything with  1 house in mind and plot

            # φτιάχνουμε ένα νέο population όπου αντί για 0-24h, θα απλώνεται σε -6h ως 30h,
            for i in range(0, len(fullX)):
                # προσθέτοντας τα samples που είναι στις ώρες 0-6 στις ώρες 24-30
                if (fullX[i] < 21600):
                    fullX.append(86400 + fullX[i])
                # προσθέτοντας τα samples που είναι στις ώρες 0-6 στις ώρες 24-30
                elif (fullX[i] > 64800):
                    fullX.append(fullX[i] - 86400)
            # μετακινούμε αυτό το νέο population σε 0-36h
            for i in range(0, len(fullX)):
                fullX[i] = fullX[i] + 21600
            fullXX = np.array(fullX)
            fullXX = fullXX.reshape(-1, 1)
            if fullXX.size < 10:
                # return empty array if data are not enough
                return []
            gmm = GaussianMixture(n_components=10, covariance_type='diag', reg_covar=100, n_init=5).fit(fullXX)
            x = np.arange(0, 129600, 1)
            x = x.reshape(-1, 1)
            p = np.exp(gmm.score_samples(x))
            # κρατάμε τις πιθανότητες από τις ώρες που μας ενδιαφέρουν όντως και κανονικοποιούμε
            ptonosx = p[21600:108000] / p[21600:108000].sum()

            #ax.plot(y,probability)
            #ax.hist(fullXX,bins=96,density=True)
            #ax.set_title(str(len(Y)) + ' times it was on', fontsize=12)
            #plt.show()
        else:
            print('The appliance was on 1 time')
            ptonosx = []
    return (ptonosx)

def prob_duration(appliance):
    """

    Parameters
    ----------
    appliance = a dataframe of an appliance
    name = the name of the appliance
    Returns
    a

    """
    idx = pd.IndexSlice
    new_app = appliance
    on_app = on_times(new_app)
    probs = on_app['duration'].value_counts(normalize=True).sort_index().to_frame()
    probs = probs.loc[idx[probs.index<96]] # keep one day's worth of duration...else next day
    #fig = plt.figure()
    #fig.suptitle(name + ' duration', fontsize=16)
    #ax = fig.add_subplot(1, 1, 1)
    #ax.bar(probs.index, probs)
    return probs

# ADD TO LIB
def train(df, start , end):
    prob_times = []
    prob_days = []
    prob_dur = []
    #train the machine
    idx = pd.IndexSlice
    for i in np.unique(df.index.get_level_values('building')):
        mask = df.index.get_level_values('building') == i
        prob_days.append(weekday(df.loc[idx[mask, :, start:end]]))
        prob_times.append(prob_time_new(df.loc[idx[mask, :, start:end]]))
        prob_dur.append(prob_duration(df.loc[idx[mask, :, start:end]]))
    return prob_times, prob_days, prob_dur

def slot (prob_days,prob_times,prob_dur,start,end):
    '''

    Parameters
    ----------
    prob_days - a list of 7 probabilities for each day
    prob_times - a list of 86400 probabilities for each second of the day
    prob_dur - probabilities of duration
    start - time of slot start
    end - time of slot end

    Returns
    -------

    '''
    idx = pd.IndexSlice
    slot_weekday = start.weekday()
    start_time = start.hour * 4 + start.minute
    end_time = end.hour * 4 + end.minute
    if prob_days != [] and prob_times != []:
        the_day = prob_days[slot_weekday]
        # για όταν συμπεριλάβουμε duration
        X = np.array(prob_dur.index.to_list())
        d_max = X.max()
        prob_times = prob_times.reshape(-1, 1)
        pfunctionx = lambda x: prob_times[int(x)]
        turns_on = integrate.quad(lambda x: pfunctionx(x)[0], start_time * 900, end_time * 900)[0]
        was_on = integrate.quad(lambda x: pfunctionx(start_time*900 - d_max*900 + x)[0]*prob_dur.loc[idx[prob_dur.index > (d_max-x/900)]].sum(), 0, d_max*900)[0]
        probability = the_day * (turns_on + was_on)
    else:
        probability = 0
    return probability