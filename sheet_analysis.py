import pandas as pd

def turn_sheet_into_frame(worksheet):
    list_of_lists = worksheet.get_all_values()
    df = pd.DataFrame(list_of_lists)
    # exclude people that are inactive
    df = df[df[1] != 'no']
    # drop active status column
    df = df.drop(1, axis=1)
    df = df.T
    # --fill in which book each speach is in--#
    for i in range(len(df)):
        try:
            if df[0].ix[i+1] == "":
                df[0].ix[i+1] = df[0].ix[i]
            else:
                df[0].ix[i+1] == df[0].ix[i+1]
        except:
            print('oops')
    df.ix[0, 0] = 'Book'
    df.ix[0, 1] = 'Project'

    df.columns = df.ix[0]
    return df


def drop_completed(advance_totals):
    advance_totals = advance_totals[advance_totals['Book'] != 'Competent Leader']
    advance_totals = advance_totals[advance_totals['Book'] != 'Competent Communicator']
    advance_totals = advance_totals[advance_totals['Book'] != 'Book']
    return advance_totals.reset_index().drop('index', axis=1)

def group_advance(df):
    advance_totals = df.groupby('Book').count().reset_index()[['Book', 'Project']]
    advance_totals = drop_completed(advance_totals)
    return advance_totals


def calculate_advance_manual_completion(advanced, advance_totals):
    # Advance totals is a dataframe with the name of each program
    # and a count of the number of projects in each program
    # Advanced is the same as DF but removed the CC and CL because
    # they are already graphed

    # calculate the amount for each person
    advance_people = advanced.ix[:,2:]
    names = advance_people.columns
    advance_manuals = advanced.ix[:,:2]
    loops = advance_people.shape[1]
    advanced_manuals_unique = list(advance_totals['Book'].unique())


    for name in names:
        books = []
        accomplishments = []
        toastmaster = advance_people[name]
        toastmaster = pd.concat([advance_manuals, toastmaster], axis=1)
        for manual in advanced_manuals_unique:
            projects = toastmaster[toastmaster['Book'] == manual]
            completed = len(projects[projects[name] != ''][name])
            books.append(manual)
            accomplishments.append(completed)

        # calculate the percentage of the total completed
        accomplishments = list(accomplishments/advance_totals['Project']*100)
        toastmaster = pd.DataFrame([books, accomplishments]).T
        toastmaster.columns = ['Book', name]
        advance_totals = advance_totals.merge(toastmaster, on='Book')

    advance_totals = advance_totals.rename(columns = {'Book':'Project', 'Project':'Book'})
    advance_totals['Book'] = 'Advance Manuals'
    return advance_totals
