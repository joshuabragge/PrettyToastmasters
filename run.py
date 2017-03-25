import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from slackclient import SlackClient
import private
import plots as pl
import sheet_analysis as sh

if __name__ == "__main__":
    # connect to the google spreadsheet
    try:
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(private.filename, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open_by_key(private.google_sheet_key).worksheet(private.sheet_name)

        # turn the worksheet into a dataframe
        df = sh.turn_sheet_into_frame(worksheet)

        # total amount of projects in each manaual
        advance_totals = sh.group_advance(df)
        # progress of each member minus the CC and CL
        advanced = sh.drop_completed(df)
        advance_totals = sh.calculate_advance_manual_completion(advanced, advance_totals)
        # publish graph updates
        pl.publish_graph_update(df, 'Competent Communicator')
        pl.publish_graph_update(df, 'Competent Leader')
        pl.publish_graph_update(advance_totals, 'Advance Manuals', advanced=True)
    except:
        print('-------------error updating graphs-------------')
        try:
            sc = SlackClient(private.SLACK_TOKEN)
            sc.api_call("chat.postMessage", channel=private.SLACK_CHANNEL, text='error updating graphs',
                        username='PrettyToast', icon_emoji=':robot_face:')
        except:
            print('Error sending slack')
    time.sleep(5400)
