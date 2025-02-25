import datetime
import json

def get_all_weeks_dates(total_weeks,starting_date,starting_month,starting_year):
    thirty_day_months = [4,6,9,10]
    february = 2
    
    weeks = []
    total_weeks = num_teams*num_rounds
    current_date = starting_date
    current_month = starting_month
    current_year = starting_year
    for _ in range(total_weeks):
        week = []
        for _ in range(7):
            current_date +=1
            if current_date>30 and current_month in thirty_day_months:
                current_date-=30
                current_month+=1
            elif current_date>28 and current_month==february:
                current_date-=28
                current_month+=1
            elif current_date>31:
                current_date-=31
                current_month+=1
            if current_month>12:
                current_month-=12
                current_year+=1
            # week.append((current_date,current_month,current_year))
            full_date = datetime.date(current_year,current_month,current_date)
            week.append(full_date.isoformat())
        weeks.append(week)
    return weeks

def get_matchup_calendar(num_teams,weeks):
    matchup_calendar = {}
    fixed = 0
    rotation = [i for i in range(1,num_teams)]
    for week_num, week in enumerate(weeks):
        matchup =[(fixed,rotation[0])]
        for i in range(1,len(rotation)//2+1):
            matchup.append((rotation[i],rotation[-i]))
        rotation=[rotation[-1]]+rotation[:-1]
        matchup_calendar[week_num]={'week':week,'pairs':matchup}
    return matchup_calendar

def get_matchup_scores(matchup_calendar):
    matchup_scores = {}
    for week in matchup_calendar:
        matchup_scores[week]=[]
        for pair in matchup_calendar[week]["pairs"]:
            matchup_scores[week].append({pair[0]:0,pair[1]:0})
    return matchup_scores

def generate_files(num_teams,num_rounds,starting_date,starting_month,starting_year):
    weeks = get_all_weeks_dates(num_teams*num_rounds,starting_date,starting_month,starting_year)
        
    matchup_calendar = get_matchup_calendar(num_teams,weeks)
    with open('matchupCalendar.json','w') as file:
        json.dump(matchup_calendar,file)
        
    matchup_scores = get_matchup_scores(matchup_calendar)
    with open('matchupScores.json','w') as file:
        json.dump(matchup_scores,file)
    return

if __name__ == "__main__":
    num_teams = 8
    num_rounds = 2
    starting_date = 16
    starting_month = 12
    starting_year = 2024
    generate_files(num_teams,num_rounds,starting_date,starting_month,starting_year)