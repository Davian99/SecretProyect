from houses.House import *

class Bwin(House):
    def __init__(self):
        super().__init__()
        self.link = "https://sports.bwin.es/es/sports"
        self.sports = {"tennis" : "tenis-5"}
        self.ret_bets = []

    def link_sport(self, sport):
        return f"{self.link}/{self.sports[sport]}"

    def sport_bets(self, sport):
        self.ret_bets = []
        self.driver.get(self.link_sport(sport))
        while True:
            try:
                self.driver.find_element_by_css_selector('#main-view > ms-widget-layout > ms-widget-slot.col-9.widget-slot')
                break
            except:
                time.sleep(0.5)
        response = self.driver.page_source
        soup = BeautifulSoup(response, "html.parser")
        table1 = soup.find('ms-widget-slot', attrs={'class':'col-9 widget-slot'})
        table2 = table1.find('ms-tabbed-grid', attrs={'class':'grid-wrapper tabbed-grid-widget'})
        table3 = table2.find('ms-grid')
        table4 = table3.find('ms-event-group', attrs={'class':'event-group'})
        rows = table4.findAll('ms-event', attrs={'class':'grid-event ms-active-highlight'})
        
        ret_bets = []
        for row in rows:
            try:
                row = row.find('div', attrs={'class':'grid-event-wrapper'})
                
                teams = row.find('a', attrs={'class':'grid-info-wrapper fixed'})
                teams = teams.find('ms-event-detail', attrs={'class':'grid-event-detail'})
                teams = teams.find('ms-event-name', attrs={'class':'grid-event-name'})
                teams = teams.find('ms-inline-tooltip')
                teams = teams.find('div', attrs={'class':'participants-pair-game'})
                teams = teams.findAll('div', {'class':['participant-wrapper ng-star-inserted', 'participant-wrapper']})
                teams_final = []
                for team in teams:
                    team = team.find('div', attrs={'class':'participant'})
                    team = team.find(text=True, recursive=False).strip()
                    teams_final.append(team)

                bets = row.find('div', attrs={'class':'grid-group-container'})
                bets = row.find('ms-option-group', attrs={'class':'grid-option-group grid-group'})
                bets = row.findAll('ms-option', attrs={'class':'grid-option'})
                bets_final = []
                for bet, _ in zip(bets, range(2)):
                    bets_final.append(bet.text)

                bet = Bet(teams_final, bets_final)
                self.ret_bets.append(bet)
            except:
                pass
        self.real_names()
        print("Bwin done")
        return self.ret_bets

    def real_names(self):
        for bet in self.ret_bets:
            for team in bet.teams:
                cnt, l_f = 0, []
                for player in all_players:
                    if player[0] == team[0] or player[1] == team[1]:
                        cnt += 1
                        l_f.append((player, lev.jaro_winkler(player, team)))
                l_f.sort(key=lambda x: x[1], reverse=True)
                bet.real_teams.append(l_f[0][0])