from houses.House import *

class WilliamHill(House):
    def __init__(self):
        super().__init__()
        self.link = "https://sports.williamhill.es/betting/es-es"
        self.sports = {"tennis" : "tenis/partidos"}
        self.ret_bets = []

    def link_sport(self, sport):
        return f"{self.link}/{self.sports[sport]}"

    def sport_bets(self, sport):
        self.ret_bets = []
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
            teams_final = teams['title'].split('?')
            bets = match.findAll('button', attrs={'class':'btn betbutton oddsbutton'})
            for bet in bets:
                bets_final.append(bet.text)
            self.ret_bets.append(Bet(teams_final, bets_final))
        self.real_names()
        print("WilliamHill done")
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