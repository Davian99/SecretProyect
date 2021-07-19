from houses.House import *

class Retabet(House):
    def __init__(self):
        super().__init__()
        self.link = "https://apuestas.retabet.es"
        self.sports = {"tennis" : "tenis-m8"}
        self.ret_bets = {}

    def link_sport(self, sport):
        return f"{self.link}/deportes/{self.sports[sport]}"

    def sport_bets(self, sport):
        start = time.time()
        self.ret_bets[sport] = []
        self.driver.get(self.link_sport(sport))
        response = self.driver.page_source
        soup = BeautifulSoup(response, "html.parser")
        table = soup.find('ul', attrs={'class':'module__events-cont jbgroup'}) #TODO findAll
        for row in table:
            row = row.find('a', attrs={'class':'jlink'})
            teams = row.find('div', attrs={'class':'module__event-info'})
            teams = teams.find('ul', attrs={'class':'module__event-players'})
            teams = list(map(lambda elem: elem.text, teams.findAll('li')))

            bets = row.find('div', attrs={'class':'list-events__element__bets'})
            bets = row.find('div', attrs={'class':'module__bets-list jbet'})
            bets = row.findAll('li', attrs={'class':'jo module__bets-li'})
            bets_list = []
            for bet, _ in zip(bets, range(2)):
                bet = bet.find('span', attrs={'class':'jpr module__bets-cuota'})
                bets_list.append(bet.text)

            bet = Bet(teams, bets_list)
            self.ret_bets[sport].append(bet)
        self.real_names(sport)
        end = time.time()
        print(f"Retabet done in {end - start:.2f}")
        return self.ret_bets[sport]
    
    def real_names(self, sport):
        for bet in self.ret_bets[sport]:
            for team in bet.teams:
                cnt, l_f = 0, []
                for player in all_players[sport]:
                    if player[0] == team[0] and player.split()[-1] == team.split()[-1]:
                        cnt += 1
                        l_f.append((player, lev.jaro_winkler(bet.teams[0][::-1], player[::-1])))
                l_f.sort(key=lambda x: x[1], reverse=True)
                if cnt == 1:
                    bet.real_teams.append(l_f[0][0])