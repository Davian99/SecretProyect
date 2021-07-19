from houses.House import *

class WilliamHill(House):
    def __init__(self):
        super().__init__()
        self.link = "https://sports.williamhill.es/betting/es-es"
        self.sports = {"tennis" : "tenis/partidos", "table_tennis" : "tenis-de-mesa/partidos/fecha/hoy"}
        self.ret_bets = {}
        self.separators = {"tennis" : u"\u208B", "table_tennis" : u"\u208B"}
    
    def house(self):
        return "WilliamHill"

    def link_sport(self, sport):
        return f"{self.link}/{self.sports[sport]}"

    def sport_bets(self, sport):
        start = time.time()
        self.ret_bets[sport] = []
        self.driver.get(self.link_sport(sport))
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.2)
        response = self.driver.page_source
        soup = BeautifulSoup(response, "html.parser")
        matches = soup.findAll('div', attrs={'class':'event'})
        for match in matches:
            teams = match.find('a')
            teams_final, bets_final = [], []
            teams_final = teams['title'].split(self.separators[sport])
            bets = match.findAll('button', attrs={'class':'btn betbutton oddsbutton'})
            for bet in bets:
                bets_final.append(bet.text)
            b = Bet(teams_final, bets_final)
            self.ret_bets[sport].append(b)
        self.real_names(sport)
        end = time.time()
        print(f"WilliamHill done in {end - start:.2f}")
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