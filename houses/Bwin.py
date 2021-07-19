from houses.House import *

class Bwin(House):
    def __init__(self):
        super().__init__()
        self.link = "https://sports.bwin.es/es/sports"
        self.sports = {"tennis" : "tenis-5", "table_tennis" : "tenis-de-mesa-56/apuestas"}
        self.ret_bets = {}
        self.wait_element = {"tennis" : "#main-view > ms-widget-layout > ms-widget-slot.col-9.widget-slot", 
                             "table_tennis" : "#main-view > ms-widget-layout > ms-widget-slot.col-9.widget-slot"}

    def house(self):
        return "Bwin"

    def link_sport(self, sport):
        return f"{self.link}/{self.sports[sport]}"

    def sport_bets(self, sport):
        start = time.time()
        self.ret_bets[sport] = []
        self.driver.get(self.link_sport(sport))
        while True:
            try:
                self.driver.find_element_by_css_selector(self.wait_element[sport])
                break
            except:
                time.sleep(1)
                break
        response = self.driver.page_source
        soup = BeautifulSoup(response, "html.parser")        
        rows = soup.findAll('ms-event', attrs={'class': 'grid-event ms-active-highlight'})

        for row in rows:
            try:
                row = row.find('div', attrs={'class':'grid-event-wrapper'})
                teams = row.findAll('div', {'class':['participant-wrapper ng-star-inserted', 'participant-wrapper']})
                teams_final = []
                for team in teams:
                    team = team.find('div', attrs={'class':'participant'})
                    team = team.find(text=True, recursive=False).strip()
                    teams_final.append(team)

                bets = row.findAll('ms-option', attrs={'class':'grid-option'})
                bets_final = []
                for bet, _ in zip(bets, range(2)):
                    bets_final.append(bet.text)

                bet = Bet(teams_final, bets_final)
                self.ret_bets[sport].append(bet)
            except:
                pass
        self.real_names(sport)
        end = time.time()
        print(f"Bwin done in {end - start:.2f}")
        return self.ret_bets[sport]

    def real_names(self, sport):
        for bet in self.ret_bets[sport]:
            for team in bet.teams:
                cnt, l_f = 0, []
                for player in all_players[sport]:
                    if player[0] == team[0] or player[1] == team[1]:
                        cnt += 1
                        l_f.append((player, lev.jaro_winkler(player, team)))
                l_f.sort(key=lambda x: x[1], reverse=True)
                bet.real_teams.append(l_f[0][0])